"""Command execution module with security controls."""

import logging
import subprocess
import threading
import shlex
import resource
import signal
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import re

from ..security.permission_manager import PermissionManager
from ..core.types.security import SecurityContext, UserLevel

@dataclass
class ResourceLimits:
    """Resource limits for command execution"""
    max_cpu_time: int = 30  # seconds
    max_memory: int = 512 * 1024 * 1024  # 512MB in bytes
    max_processes: int = 10
    max_file_size: int = 50 * 1024 * 1024  # 50MB in bytes

@dataclass
class CommandResult:
    """Result of a command execution."""
    output: str
    error: Optional[str]
    exit_code: int
    timestamp: datetime
    resource_usage: Dict[str, float]

class CommandExecutor:
    """Secure command execution with permission checks."""

    # Commands that are never allowed
    BLACKLISTED_COMMANDS = {
        'rm', 'srm', 'shred',  # File deletion
        'mkfs', 'fdisk',       # Disk operations
        'mount', 'umount',     # Mount operations
        'dd',                  # Direct disk access
        'chmod', 'chown',      # Permission changes
        'sudo', 'su',          # Privilege escalation
        'passwd', 'chsh'       # User management
    }

    # Regex patterns for dangerous constructs
    DANGEROUS_PATTERNS = [
        r'[|;&`$]',           # Shell operators
        r'>\s*[^"]',          # Redirections
        r'<\s*[^"]',          # Input redirections
        r'\$\(',              # Command substitution
        r'\\[^nt]'            # Escapes except \n and \t
    ]

    def __init__(self, permission_manager: PermissionManager):
        self.permission_manager = permission_manager
        self._lock = threading.Lock()
        self.active_commands: Dict[str, subprocess.Popen] = {}
        self.command_limits: Dict[str, ResourceLimits] = {}

    def execute(self, command: str, context: SecurityContext) -> CommandResult:
        """Execute a command with security checks."""
        try:
            # Validate command
            if not self._validate_command(command, context):
                return CommandResult(
                    output="",
                    error="Command validation failed: Security violation",
                    exit_code=1,
                    timestamp=datetime.now(),
                    resource_usage={}
                )

            # Get resource limits
            limits = self._get_resource_limits(context.user_level)

            # Set up command execution
            args = shlex.split(command)
            
            # Apply resource limits
            def preexec():
                resource.setrlimit(resource.RLIMIT_CPU, (limits.max_cpu_time, limits.max_cpu_time))
                resource.setrlimit(resource.RLIMIT_AS, (limits.max_memory, limits.max_memory))
                resource.setrlimit(resource.RLIMIT_NPROC, (limits.max_processes, limits.max_processes))
                resource.setrlimit(resource.RLIMIT_FSIZE, (limits.max_file_size, limits.max_file_size))

            # Execute command
            with self._lock:
                process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=preexec,
                    text=True,
                    shell=False  # Never use shell=True
                )
                self.active_commands[context.session_id] = process

            try:
                # Wait with timeout
                stdout, stderr = process.communicate(timeout=limits.max_cpu_time)
            except subprocess.TimeoutExpired:
                self._terminate_process(process)
                return CommandResult(
                    output="",
                    error="Command timed out",
                    exit_code=124,
                    timestamp=datetime.now(),
                    resource_usage=self._get_resource_usage(process)
                )
            finally:
                # Cleanup
                with self._lock:
                    if context.session_id in self.active_commands:
                        del self.active_commands[context.session_id]

            return CommandResult(
                output=stdout,
                error=stderr if stderr else None,
                exit_code=process.returncode,
                timestamp=datetime.now(),
                resource_usage=self._get_resource_usage(process)
            )

        except Exception as e:
            logging.error(f"Command execution failed: {str(e)}")
            return CommandResult(
                output="",
                error=str(e),
                exit_code=1,
                timestamp=datetime.now(),
                resource_usage={}
            )

    def stop(self, session_id: str) -> bool:
        """Stop a running command."""
        with self._lock:
            if session_id in self.active_commands:
                process = self.active_commands[session_id]
                self._terminate_process(process)
                del self.active_commands[session_id]
                return True
        return False

    def _validate_command(self, command: str, context: SecurityContext) -> bool:
        """Validate command for security."""
        try:
            # Split command into parts
            parts = shlex.split(command)
            if not parts:
                return False

            # Check base command
            base_cmd = parts[0].lower()
            if base_cmd in self.BLACKLISTED_COMMANDS:
                logging.warning(f"Blocked blacklisted command: {base_cmd}")
                return False

            # Check for dangerous patterns
            for pattern in self.DANGEROUS_PATTERNS:
                if re.search(pattern, command):
                    logging.warning(f"Blocked command with dangerous pattern: {pattern}")
                    return False

            # Validate through permission manager
            if not self.permission_manager.check_permission(f"execute_{base_cmd}"):
                logging.warning(f"Permission denied for command: {base_cmd}")
                return False

            return True

        except Exception as e:
            logging.error(f"Command validation failed: {str(e)}")
            return False

    def _get_resource_limits(self, user_level: UserLevel) -> ResourceLimits:
        """Get resource limits based on user level."""
        if user_level == UserLevel.ADMIN:
            return ResourceLimits(
                max_cpu_time=300,    # 5 minutes
                max_memory=2 * 1024 * 1024 * 1024,  # 2GB
                max_processes=50,
                max_file_size=500 * 1024 * 1024  # 500MB
            )
        elif user_level == UserLevel.ADVANCED:
            return ResourceLimits(
                max_cpu_time=120,    # 2 minutes
                max_memory=1024 * 1024 * 1024,  # 1GB
                max_processes=20,
                max_file_size=100 * 1024 * 1024  # 100MB
            )
        else:
            return ResourceLimits()  # Default limits

    def _terminate_process(self, process: subprocess.Popen) -> None:
        """Safely terminate a process."""
        try:
            process.terminate()
            try:
                process.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        except Exception as e:
            logging.error(f"Process termination failed: {str(e)}")

    def _get_resource_usage(self, process: subprocess.Popen) -> Dict[str, float]:
        """Get resource usage statistics for a process."""
        try:
            with process.stdout, process.stderr:
                usage = resource.getrusage(resource.RUSAGE_CHILDREN)
                return {
                    'user_time': usage.ru_utime,
                    'system_time': usage.ru_stime,
                    'max_rss': usage.ru_maxrss,
                    'shared_memory': usage.ru_ixrss,
                    'unshared_memory': usage.ru_idrss,
                    'page_faults': usage.ru_majflt,
                    'block_input': usage.ru_inblock,
                    'block_output': usage.ru_oublock
                }
        except Exception as e:
            logging.error(f"Failed to get resource usage: {str(e)}")
            return {}

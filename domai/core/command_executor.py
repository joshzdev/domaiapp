"""
Command Executor for DōmAI
Handles secure command execution
"""

import subprocess
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
import shlex

@dataclass
class CommandResult:
    """Command execution result"""
    success: bool
    output: str
    error: Optional[str] = None

class CommandExecutor:
    """Handles secure command execution"""
    
    def __init__(self):
        self.logger = logging.getLogger("domai.executor")
        
    def execute(self, command: str) -> CommandResult:
        """Execute command securely"""
        try:
            # Sanitize command
            command = self._sanitize_command(command)
            
            # Execute command
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            # Process result
            success = process.returncode == 0
            output = process.stdout
            error = process.stderr if process.stderr else None
            
            if not success:
                self.logger.warning(f"Command failed: {error}")
            
            return CommandResult(
                success=success,
                output=output,
                error=error
            )
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return CommandResult(
                success=False,
                output="",
                error=str(e)
            )
            
    def _sanitize_command(self, command: str) -> str:
        """Sanitize command for secure execution"""
        # Split command into parts
        parts = shlex.split(command)
        
        # Basic sanitization
        sanitized = []
        for part in parts:
            # Remove dangerous characters
            part = part.replace(";", "")
            part = part.replace("&&", "")
            part = part.replace("||", "")
            part = part.replace("|", "")
            part = part.replace(">", "")
            part = part.replace("<", "")
            sanitized.append(part)
            
        # Rejoin command
        return " ".join(sanitized)

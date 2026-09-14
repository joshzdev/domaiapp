#!/usr/bin/env python3
"""
DōmAI Permission Management System
Handles elevated privileges securely with user consent and audit logging
"""

import os
import pwd
import grp
import logging
import threading
from typing import Dict, List, Optional, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import time
from pathlib import Path

class PrivilegeLevel(Enum):
    NORMAL = "normal"         # No special privileges
    ELEVATED = "elevated"     # Some system access (e.g., reading system files)
    ADMIN = "admin"          # Full system access (requires sudo/root)

@dataclass
class Permission:
    name: str
    level: PrivilegeLevel
    description: str
    reason: str
    commands: List[str]
    alternatives: List[str]
    expiry: Optional[datetime] = None
    rate_limit: int = 10  # Max requests per minute

class PermissionManager:
    """Manages system permissions and privileged operations"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.granted_permissions: Dict[str, Permission] = {}
        self.permission_requests: Dict[str, List[datetime]] = {}
        self._setup_audit_logging()
        
        # Define known permissions
        self.permissions: Dict[str, Permission] = {
            "packet_capture": Permission(
                name="packet_capture",
                level=PrivilegeLevel.ADMIN,
                description="Capture network packets",
                reason="Required for network monitoring and security analysis",
                commands=["tcpdump"],
                alternatives=["Wireshark (GUI)", "tshark (CLI)"]
            ),
            "process_monitor": Permission(
                name="process_monitor",
                level=PrivilegeLevel.ELEVATED,
                description="Monitor system processes",
                reason="Required for security monitoring",
                commands=["ps", "top", "lsof"],
                alternatives=["Activity Monitor (GUI)"]
            ),
            "file_monitor": Permission(
                name="file_monitor",
                level=PrivilegeLevel.ELEVATED,
                description="Monitor filesystem changes",
                reason="Required for security monitoring",
                commands=["fswatch", "fs_usage"],
                alternatives=["Folder watching (limited)"]
            )
        }
        
        # Start cleanup thread
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_expired_permissions,
            daemon=True
        )
        self._cleanup_thread.start()
        
    def _setup_audit_logging(self) -> None:
        """Setup secure audit logging"""
        log_dir = Path("logs/security")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Secure log directory
        os.chmod(log_dir, 0o700)
        
        # Setup audit log file
        self.audit_log_file = log_dir / "permissions.log"
        self.audit_log_file.touch(mode=0o600, exist_ok=True)
        
        # Configure logger
        audit_handler = logging.FileHandler(self.audit_log_file)
        audit_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        
        self.audit_logger = logging.getLogger("domai.security.permissions")
        self.audit_logger.addHandler(audit_handler)
        self.audit_logger.setLevel(logging.INFO)
        
    def check_permission(self, permission_name: str) -> bool:
        """Check if permission is currently granted"""
        if not self._validate_permission_name(permission_name):
            return False
            
        with self._lock:
            if permission_name not in self.granted_permissions:
                return False
                
            perm = self.granted_permissions[permission_name]
            if perm.expiry and datetime.now() > perm.expiry:
                self.release_permission(permission_name)
                return False
                
            return True
            
    def request_permission(self, permission_name: str) -> bool:
        """Request permission with rate limiting and validation"""
        if not self._validate_permission_name(permission_name):
            return False
            
        with self._lock:
            # Check rate limiting
            if not self._check_rate_limit(permission_name):
                self.audit_logger.warning(
                    f"Rate limit exceeded for permission: {permission_name}"
                )
                return False
                
            # Get permission definition
            perm = self.permissions[permission_name]
            
            try:
                # Log permission request
                self._log_request(permission_name, perm.level)
                
                # Check current privileges
                current_privileges = self._get_current_privileges()
                
                # Handle elevation if needed
                if perm.level == PrivilegeLevel.ADMIN and current_privileges != PrivilegeLevel.ADMIN:
                    if not self._request_elevation(perm):
                        return False
                        
                # Grant permission with expiry
                self.granted_permissions[permission_name] = Permission(
                    **perm.__dict__,
                    expiry=datetime.now() + timedelta(minutes=30)
                )
                
                self._log_grant(permission_name)
                return True
                
            except Exception as e:
                self.audit_logger.error(
                    f"Permission request failed: {str(e)}"
                )
                return False
                
    def release_permission(self, permission_name: str) -> None:
        """Release a previously granted permission"""
        if not self._validate_permission_name(permission_name):
            return
            
        with self._lock:
            if permission_name in self.granted_permissions:
                del self.granted_permissions[permission_name]
                self._log_release(permission_name)
                
    def _validate_permission_name(self, name: str) -> bool:
        """Validate permission name exists"""
        return name in self.permissions
        
    def _check_rate_limit(self, permission_name: str) -> bool:
        """Check rate limiting for permission requests"""
        now = datetime.now()
        
        # Initialize request history
        if permission_name not in self.permission_requests:
            self.permission_requests[permission_name] = []
            
        # Clean old requests
        self.permission_requests[permission_name] = [
            t for t in self.permission_requests[permission_name]
            if (now - t).total_seconds() < 60
        ]
        
        # Check limit
        perm = self.permissions[permission_name]
        if len(self.permission_requests[permission_name]) >= perm.rate_limit:
            return False
            
        # Add new request
        self.permission_requests[permission_name].append(now)
        return True
        
    def _cleanup_expired_permissions(self) -> None:
        """Cleanup expired permissions periodically"""
        while True:
            try:
                with self._lock:
                    now = datetime.now()
                    expired = [
                        name for name, perm in self.granted_permissions.items()
                        if perm.expiry and now > perm.expiry
                    ]
                    for name in expired:
                        self.release_permission(name)
                        
            except Exception as e:
                self.audit_logger.error(
                    f"Permission cleanup failed: {str(e)}"
                )
                
            time.sleep(60)  # Check every minute
            
    def _log_request(self, permission_name: str, level: PrivilegeLevel) -> None:
        """Log permission request to audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "request",
            "permission": permission_name,
            "level": level.value,
            "process_id": os.getpid(),
            "user": pwd.getpwuid(os.getuid())[0]
        }
        self.audit_logger.info(f"Permission request: {json.dumps(entry)}")
        
    def _log_grant(self, permission_name: str) -> None:
        """Log permission grant to audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "grant",
            "permission": permission_name,
            "process_id": os.getpid(),
            "user": pwd.getpwuid(os.getuid())[0]
        }
        self.audit_logger.info(f"Permission granted: {json.dumps(entry)}")
        
    def _log_release(self, permission_name: str) -> None:
        """Log permission release to audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "release",
            "permission": permission_name,
            "process_id": os.getpid(),
            "user": pwd.getpwuid(os.getuid())[0]
        }
        self.audit_logger.info(f"Permission released: {json.dumps(entry)}")
        
    def get_command_wrapper(self, command: str) -> Optional[str]:
        """Get appropriate wrapper for privileged command"""
        # Find permission that includes this command
        for perm in self.permissions.values():
            if command in perm.commands:
                if self.check_permission(perm.name):
                    if perm.level == PrivilegeLevel.ADMIN:
                        return "sudo"  # Use sudo for admin commands
                break
                
        return None
        
    def _get_current_privileges(self) -> PrivilegeLevel:
        """Determine current process privileges"""
        if os.geteuid() == 0:
            return PrivilegeLevel.ADMIN
            
        # Check group membership
        groups = [g.gr_name for g in grp.getgrall() if pwd.getpwuid(os.getuid())[0] in g.gr_mem]
        if "admin" in groups:
            return PrivilegeLevel.ELEVATED
            
        return PrivilegeLevel.NORMAL
        
    def _request_elevation(self, permission: Permission) -> bool:
        """Request privilege elevation from user"""
        # This would integrate with system's privilege elevation
        # For now, we'll assume it's handled externally
        return True

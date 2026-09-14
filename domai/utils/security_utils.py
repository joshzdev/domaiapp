"""
Security Utilities for DōmAI
Helper functions for MacOS security operations
"""

import logging
import subprocess
import re
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import shlex

class SecurityStatus(Enum):
    """Security feature status"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    PARTIAL = "partial"
    UNKNOWN = "unknown"

@dataclass
class SecurityCheck:
    """Security check result"""
    feature: str
    status: SecurityStatus
    details: str
    timestamp: float
    recommendations: Optional[str] = None

class SecurityUtils:
    """MacOS security utility functions"""
    
    def __init__(self):
        self.logger = logging.getLogger("domai.security")
        
    def check_sip_status(self) -> SecurityCheck:
        """Check System Integrity Protection status"""
        try:
            result = subprocess.run(
                ['csrutil', 'status'],
                capture_output=True,
                text=True
            )
            
            status = SecurityStatus.UNKNOWN
            if "enabled" in result.stdout.lower():
                status = SecurityStatus.ENABLED
            elif "disabled" in result.stdout.lower():
                status = SecurityStatus.DISABLED
                
            return SecurityCheck(
                feature="System Integrity Protection",
                status=status,
                details=result.stdout.strip(),
                timestamp=float(subprocess.check_output(['date', '+%s']))
            )
            
        except Exception as e:
            self.logger.error(f"SIP check failed: {str(e)}")
            return SecurityCheck(
                feature="System Integrity Protection",
                status=SecurityStatus.UNKNOWN,
                details=f"Check failed: {str(e)}",
                timestamp=float(subprocess.check_output(['date', '+%s']))
            )
            
    def check_firewall_status(self) -> SecurityCheck:
        """Check Application Firewall status"""
        try:
            result = subprocess.run(
                ['defaults', 'read', '/Library/Preferences/com.apple.alf', 'globalstate'],
                capture_output=True,
                text=True
            )
            
            status = SecurityStatus.UNKNOWN
            if result.stdout.strip() == "1":
                status = SecurityStatus.ENABLED
            elif result.stdout.strip() == "0":
                status = SecurityStatus.DISABLED
                
            return SecurityCheck(
                feature="Application Firewall",
                status=status,
                details=f"Firewall is {status.value}",
                timestamp=float(subprocess.check_output(['date', '+%s'])),
                recommendations="Enable firewall for better security" if status == SecurityStatus.DISABLED else None
            )
            
        except Exception as e:
            self.logger.error(f"Firewall check failed: {str(e)}")
            return SecurityCheck(
                feature="Application Firewall",
                status=SecurityStatus.UNKNOWN,
                details=f"Check failed: {str(e)}",
                timestamp=float(subprocess.check_output(['date', '+%s']))
            )
            
    def check_filevault_status(self) -> SecurityCheck:
        """Check FileVault encryption status"""
        try:
            result = subprocess.run(
                ['fdesetup', 'status'],
                capture_output=True,
                text=True
            )
            
            status = SecurityStatus.UNKNOWN
            if "FileVault is On" in result.stdout:
                status = SecurityStatus.ENABLED
            elif "FileVault is Off" in result.stdout:
                status = SecurityStatus.DISABLED
                
            return SecurityCheck(
                feature="FileVault",
                status=status,
                details=result.stdout.strip(),
                timestamp=float(subprocess.check_output(['date', '+%s'])),
                recommendations="Enable FileVault for disk encryption" if status == SecurityStatus.DISABLED else None
            )
            
        except Exception as e:
            self.logger.error(f"FileVault check failed: {str(e)}")
            return SecurityCheck(
                feature="FileVault",
                status=SecurityStatus.UNKNOWN,
                details=f"Check failed: {str(e)}",
                timestamp=float(subprocess.check_output(['date', '+%s']))
            )
            
    def check_gatekeeper_status(self) -> SecurityCheck:
        """Check Gatekeeper status"""
        try:
            result = subprocess.run(
                ['spctl', '--status'],
                capture_output=True,
                text=True
            )
            
            status = SecurityStatus.UNKNOWN
            if "assessments enabled" in result.stdout.lower():
                status = SecurityStatus.ENABLED
            elif "assessments disabled" in result.stdout.lower():
                status = SecurityStatus.DISABLED
                
            return SecurityCheck(
                feature="Gatekeeper",
                status=status,
                details=result.stdout.strip(),
                timestamp=float(subprocess.check_output(['date', '+%s'])),
                recommendations="Enable Gatekeeper for app security" if status == SecurityStatus.DISABLED else None
            )
            
        except Exception as e:
            self.logger.error(f"Gatekeeper check failed: {str(e)}")
            return SecurityCheck(
                feature="Gatekeeper",
                status=SecurityStatus.UNKNOWN,
                details=f"Check failed: {str(e)}",
                timestamp=float(subprocess.check_output(['date', '+%s']))
            )
            
    def validate_permissions(self, path: str) -> Tuple[bool, str]:
        """Validate file/directory permissions"""
        try:
            result = subprocess.run(
                ['ls', '-l', path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return False, f"Permission check failed: {result.stderr}"
                
            # Parse permissions
            perms = result.stdout.split()[0]
            owner = result.stdout.split()[2]
            group = result.stdout.split()[3]
            
            # Basic security checks
            is_secure = True
            issues = []
            
            # Check world-writable
            if perms[-2] == 'w':
                is_secure = False
                issues.append("World-writable")
                
            # Check owner
            if owner == "root" and perms[1:4] != "---":
                is_secure = False
                issues.append("Root-owned with non-root permissions")
                
            return is_secure, "; ".join(issues) if issues else "Permissions are secure"
            
        except Exception as e:
            self.logger.error(f"Permission validation failed: {str(e)}")
            return False, f"Validation failed: {str(e)}"
            
    def check_quarantine_attribute(self, path: str) -> bool:
        """Check if file has quarantine attribute"""
        try:
            result = subprocess.run(
                ['xattr', path],
                capture_output=True,
                text=True
            )
            
            return "com.apple.quarantine" in result.stdout
            
        except Exception as e:
            self.logger.error(f"Quarantine check failed: {str(e)}")
            return False
            
    def get_security_assessment(self) -> Dict[str, SecurityCheck]:
        """Get comprehensive security assessment"""
        return {
            "sip": self.check_sip_status(),
            "firewall": self.check_firewall_status(),
            "filevault": self.check_filevault_status(),
            "gatekeeper": self.check_gatekeeper_status()
        } 
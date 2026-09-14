"""
macOS firewall management module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
import shutil
from enum import Enum, auto

class FirewallStatus(Enum):
    """Firewall status enumeration"""
    ENABLED = auto()
    DISABLED = auto()
    ERROR = auto()

class FirewallManager:
    """Manage macOS packet filter firewall"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._pfctl_path = self._get_pfctl_path()
        
    def _get_pfctl_path(self) -> Path:
        """Get the full path to pfctl binary"""
        pfctl_path = shutil.which('pfctl')
        if not pfctl_path:
            raise RuntimeError("pfctl not found. Firewall management requires root privileges.")
        return Path(pfctl_path)

    def _run_pfctl_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run pfctl command with proper security checks"""
        if not self._pfctl_path.exists():
            raise FileNotFoundError("pfctl binary not found")
            
        cmd = [str(self._pfctl_path)] + args
        
        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=10  # Add timeout
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError("pfctl command timed out")

    def get_status(self) -> Dict[str, Union[str, FirewallStatus]]:
        """Get firewall status"""
        try:
            proc = self._run_pfctl_command(["-s", "info"])
            status_dict = self._parse_status(proc.stdout)
            
            # Add enum status
            status_dict["status"] = (FirewallStatus.ENABLED 
                                   if "Enabled" in proc.stdout 
                                   else FirewallStatus.DISABLED)
            return status_dict
            
        except Exception as e:
            self.logger.error(f"Error getting firewall status: {str(e)}")
            return {"status": FirewallStatus.ERROR, "message": str(e)}

    def get_rules(self) -> List[Dict[str, str]]:
        """Get current firewall rules"""
        try:
            proc = self._run_pfctl_command(["-s", "rules"])
            return self._parse_rules(proc.stdout)
        except Exception as e:
            self.logger.error(f"Error getting firewall rules: {str(e)}")
            return []

    def get_state(self) -> List[Dict[str, str]]:
        """Get firewall state table"""
        try:
            proc = self._run_pfctl_command(["-s", "state"])
            return self._parse_state(proc.stdout)
        except Exception as e:
            self.logger.error(f"Error getting firewall state: {str(e)}")
            return []

    def update_rules(self, rules_file: Path) -> bool:
        """Update firewall rules from file"""
        try:
            if not rules_file.exists():
                raise FileNotFoundError(f"Rules file not found: {rules_file}")
                
            if not rules_file.is_file():
                raise ValueError(f"Not a regular file: {rules_file}")
                
            proc = self._run_pfctl_command(["-f", str(rules_file)])
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating firewall rules: {str(e)}")
            return False

    # ... rest of the parsing methods remain the same ...
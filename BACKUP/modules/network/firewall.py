"""
macOS firewall management module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class FirewallManager:
    """Manage macOS packet filter firewall"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_status(self) -> Dict[str, Any]:
        """Get firewall status"""
        try:
            # Check pfctl status
            cmd = ["pfctl", "-s", "info"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_status(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"pfctl failed: {e.stderr}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            self.logger.error(f"Error getting firewall status: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def get_rules(self) -> List[Dict[str, Any]]:
        """Get current firewall rules"""
        try:
            # Get rules from pfctl
            cmd = ["pfctl", "-s", "rules"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_rules(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"pfctl failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting firewall rules: {str(e)}")
            return []
            
    def get_state(self) -> List[Dict[str, Any]]:
        """Get firewall state table"""
        try:
            # Get state table
            cmd = ["pfctl", "-s", "state"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_state(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"pfctl failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting firewall state: {str(e)}")
            return []
            
    def update_rules(self, rules_file: Path) -> bool:
        """Update firewall rules from file"""
        try:
            # Load new rules
            cmd = ["pfctl", "-f", str(rules_file)]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"pfctl failed: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Error updating firewall rules: {str(e)}")
            return False
            
    def _parse_status(self, output: str) -> Dict[str, Any]:
        """Parse pfctl status output"""
        status = {}
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            if ":" in line:
                key, value = line.split(":", 1)
                status[key.strip()] = value.strip()
                
        return status
        
    def _parse_rules(self, output: str) -> List[Dict[str, Any]]:
        """Parse pfctl rules output"""
        rules = []
        current_rule = {}
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                if current_rule:
                    rules.append(current_rule)
                    current_rule = {}
                continue
                
            # Parse rule components
            if line.startswith("@"):
                current_rule["id"] = line
            elif "pass" in line or "block" in line:
                current_rule["action"] = "pass" if "pass" in line else "block"
                current_rule["rule"] = line
                
        if current_rule:
            rules.append(current_rule)
            
        return rules
        
    def _parse_state(self, output: str) -> List[Dict[str, Any]]:
        """Parse pfctl state table output"""
        states = []
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            # Parse state entry
            try:
                parts = line.split()
                if len(parts) >= 4:
                    state = {
                        "protocol": parts[0],
                        "source": parts[1],
                        "destination": parts[2],
                        "state": parts[3]
                    }
                    states.append(state)
            except Exception as e:
                self.logger.error(f"Error parsing state line: {str(e)}")
                continue
                
        return states 
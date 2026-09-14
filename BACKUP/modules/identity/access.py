"""
Access control monitoring module
Handles access control monitoring and management
"""

import logging
import subprocess
import pwd
import grp
from typing import Optional, Dict, Any, List, Set
from pathlib import Path
from datetime import datetime

class AccessMonitor:
    """Monitor access control and authentication"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_sudo_config(self) -> Dict[str, Any]:
        """Get sudo configuration"""
        try:
            # Read sudoers file
            cmd = ["sudo", "cat", "/etc/sudoers"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"Failed to read sudoers: {proc.stderr}")
                
            return self._parse_sudoers(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting sudo config: {str(e)}")
            return {}
            
    def get_pam_config(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get PAM configuration"""
        try:
            configs = {}
            
            # Common PAM service files
            pam_files = [
                "common-auth",
                "common-account",
                "common-password",
                "common-session",
                "sudo"
            ]
            
            # Read each PAM file
            for pam_file in pam_files:
                path = Path(f"/etc/pam.d/{pam_file}")
                if path.exists():
                    try:
                        text = path.read_text()
                        configs[pam_file] = self._parse_pam_config(text)
                    except Exception as e:
                        self.logger.error(f"Error reading {pam_file}: {str(e)}")
                        continue
                        
            return configs
            
        except Exception as e:
            self.logger.error(f"Error getting PAM config: {str(e)}")
            return {}
            
    def get_ssh_config(self) -> Dict[str, Any]:
        """Get SSH configuration"""
        try:
            config = {
                "allow_users": [],
                "deny_users": [],
                "allow_groups": [],
                "deny_groups": [],
                "settings": {}
            }
            
            # Read sshd config
            path = Path("/etc/ssh/sshd_config")
            if path.exists():
                text = path.read_text()
                config.update(self._parse_ssh_config(text))
                
            return config
            
        except Exception as e:
            self.logger.error(f"Error getting SSH config: {str(e)}")
            return {}
            
    def get_login_config(self) -> Dict[str, Any]:
        """Get login configuration"""
        try:
            config = {}
            
            # Read login.defs
            path = Path("/etc/login.defs")
            if path.exists():
                text = path.read_text()
                config["login_defs"] = self._parse_login_defs(text)
                
            # Read login.access
            path = Path("/etc/security/login.access")
            if path.exists():
                text = path.read_text()
                config["login_access"] = self._parse_login_access(text)
                
            return config
            
        except Exception as e:
            self.logger.error(f"Error getting login config: {str(e)}")
            return {}
            
    def check_user_access(self, username: str) -> Dict[str, bool]:
        """Check user's access permissions"""
        try:
            access = {
                "can_login": False,
                "can_sudo": False,
                "ssh_allowed": False,
                "is_locked": False
            }
            
            # Check if account is locked
            cmd = ["passwd", "-S", username]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode == 0:
                access["is_locked"] = "L" in proc.stdout
                
            # Check sudo access
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            access["can_sudo"] = "sudo" in groups or "admin" in groups or "wheel" in groups
            
            # Check SSH access
            ssh_config = self.get_ssh_config()
            
            if ssh_config["allow_users"] and username not in ssh_config["allow_users"]:
                access["ssh_allowed"] = False
            elif username in ssh_config["deny_users"]:
                access["ssh_allowed"] = False
            elif any(g in ssh_config["allow_groups"] for g in groups):
                access["ssh_allowed"] = True
            elif any(g in ssh_config["deny_groups"] for g in groups):
                access["ssh_allowed"] = False
            else:
                access["ssh_allowed"] = True
                
            # Check if user can login
            try:
                user = pwd.getpwnam(username)
                access["can_login"] = user.pw_shell not in ["/sbin/nologin", "/bin/false"]
            except KeyError:
                access["can_login"] = False
                
            return access
            
        except Exception as e:
            self.logger.error(f"Error checking user access: {str(e)}")
            return {
                "can_login": False,
                "can_sudo": False,
                "ssh_allowed": False,
                "is_locked": True
            }
            
    def _parse_sudoers(self, content: str) -> Dict[str, Any]:
        """Parse sudoers file content"""
        config = {
            "aliases": {
                "user": {},
                "runas": {},
                "host": {},
                "command": {}
            },
            "defaults": [],
            "rules": []
        }
        
        try:
            current_section = None
            
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                if line.startswith("User_Alias"):
                    current_section = "user"
                    config["aliases"]["user"].update(self._parse_alias(line))
                elif line.startswith("Runas_Alias"):
                    current_section = "runas"
                    config["aliases"]["runas"].update(self._parse_alias(line))
                elif line.startswith("Host_Alias"):
                    current_section = "host"
                    config["aliases"]["host"].update(self._parse_alias(line))
                elif line.startswith("Cmnd_Alias"):
                    current_section = "command"
                    config["aliases"]["command"].update(self._parse_alias(line))
                elif line.startswith("Defaults"):
                    config["defaults"].append(self._parse_defaults(line))
                else:
                    rule = self._parse_sudo_rule(line)
                    if rule:
                        config["rules"].append(rule)
                        
        except Exception as e:
            self.logger.error(f"Error parsing sudoers: {str(e)}")
            
        return config
        
    def _parse_pam_config(self, content: str) -> List[Dict[str, Any]]:
        """Parse PAM configuration file"""
        rules = []
        
        try:
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split()
                if len(parts) >= 3:
                    rule = {
                        "type": parts[0],
                        "control": parts[1],
                        "module": parts[2],
                        "args": parts[3:] if len(parts) > 3 else []
                    }
                    rules.append(rule)
                    
        except Exception as e:
            self.logger.error(f"Error parsing PAM config: {str(e)}")
            
        return rules
        
    def _parse_ssh_config(self, content: str) -> Dict[str, Any]:
        """Parse SSH configuration file"""
        config = {
            "allow_users": [],
            "deny_users": [],
            "allow_groups": [],
            "deny_groups": [],
            "settings": {}
        }
        
        try:
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0].lower()
                    value = " ".join(parts[1:])
                    
                    if key == "allowusers":
                        config["allow_users"].extend(value.split())
                    elif key == "denyusers":
                        config["deny_users"].extend(value.split())
                    elif key == "allowgroups":
                        config["allow_groups"].extend(value.split())
                    elif key == "denygroups":
                        config["deny_groups"].extend(value.split())
                    else:
                        config["settings"][key] = value
                        
        except Exception as e:
            self.logger.error(f"Error parsing SSH config: {str(e)}")
            
        return config
        
    def _parse_login_defs(self, content: str) -> Dict[str, Any]:
        """Parse login.defs file"""
        config = {}
        
        try:
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0]
                    value = " ".join(parts[1:])
                    config[key] = value
                    
        except Exception as e:
            self.logger.error(f"Error parsing login.defs: {str(e)}")
            
        return config
        
    def _parse_login_access(self, content: str) -> List[Dict[str, Any]]:
        """Parse login.access file"""
        rules = []
        
        try:
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split(":")
                if len(parts) == 3:
                    rule = {
                        "permission": parts[0],
                        "users": parts[1].split(),
                        "origins": parts[2].split()
                    }
                    rules.append(rule)
                    
        except Exception as e:
            self.logger.error(f"Error parsing login.access: {str(e)}")
            
        return rules
        
    def _parse_alias(self, line: str) -> Dict[str, List[str]]:
        """Parse sudoers alias line"""
        aliases = {}
        
        try:
            parts = line.split("=", 1)
            if len(parts) == 2:
                name = parts[0].split()[-1]
                values = [v.strip() for v in parts[1].split(",")]
                aliases[name] = values
                
        except Exception as e:
            self.logger.error(f"Error parsing alias: {str(e)}")
            
        return aliases
        
    def _parse_defaults(self, line: str) -> Dict[str, Any]:
        """Parse sudoers defaults line"""
        defaults = {
            "type": "global",
            "target": None,
            "options": {}
        }
        
        try:
            parts = line.split()
            if ">" in parts[0]:
                defaults["type"] = "runas"
                defaults["target"] = parts[0].split(">")[1]
            elif ":" in parts[0]:
                defaults["type"] = "user"
                defaults["target"] = parts[0].split(":")[1]
            elif "@" in parts[0]:
                defaults["type"] = "host"
                defaults["target"] = parts[0].split("@")[1]
                
            for option in parts[1:]:
                if "=" in option:
                    key, value = option.split("=", 1)
                    defaults["options"][key] = value
                else:
                    defaults["options"][option] = True
                    
        except Exception as e:
            self.logger.error(f"Error parsing defaults: {str(e)}")
            
        return defaults
        
    def _parse_sudo_rule(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse sudoers rule line"""
        try:
            parts = line.split()
            if len(parts) >= 2:
                rule = {
                    "user": parts[0],
                    "host": "ALL",
                    "runas": "ALL",
                    "commands": []
                }
                
                # Parse host specification
                if parts[1] != "ALL":
                    rule["host"] = parts[1]
                    
                # Parse command specification
                cmd_part = " ".join(parts[2:])
                if "=" in cmd_part:
                    runas, cmds = cmd_part.split("=", 1)
                    if runas:
                        rule["runas"] = runas.strip("()")
                    rule["commands"] = [c.strip() for c in cmds.split(",")]
                else:
                    rule["commands"] = [cmd_part]
                    
                return rule
                
        except Exception as e:
            self.logger.error(f"Error parsing sudo rule: {str(e)}")
            
        return None 
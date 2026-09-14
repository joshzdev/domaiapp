"""
User management module
Handles user tracking and management
"""

import logging
import pwd
import grp
import subprocess
from typing import Optional, Dict, Any, List, Set
from pathlib import Path
from datetime import datetime

class UserManager:
    """Manage and track system users"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_users(self) -> List[Dict[str, Any]]:
        """Get list of system users"""
        try:
            users = []
            
            # Get all users from passwd
            for user in pwd.getpwall():
                try:
                    # Get user groups
                    groups = [g.gr_name for g in grp.getgrall() if user.pw_name in g.gr_mem]
                    primary_group = grp.getgrgid(user.pw_gid).gr_name
                    if primary_group not in groups:
                        groups.append(primary_group)
                        
                    users.append({
                        "username": user.pw_name,
                        "uid": user.pw_uid,
                        "gid": user.pw_gid,
                        "full_name": user.pw_gecos,
                        "home": user.pw_dir,
                        "shell": user.pw_shell,
                        "groups": groups
                    })
                except Exception as e:
                    self.logger.error(f"Error processing user {user.pw_name}: {str(e)}")
                    continue
                    
            return users
            
        except Exception as e:
            self.logger.error(f"Error getting users: {str(e)}")
            return []
            
    def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a user"""
        try:
            # Get basic user info
            user = pwd.getpwnam(username)
            
            # Get groups
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            primary_group = grp.getgrgid(user.pw_gid).gr_name
            if primary_group not in groups:
                groups.append(primary_group)
                
            # Get login history
            last_login = self._get_last_login(username)
            
            # Get processes
            processes = self._get_user_processes(username)
            
            return {
                "username": user.pw_name,
                "uid": user.pw_uid,
                "gid": user.pw_gid,
                "full_name": user.pw_gecos,
                "home": user.pw_dir,
                "shell": user.pw_shell,
                "groups": groups,
                "last_login": last_login,
                "processes": processes
            }
            
        except KeyError:
            self.logger.error(f"User not found: {username}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting user info: {str(e)}")
            return None
            
    def get_active_users(self) -> List[Dict[str, Any]]:
        """Get currently active users"""
        try:
            # Use who command
            cmd = ["who"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"who failed: {proc.stderr}")
                
            return self._parse_who_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting active users: {str(e)}")
            return []
            
    def get_login_history(self, username: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get user login history"""
        try:
            # Use last command
            cmd = ["last", "-100"]
            if username:
                cmd.append(username)
                
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"last failed: {proc.stderr}")
                
            return self._parse_last_output(proc.stdout, limit)
            
        except Exception as e:
            self.logger.error(f"Error getting login history: {str(e)}")
            return []
            
    def get_failed_logins(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get failed login attempts"""
        try:
            # Use lastb command
            cmd = ["lastb", "-100"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"lastb failed: {proc.stderr}")
                
            return self._parse_last_output(proc.stdout, limit)
            
        except Exception as e:
            self.logger.error(f"Error getting failed logins: {str(e)}")
            return []
            
    def _get_last_login(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user's last login"""
        try:
            history = self.get_login_history(username, 1)
            return history[0] if history else None
            
        except Exception as e:
            self.logger.error(f"Error getting last login: {str(e)}")
            return None
            
    def _get_user_processes(self, username: str) -> List[Dict[str, Any]]:
        """Get processes owned by user"""
        try:
            # Use ps command
            cmd = ["ps", "-u", username, "-o", "pid,ppid,%cpu,%mem,command"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"ps failed: {proc.stderr}")
                
            return self._parse_ps_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting user processes: {str(e)}")
            return []
            
    def _parse_who_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse who command output"""
        users = []
        
        try:
            for line in output.strip().split("\n"):
                if not line:
                    continue
                    
                parts = line.split()
                if len(parts) >= 5:
                    user = {
                        "username": parts[0],
                        "terminal": parts[1],
                        "date": " ".join(parts[2:5])
                    }
                    
                    # Add host if present
                    if len(parts) >= 6:
                        user["host"] = parts[5].strip("()")
                        
                    users.append(user)
                    
        except Exception as e:
            self.logger.error(f"Error parsing who output: {str(e)}")
            
        return users
        
    def _parse_last_output(self, output: str, limit: int) -> List[Dict[str, Any]]:
        """Parse last/lastb command output"""
        logins = []
        count = 0
        
        try:
            for line in output.strip().split("\n"):
                if not line or "wtmp begins" in line:
                    continue
                    
                if count >= limit:
                    break
                    
                parts = line.split()
                if len(parts) >= 9:
                    login = {
                        "username": parts[0],
                        "terminal": parts[1],
                        "host": parts[2] if parts[2] != ":" else None,
                        "date": " ".join(parts[3:8]),
                        "duration": parts[8] if parts[8] != "still" else "active"
                    }
                    logins.append(login)
                    count += 1
                    
        except Exception as e:
            self.logger.error(f"Error parsing last output: {str(e)}")
            
        return logins
        
    def _parse_ps_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse ps command output"""
        processes = []
        
        try:
            lines = output.strip().split("\n")
            if len(lines) < 2:  # Need header and at least one process
                return processes
                
            # Parse header
            headers = lines[0].lower().split()
            
            # Parse processes
            for line in lines[1:]:
                parts = line.split(None, len(headers) - 1)
                if len(parts) >= len(headers):
                    process = {}
                    for i, header in enumerate(headers):
                        # Convert numeric values
                        if header in ["pid", "ppid"]:
                            process[header] = int(parts[i])
                        elif header in ["%cpu", "%mem"]:
                            process[header] = float(parts[i])
                        else:
                            process[header] = parts[i]
                    processes.append(process)
                    
        except Exception as e:
            self.logger.error(f"Error parsing ps output: {str(e)}")
            
        return processes 
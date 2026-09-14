"""
File permissions monitoring module
Handles file permission monitoring and management
"""

import logging
import os
import stat
import pwd
import grp
import subprocess
from typing import Optional, Dict, Any, List, Set
from pathlib import Path

class PermissionsMonitor:
    """Monitor and manage file permissions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_permissions(self, path: str) -> Dict[str, Any]:
        """Get detailed permissions information"""
        try:
            path_obj = Path(path)
            stat_result = path_obj.stat()
            
            # Get owner and group names
            try:
                owner = pwd.getpwuid(stat_result.st_uid).pw_name
            except KeyError:
                owner = str(stat_result.st_uid)
                
            try:
                group = grp.getgrgid(stat_result.st_gid).gr_name
            except KeyError:
                group = str(stat_result.st_gid)
                
            return {
                "mode": stat_result.st_mode,
                "mode_string": stat.filemode(stat_result.st_mode),
                "owner": owner,
                "group": group,
                "owner_id": stat_result.st_uid,
                "group_id": stat_result.st_gid,
                "permissions": {
                    "user": {
                        "read": bool(stat_result.st_mode & stat.S_IRUSR),
                        "write": bool(stat_result.st_mode & stat.S_IWUSR),
                        "execute": bool(stat_result.st_mode & stat.S_IXUSR)
                    },
                    "group": {
                        "read": bool(stat_result.st_mode & stat.S_IRGRP),
                        "write": bool(stat_result.st_mode & stat.S_IWGRP),
                        "execute": bool(stat_result.st_mode & stat.S_IXGRP)
                    },
                    "other": {
                        "read": bool(stat_result.st_mode & stat.S_IROTH),
                        "write": bool(stat_result.st_mode & stat.S_IWOTH),
                        "execute": bool(stat_result.st_mode & stat.S_IXOTH)
                    }
                },
                "special": {
                    "setuid": bool(stat_result.st_mode & stat.S_ISUID),
                    "setgid": bool(stat_result.st_mode & stat.S_ISGID),
                    "sticky": bool(stat_result.st_mode & stat.S_ISVTX)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting permissions: {str(e)}")
            return {}
            
    def get_acl(self, path: str) -> List[Dict[str, Any]]:
        """Get Access Control List entries"""
        try:
            cmd = ["ls", "-le", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"ls failed: {proc.stderr}")
                
            return self._parse_acl_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting ACL: {str(e)}")
            return []
            
    def check_access(self, path: str, user: Optional[str] = None) -> Dict[str, bool]:
        """Check access permissions for current or specified user"""
        try:
            if user:
                # Get user info
                try:
                    user_info = pwd.getpwnam(user)
                    uid = user_info.pw_uid
                    groups = [g.gr_gid for g in grp.getgrall() if user in g.gr_mem]
                    groups.append(user_info.pw_gid)
                except KeyError:
                    raise ValueError(f"User not found: {user}")
            else:
                # Current process user
                uid = os.getuid()
                groups = os.getgroups()
                
            path_obj = Path(path)
            stat_result = path_obj.stat()
            
            # Check if user is owner
            is_owner = stat_result.st_uid == uid
            # Check if user is in group
            in_group = stat_result.st_gid in groups
            
            mode = stat_result.st_mode
            
            return {
                "exists": True,
                "read": (
                    (is_owner and bool(mode & stat.S_IRUSR)) or
                    (in_group and bool(mode & stat.S_IRGRP)) or
                    bool(mode & stat.S_IROTH)
                ),
                "write": (
                    (is_owner and bool(mode & stat.S_IWUSR)) or
                    (in_group and bool(mode & stat.S_IWGRP)) or
                    bool(mode & stat.S_IWOTH)
                ),
                "execute": (
                    (is_owner and bool(mode & stat.S_IXUSR)) or
                    (in_group and bool(mode & stat.S_IXGRP)) or
                    bool(mode & stat.S_IXOTH)
                )
            }
            
        except FileNotFoundError:
            return {"exists": False, "read": False, "write": False, "execute": False}
        except Exception as e:
            self.logger.error(f"Error checking access: {str(e)}")
            return {"exists": True, "read": False, "write": False, "execute": False}
            
    def scan_directory_permissions(self, 
                                 directory: str,
                                 recursive: bool = True,
                                 check_patterns: Optional[List[Dict[str, Any]]] = None
                                 ) -> Dict[str, Any]:
        """Scan directory for permission issues"""
        results = {
            "scanned": 0,
            "issues": [],
            "errors": []
        }
        
        try:
            path_obj = Path(directory)
            if not path_obj.is_dir():
                raise ValueError(f"Not a directory: {directory}")
                
            # Get list of files
            if recursive:
                files = path_obj.rglob("*")
            else:
                files = path_obj.glob("*")
                
            # Process each file
            for file_path in files:
                try:
                    results["scanned"] += 1
                    perms = self.get_permissions(str(file_path))
                    
                    # Check against patterns if provided
                    if check_patterns:
                        for pattern in check_patterns:
                            if self._check_permission_pattern(perms, pattern):
                                results["issues"].append({
                                    "path": str(file_path),
                                    "permissions": perms,
                                    "pattern": pattern
                                })
                                
                except Exception as e:
                    results["errors"].append({
                        "path": str(file_path),
                        "error": str(e)
                    })
                    
        except Exception as e:
            self.logger.error(f"Error scanning directory permissions: {str(e)}")
            
        return results
        
    def _parse_acl_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse ACL command output"""
        entries = []
        
        try:
            lines = output.strip().split("\n")
            for line in lines:
                if line.startswith(" "):  # ACL entry
                    parts = line.strip().split(":")
                    if len(parts) >= 3:
                        entry = {
                            "type": parts[0],
                            "name": parts[1],
                            "permissions": parts[2]
                        }
                        entries.append(entry)
                        
        except Exception as e:
            self.logger.error(f"Error parsing ACL output: {str(e)}")
            
        return entries
        
    def _check_permission_pattern(self, perms: Dict[str, Any], pattern: Dict[str, Any]) -> bool:
        """Check if permissions match a pattern"""
        try:
            # Check each condition in pattern
            for key, value in pattern.items():
                if key == "min_mode":
                    if perms["mode"] & value != value:
                        return True
                elif key == "max_mode":
                    if perms["mode"] & ~value != 0:
                        return True
                elif key == "owner":
                    if perms["owner"] == value:
                        return True
                elif key == "group":
                    if perms["group"] == value:
                        return True
                elif key == "world_writable":
                    if value and perms["permissions"]["other"]["write"]:
                        return True
                elif key == "setuid":
                    if value and perms["special"]["setuid"]:
                        return True
                elif key == "setgid":
                    if value and perms["special"]["setgid"]:
                        return True
                        
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking permission pattern: {str(e)}")
            return False 
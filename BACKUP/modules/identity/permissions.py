"""
Permission management module
Handles user and group permission management
"""

import logging
import pwd
import grp
import os
import stat
import subprocess
from typing import Optional, Dict, Any, List, Set
from pathlib import Path

class PermissionManager:
    """Manage user and group permissions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def check_user_permission(self, username: str, path: str) -> Dict[str, bool]:
        """Check user's permissions for a path"""
        try:
            # Get user info
            user = pwd.getpwnam(username)
            
            # Get user's groups
            groups = [g.gr_gid for g in grp.getgrall() if username in g.gr_mem]
            groups.append(user.pw_gid)
            
            # Get file info
            path_obj = Path(path)
            if not path_obj.exists():
                return {
                    "exists": False,
                    "read": False,
                    "write": False,
                    "execute": False
                }
                
            stat_result = path_obj.stat()
            
            # Check if user is owner
            is_owner = stat_result.st_uid == user.pw_uid
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
            
        except KeyError:
            self.logger.error(f"User not found: {username}")
            return {"exists": False, "read": False, "write": False, "execute": False}
        except Exception as e:
            self.logger.error(f"Error checking permissions: {str(e)}")
            return {"exists": True, "read": False, "write": False, "execute": False}
            
    def get_user_capabilities(self, username: str) -> Dict[str, Any]:
        """Get user's system capabilities"""
        try:
            # Get user info
            user = pwd.getpwnam(username)
            
            # Get groups
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            primary_group = grp.getgrgid(user.pw_gid).gr_name
            if primary_group not in groups:
                groups.append(primary_group)
                
            # Check sudo access
            sudo_access = self._check_sudo_access(username)
            
            # Check admin group membership
            admin_groups = {"admin", "sudo", "wheel", "staff"}
            is_admin = bool(admin_groups.intersection(groups))
            
            return {
                "uid": user.pw_uid,
                "is_root": user.pw_uid == 0,
                "primary_group": primary_group,
                "groups": groups,
                "is_admin": is_admin,
                "sudo_access": sudo_access,
                "home_directory": user.pw_dir,
                "shell": user.pw_shell
            }
            
        except KeyError:
            self.logger.error(f"User not found: {username}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting capabilities: {str(e)}")
            return {}
            
    def get_group_permissions(self, group: str, path: str) -> Dict[str, bool]:
        """Check group's permissions for a path"""
        try:
            # Get group info
            group_info = grp.getgrnam(group)
            
            # Get file info
            path_obj = Path(path)
            if not path_obj.exists():
                return {
                    "exists": False,
                    "read": False,
                    "write": False,
                    "execute": False
                }
                
            stat_result = path_obj.stat()
            
            # Check if path belongs to group
            is_group = stat_result.st_gid == group_info.gr_gid
            
            mode = stat_result.st_mode
            
            return {
                "exists": True,
                "read": is_group and bool(mode & stat.S_IRGRP),
                "write": is_group and bool(mode & stat.S_IWGRP),
                "execute": is_group and bool(mode & stat.S_IXGRP)
            }
            
        except KeyError:
            self.logger.error(f"Group not found: {group}")
            return {"exists": False, "read": False, "write": False, "execute": False}
        except Exception as e:
            self.logger.error(f"Error checking group permissions: {str(e)}")
            return {"exists": True, "read": False, "write": False, "execute": False}
            
    def scan_user_permissions(self, 
                            username: str,
                            paths: List[str]
                            ) -> Dict[str, Dict[str, bool]]:
        """Scan multiple paths for user permissions"""
        results = {}
        
        try:
            for path in paths:
                try:
                    results[path] = self.check_user_permission(username, path)
                except Exception as e:
                    self.logger.error(f"Error checking {path}: {str(e)}")
                    results[path] = {
                        "exists": False,
                        "read": False,
                        "write": False,
                        "execute": False,
                        "error": str(e)
                    }
                    
        except Exception as e:
            self.logger.error(f"Error scanning permissions: {str(e)}")
            
        return results
        
    def get_effective_permissions(self, 
                                username: str,
                                path: str
                                ) -> Dict[str, Any]:
        """Get effective permissions including ACLs"""
        try:
            # Get basic permissions
            basic_perms = self.check_user_permission(username, path)
            
            # Get ACL permissions
            acl_perms = self._get_acl_permissions(username, path)
            
            # Get extended attributes
            xattrs = self._get_extended_attributes(path)
            
            return {
                "basic": basic_perms,
                "acl": acl_perms,
                "xattr": xattrs
            }
            
        except Exception as e:
            self.logger.error(f"Error getting effective permissions: {str(e)}")
            return {}
            
    def _check_sudo_access(self, username: str) -> bool:
        """Check if user has sudo access"""
        try:
            # Check sudo group membership
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            return "sudo" in groups or "admin" in groups or "wheel" in groups
            
        except Exception as e:
            self.logger.error(f"Error checking sudo access: {str(e)}")
            return False
            
    def _get_acl_permissions(self, username: str, path: str) -> Dict[str, bool]:
        """Get ACL permissions for path"""
        try:
            cmd = ["ls", "-le", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                return {"read": False, "write": False, "execute": False}
                
            return self._parse_acl_output(proc.stdout, username)
            
        except Exception as e:
            self.logger.error(f"Error getting ACL permissions: {str(e)}")
            return {"read": False, "write": False, "execute": False}
            
    def _get_extended_attributes(self, path: str) -> List[str]:
        """Get extended attributes of path"""
        try:
            cmd = ["xattr", "-l", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                return []
                
            return [line.strip() for line in proc.stdout.split("\n") if line.strip()]
            
        except Exception as e:
            self.logger.error(f"Error getting extended attributes: {str(e)}")
            return []
            
    def _parse_acl_output(self, output: str, username: str) -> Dict[str, bool]:
        """Parse ACL command output"""
        perms = {"read": False, "write": False, "execute": False}
        
        try:
            for line in output.split("\n"):
                if line.strip().startswith(f"user:{username}:"):
                    perm_str = line.split(":")[-1].strip()
                    perms["read"] = "r" in perm_str
                    perms["write"] = "w" in perm_str
                    perms["execute"] = "x" in perm_str
                    break
                    
        except Exception as e:
            self.logger.error(f"Error parsing ACL output: {str(e)}")
            
        return perms 
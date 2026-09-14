"""
Storage monitoring module
Handles disk and volume monitoring
"""

import logging
import subprocess
import json
from typing import Optional, Dict, Any, List
from pathlib import Path

class StorageMonitor:
    """Monitor disk and volume storage"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_volumes(self) -> List[Dict[str, Any]]:
        """Get list of mounted volumes"""
        try:
            # Use diskutil list for volume info
            cmd = ["diskutil", "list", "-plist"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"diskutil failed: {proc.stderr}")
                
            # Parse plist output
            volumes = []
            plist = self._parse_plist(proc.stdout)
            
            # Get detailed info for each disk
            for disk in plist.get("AllDisksAndPartitions", []):
                disk_info = self._get_disk_info(disk["DeviceIdentifier"])
                if disk_info:
                    volumes.append(disk_info)
                    
            return volumes
            
        except Exception as e:
            self.logger.error(f"Error getting volumes: {str(e)}")
            return []
            
    def get_volume_info(self, volume: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a volume"""
        try:
            # Use diskutil info for volume info
            cmd = ["diskutil", "info", "-plist", volume]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"diskutil failed: {proc.stderr}")
                
            return self._parse_plist(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting volume info: {str(e)}")
            return None
            
    def get_storage_usage(self, path: str = "/") -> Dict[str, Any]:
        """Get storage usage information"""
        try:
            # Use df for storage info
            cmd = ["df", "-h", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"df failed: {proc.stderr}")
                
            return self._parse_df_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting storage usage: {str(e)}")
            return {}
            
    def get_directory_size(self, path: str) -> Dict[str, Any]:
        """Get directory size information"""
        try:
            # Use du for directory size
            cmd = ["du", "-sh", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"du failed: {proc.stderr}")
                
            return self._parse_du_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting directory size: {str(e)}")
            return {}
            
    def get_volume_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all volumes"""
        try:
            stats = {}
            
            # Get list of volumes
            volumes = self.get_volumes()
            
            # Get stats for each volume
            for volume in volumes:
                identifier = volume.get("DeviceIdentifier")
                if identifier:
                    mount_point = volume.get("MountPoint")
                    if mount_point:
                        stats[identifier] = {
                            "info": volume,
                            "usage": self.get_storage_usage(mount_point)
                        }
                        
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting volume stats: {str(e)}")
            return {}
            
    def _get_disk_info(self, disk_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed disk information"""
        try:
            cmd = ["diskutil", "info", "-plist", disk_id]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                return None
                
            return self._parse_plist(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting disk info: {str(e)}")
            return None
            
    def _parse_plist(self, plist_str: str) -> Dict[str, Any]:
        """Parse property list output"""
        try:
            # Convert plist to JSON
            cmd = ["plutil", "-convert", "json", "-o", "-", "-"]
            
            proc = subprocess.run(
                cmd,
                input=plist_str.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if proc.returncode != 0:
                raise Exception(f"plutil failed: {proc.stderr.decode()}")
                
            return json.loads(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error parsing plist: {str(e)}")
            return {}
            
    def _parse_df_output(self, output: str) -> Dict[str, Any]:
        """Parse df command output"""
        try:
            lines = output.strip().split("\n")
            if len(lines) < 2:
                return {}
                
            # Parse header
            headers = lines[0].lower().split()
            
            # Parse values
            values = lines[1].split()
            
            if len(headers) == len(values):
                return dict(zip(headers, values))
                
            return {}
            
        except Exception as e:
            self.logger.error(f"Error parsing df output: {str(e)}")
            return {}
            
    def _parse_du_output(self, output: str) -> Dict[str, Any]:
        """Parse du command output"""
        try:
            parts = output.strip().split()
            if len(parts) >= 2:
                return {
                    "size": parts[0],
                    "path": parts[1]
                }
                
            return {}
            
        except Exception as e:
            self.logger.error(f"Error parsing du output: {str(e)}")
            return {} 
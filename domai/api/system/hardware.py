"""
Hardware monitoring module
"""

import logging
import subprocess
import json
from typing import Optional, Dict, Any, List
from pathlib import Path

class HardwareMonitor:
    """Monitor system hardware"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_system_info(self) -> Dict[str, Any]:
        """Get system hardware information"""
        try:
            # Use system_profiler for hardware info
            cmd = ["system_profiler", "SPHardwareDataType", "-json"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return json.loads(proc.stdout)["SPHardwareDataType"][0]
            
        except Exception as e:
            self.logger.error(f"Error getting system info: {str(e)}")
            return {}
            
    def get_temperature(self) -> Dict[str, float]:
        """Get temperature sensors data"""
        try:
            # Use osx-cpu-temp for temperature
            cmd = ["osx-cpu-temp", "-j"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return json.loads(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting temperature: {str(e)}")
            return {}
            
    def get_power_info(self) -> Dict[str, Any]:
        """Get power and battery information"""
        try:
            # Use system_profiler for power info
            cmd = ["system_profiler", "SPPowerDataType", "-json"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return json.loads(proc.stdout)["SPPowerDataType"][0]
            
        except Exception as e:
            self.logger.error(f"Error getting power info: {str(e)}")
            return {}
            
    def get_disk_info(self) -> List[Dict[str, Any]]:
        """Get disk and storage information"""
        try:
            # Use diskutil for disk info
            cmd = ["diskutil", "list", "-plist"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            disks = []
            plist = self._parse_plist(proc.stdout)
            
            # Get detailed info for each disk
            for disk in plist.get("AllDisksAndPartitions", []):
                disk_info = self._get_disk_details(disk["DeviceIdentifier"])
                if disk_info:
                    disks.append(disk_info)
                    
            return disks
            
        except Exception as e:
            self.logger.error(f"Error getting disk info: {str(e)}")
            return []
            
    def get_memory_pressure(self) -> Dict[str, Any]:
        """Get memory pressure statistics"""
        try:
            # Use memory_pressure command
            cmd = ["memory_pressure"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_memory_pressure(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting memory pressure: {str(e)}")
            return {}
            
    def _get_disk_details(self, disk_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific disk"""
        try:
            # Use diskutil info for detailed disk info
            cmd = ["diskutil", "info", "-plist", disk_id]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_plist(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting disk details: {str(e)}")
            return None
            
    def _parse_plist(self, plist_str: str) -> Dict[str, Any]:
        """Parse property list output"""
        try:
            # Convert plist to JSON format
            cmd = ["plutil", "-convert", "json", "-o", "-", "-"]
            
            proc = subprocess.run(
                cmd,
                input=plist_str.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if proc.returncode != 0:
                return {}
                
            return json.loads(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error parsing plist: {str(e)}")
            return {}
            
    def _parse_memory_pressure(self, output: str) -> Dict[str, Any]:
        """Parse memory_pressure command output"""
        pressure = {
            "system": {},
            "levels": {}
        }
        
        current_section = None
        
        for line in output.split("\n"):
            line = line.strip()
            
            if not line:
                continue
                
            # Detect sections
            if "System-wide memory pressure:" in line:
                current_section = "system"
                continue
            elif "Memory pressure level:" in line:
                current_section = "levels"
                continue
                
            # Parse values
            if current_section and ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                
                # Try to convert percentages
                if "%" in value:
                    try:
                        value = float(value.replace("%", ""))
                    except ValueError:
                        pass
                        
                if current_section == "system":
                    pressure["system"][key] = value
                else:
                    pressure["levels"][key] = value
                    
        return pressure 
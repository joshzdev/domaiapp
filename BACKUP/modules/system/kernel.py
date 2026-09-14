"""
Kernel monitoring and management module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class KernelMonitor:
    """Monitor kernel parameters and system messages"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_kernel_info(self) -> Dict[str, Any]:
        """Get kernel information"""
        try:
            # Use sysctl for kernel info
            cmd = ["sysctl", "-a"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_sysctl_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting kernel info: {str(e)}")
            return {}
            
    def get_system_messages(self, lines: int = 100) -> List[Dict[str, Any]]:
        """Get recent system messages"""
        try:
            # Use dmesg for system messages
            cmd = ["dmesg"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_dmesg_output(proc.stdout, lines)
            
        except Exception as e:
            self.logger.error(f"Error getting system messages: {str(e)}")
            return []
            
    def get_kernel_extensions(self) -> List[Dict[str, Any]]:
        """Get loaded kernel extensions"""
        try:
            # Use kextstat for kernel extensions
            cmd = ["kextstat"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_kextstat_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting kernel extensions: {str(e)}")
            return []
            
    def get_boot_args(self) -> Dict[str, str]:
        """Get boot arguments"""
        try:
            # Use nvram for boot args
            cmd = ["nvram", "boot-args"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_nvram_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting boot args: {str(e)}")
            return {}
            
    def _parse_sysctl_output(self, output: str) -> Dict[str, Any]:
        """Parse sysctl command output"""
        info = {}
        
        for line in output.split("\n"):
            if ":" in line:
                try:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Try to convert numeric values
                    try:
                        if "." in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                        
                    info[key] = value
                except Exception as e:
                    self.logger.error(f"Error parsing sysctl line: {str(e)}")
                    continue
                    
        return info
        
    def _parse_dmesg_output(self, output: str, limit: int) -> List[Dict[str, Any]]:
        """Parse dmesg command output"""
        messages = []
        
        for line in output.split("\n")[-limit:]:
            if not line.strip():
                continue
                
            try:
                # Parse timestamp and message
                parts = line.split(None, 1)
                if len(parts) >= 2:
                    messages.append({
                        "timestamp": parts[0],
                        "message": parts[1]
                    })
            except Exception as e:
                self.logger.error(f"Error parsing dmesg line: {str(e)}")
                continue
                
        return messages
        
    def _parse_kextstat_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse kextstat command output"""
        extensions = []
        
        for line in output.split("\n")[1:]:  # Skip header
            if not line.strip():
                continue
                
            try:
                parts = line.split()
                if len(parts) >= 6:
                    extension = {
                        "index": int(parts[0]),
                        "refs": int(parts[1]),
                        "address": parts[2],
                        "size": parts[3],
                        "wired": parts[4],
                        "name": parts[5]
                    }
                    
                    # Add version if present
                    if len(parts) > 6:
                        extension["version"] = parts[6].strip("()")
                        
                    extensions.append(extension)
            except Exception as e:
                self.logger.error(f"Error parsing kextstat line: {str(e)}")
                continue
                
        return extensions
        
    def _parse_nvram_output(self, output: str) -> Dict[str, str]:
        """Parse nvram command output"""
        args = {}
        
        if "boot-args" in output:
            try:
                # Extract boot args
                value = output.split("boot-args", 1)[1].strip()
                
                # Parse individual arguments
                for arg in value.split():
                    if "=" in arg:
                        key, val = arg.split("=", 1)
                        args[key] = val
                    else:
                        args[arg] = ""
                        
            except Exception as e:
                self.logger.error(f"Error parsing boot args: {str(e)}")
                
        return args
``` 
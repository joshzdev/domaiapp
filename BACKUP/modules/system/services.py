"""
System services monitoring module
Handles launchctl service monitoring and management
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class ServiceMonitor:
    """Monitor and manage system services via launchctl"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def list_services(self) -> List[Dict[str, Any]]:
        """List all services"""
        try:
            # Use launchctl list for service info
            cmd = ["launchctl", "list"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_service_list(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error listing services: {str(e)}")
            return []
            
    def get_service_info(self, label: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific service"""
        try:
            # Use launchctl print for detailed info
            cmd = ["launchctl", "print", label]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_service_info(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting service info: {str(e)}")
            return None
            
    def get_service_status(self, label: str) -> Dict[str, Any]:
        """Get current status of a service"""
        try:
            # Use launchctl print for status
            cmd = ["launchctl", "print", label]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_service_status(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting service status: {str(e)}")
            return {"status": "error", "error": str(e)}
            
    def find_service_plist(self, label: str) -> Optional[Path]:
        """Find plist file for a service"""
        try:
            # Common plist locations
            locations = [
                Path("/Library/LaunchDaemons"),
                Path("/Library/LaunchAgents"),
                Path.home() / "Library/LaunchAgents",
                Path("/System/Library/LaunchDaemons"),
                Path("/System/Library/LaunchAgents")
            ]
            
            for location in locations:
                if not location.exists():
                    continue
                    
                plist = location / f"{label}.plist"
                if plist.exists():
                    return plist
                    
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding service plist: {str(e)}")
            return None
            
    def _parse_service_list(self, output: str) -> List[Dict[str, Any]]:
        """Parse launchctl list output"""
        services = []
        
        try:
            lines = output.strip().split("\n")
            
            for line in lines[1:]:  # Skip header
                if not line.strip():
                    continue
                    
                parts = line.split()
                if len(parts) >= 3:
                    service = {
                        "pid": parts[0] if parts[0] != "-" else None,
                        "status": parts[1],
                        "label": " ".join(parts[2:])
                    }
                    services.append(service)
                    
        except Exception as e:
            self.logger.error(f"Error parsing service list: {str(e)}")
            
        return services
        
    def _parse_service_info(self, output: str) -> Dict[str, Any]:
        """Parse service info output"""
        info = {
            "state": {},
            "config": {}
        }
        
        try:
            current_section = None
            
            for line in output.split("\n"):
                line = line.strip()
                if not line:
                    continue
                    
                if line.endswith(":"):
                    current_section = line[:-1].lower()
                    info[current_section] = {}
                elif "=" in line and current_section:
                    key, value = line.split("=", 1)
                    info[current_section][key.strip()] = value.strip()
                    
        except Exception as e:
            self.logger.error(f"Error parsing service info: {str(e)}")
            
        return info
        
    def _parse_service_status(self, output: str) -> Dict[str, Any]:
        """Parse service status output"""
        status = {
            "status": "unknown",
            "pid": None,
            "exit_code": None
        }
        
        try:
            for line in output.split("\n"):
                line = line.strip()
                
                if "state = running" in line.lower():
                    status["status"] = "running"
                elif "state = waiting" in line.lower():
                    status["status"] = "waiting"
                elif "state = stopped" in line.lower():
                    status["status"] = "stopped"
                    
                if "pid =" in line.lower():
                    try:
                        status["pid"] = int(line.split("=")[1].strip())
                    except (ValueError, IndexError):
                        pass
                        
                if "last exit code =" in line.lower():
                    try:
                        status["exit_code"] = int(line.split("=")[1].strip())
                    except (ValueError, IndexError):
                        pass
                        
        except Exception as e:
            self.logger.error(f"Error parsing service status: {str(e)}")
            
        return status
</rewritten_file> 
"""
Network services monitoring module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class ServiceMonitor:
    """Monitor network services and daemons"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_listening_services(self) -> List[Dict[str, Any]]:
        """Get all network services listening for connections"""
        try:
            # Use lsof to get listening services
            cmd = ["lsof", "-i", "-P", "-n"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_listening_services(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"lsof failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting listening services: {str(e)}")
            return []
            
    def get_service_info(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific service"""
        try:
            # First check launchctl for the service
            cmd = ["launchctl", "list"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            services = self._parse_launchctl_output(proc.stdout)
            service = next((s for s in services if service_name in s["name"]), None)
            
            if service:
                # Get process info if running
                if service["pid"] > 0:
                    service["connections"] = self._get_process_connections(service["pid"])
                    service["ports"] = self._get_process_ports(service["pid"])
                    
            return service
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"launchctl failed: {e.stderr}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting service info: {str(e)}")
            return None
            
    def get_active_services(self) -> List[Dict[str, Any]]:
        """Get all active network services"""
        try:
            # Combine launchctl and netstat info
            services = []
            
            # Get launchctl services
            cmd = ["launchctl", "list"]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            launchd_services = self._parse_launchctl_output(proc.stdout)
            
            # Get network info for running services
            for service in launchd_services:
                if service["pid"] > 0:  # If service is running
                    service["connections"] = self._get_process_connections(service["pid"])
                    service["ports"] = self._get_process_ports(service["pid"])
                    if service["connections"] or service["ports"]:
                        services.append(service)
                        
            return services
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"launchctl failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting active services: {str(e)}")
            return []
            
    def _parse_listening_services(self, output: str) -> List[Dict[str, Any]]:
        """Parse lsof output for listening services"""
        services = []
        
        for line in output.split("\n")[1:]:  # Skip header
            if "LISTEN" in line:
                try:
                    parts = line.split()
                    if len(parts) >= 9:
                        service = {
                            "name": parts[0],
                            "pid": int(parts[1]),
                            "user": parts[2],
                            "protocol": parts[4],
                            "address": parts[8],
                            "state": "LISTENING"
                        }
                        services.append(service)
                except Exception as e:
                    self.logger.error(f"Error parsing service line: {str(e)}")
                    continue
                    
        return services
        
    def _parse_launchctl_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse launchctl list output"""
        services = []
        
        for line in output.split("\n")[1:]:  # Skip header
            try:
                parts = line.split()
                if len(parts) >= 3:
                    service = {
                        "pid": int(parts[0]) if parts[0] != "-" else 0,
                        "status": int(parts[1]) if parts[1] != "-" else 0,
                        "name": parts[2],
                        "connections": [],
                        "ports": []
                    }
                    services.append(service)
            except Exception as e:
                self.logger.error(f"Error parsing launchctl line: {str(e)}")
                continue
                
        return services
        
    def _get_process_connections(self, pid: int) -> List[Dict[str, Any]]:
        """Get network connections for a specific process"""
        try:
            cmd = ["lsof", "-i", "-a", "-p", str(pid), "-n", "-P"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            connections = []
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    try:
                        parts = line.split()
                        if len(parts) >= 9:
                            conn = {
                                "protocol": parts[4],
                                "address": parts[8],
                                "state": parts[9] if len(parts) > 9 else "UNKNOWN"
                            }
                            connections.append(conn)
                    except Exception as e:
                        self.logger.error(f"Error parsing connection: {str(e)}")
                        continue
                        
            return connections
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting process connections: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting process connections: {str(e)}")
            return []
            
    def _get_process_ports(self, pid: int) -> List[int]:
        """Get ports used by a specific process"""
        try:
            cmd = ["lsof", "-i", "-a", "-p", str(pid), "-n", "-P"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            ports = set()
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    try:
                        parts = line.split()
                        if len(parts) >= 9:
                            # Extract port from address field
                            addr = parts[8]
                            if ":" in addr:
                                port = int(addr.split(":")[-1])
                                ports.add(port)
                    except Exception as e:
                        self.logger.error(f"Error parsing port: {str(e)}")
                        continue
                        
            return sorted(list(ports))
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting process ports: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting process ports: {str(e)}")
            return []
</rewritten_file> 
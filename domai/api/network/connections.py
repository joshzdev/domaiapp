"""
Network connection monitoring module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
#from pathlib import Path

class ConnectionMonitor:
    """Monitor network connections using native tools"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_connections(
        self,
        port: Optional[int] = None,
        protocol: Optional[str] = None,
        state: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get current network connections"""
        try:
            # Use netstat for connection info
            cmd = ["netstat", "-an"]
            if protocol:
                if protocol.lower() == "tcp":
                    cmd.append("-p tcp")
                elif protocol.lower() == "udp":
                    cmd.append("-p udp")
                    
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse connections
            connections = []
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    conn = self._parse_netstat_line(line)
                    if conn:
                        # Apply filters
                        if port and conn.get("local_port") != port and conn.get("remote_port") != port:
                            continue
                        if state and conn.get("state") != state:
                            continue
                        connections.append(conn)
                        
            return connections
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting connections: {str(e)}")
            return []
            
    def get_listening_ports(self) -> List[Dict[str, Any]]:
        """Get listening ports"""
        try:
            # Use lsof for listening ports
            cmd = ["lsof", "-i", "-n", "-P"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse listening ports
            listening = []
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if "LISTEN" in line:
                    port = self._parse_lsof_line(line)
                    if port:
                        listening.append(port)
                        
            return listening
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"lsof failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting listening ports: {str(e)}")
            return []
            
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        try:
            # Use netstat for statistics
            cmd = ["netstat", "-s"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse statistics
            return self._parse_netstat_stats(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting connection stats: {str(e)}")
            return {}
            
    def _parse_netstat_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single netstat output line"""
        try:
            parts = line.split()
            if len(parts) < 4:
                return None
                
            # Parse local and remote addresses
            local = parts[3]
            remote = parts[4] if len(parts) > 4 else ""
            
            local_parts = local.rsplit(".", 1)
            local_addr = local_parts[0]
            local_port = int(local_parts[1]) if len(local_parts) > 1 else None
            
            remote_parts = remote.rsplit(".", 1)
            remote_addr = remote_parts[0]
            remote_port = int(remote_parts[1]) if len(remote_parts) > 1 else None
            
            return {
                "protocol": parts[0],
                "local_addr": local_addr,
                "local_port": local_port,
                "remote_addr": remote_addr,
                "remote_port": remote_port,
                "state": parts[5] if len(parts) > 5 else None
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing netstat line: {str(e)}")
            return None
            
    def _parse_lsof_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single lsof output line"""
        try:
            parts = line.split()
            if len(parts) < 8:
                return None
                
            # Parse address and port
            addr_port = parts[8]
            addr_parts = addr_port.rsplit(":", 1)
            
            return {
                "command": parts[0],
                "pid": int(parts[1]),
                "user": parts[2],
                "fd": parts[3],
                "type": parts[4],
                "address": addr_parts[0],
                "port": int(addr_parts[1])
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing lsof line: {str(e)}")
            return None
            
    def _parse_netstat_stats(self, output: str) -> Dict[str, Any]:
        """Parse netstat statistics output"""
        stats = {
            "tcp": {},
            "udp": {},
            "ip": {},
            "icmp": {}
        }
        
        current_section = None
        
        for line in output.split("\n"):
            line = line.strip()
            
            if not line:
                continue
                
            # Detect section
            if "tcp:" in line.lower():
                current_section = "tcp"
                continue
            elif "udp:" in line.lower():
                current_section = "udp"
                continue
            elif "ip:" in line.lower():
                current_section = "ip"
                continue
            elif "icmp:" in line.lower():
                current_section = "icmp"
                continue
                
            if current_section and ":" in line:
                key, value = line.split(":", 1)
                try:
                    # Extract numeric value
                    value = int(''.join(filter(str.isdigit, value)))
                    stats[current_section][key.strip()] = value
                except ValueError:
                    continue
                    
        return stats 
"""
Network statistics monitoring module
"""

import logging
import subprocess
import re
import threading
from queue import Queue
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

class NetworkStats:
    """Monitor network interface statistics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.monitor_thread = None
        self.should_monitor = False
        self.stats_queue = Queue()
        
    def get_interface_stats(self, interface: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Get statistics for network interfaces"""
        try:
            # Use netstat for interface stats
            cmd = ["netstat", "-I"]
            if interface:
                cmd.append(interface)
            else:
                cmd.append("all")  # All interfaces
                
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_interface_stats(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting interface stats: {str(e)}")
            return {}
            
    def get_bandwidth_usage(self, interface: Optional[str] = None) -> Dict[str, Dict[str, float]]:
        """Get current bandwidth usage"""
        try:
            # Use nettop for bandwidth monitoring
            cmd = ["nettop", "-P", "-L", "1", "-n"]
            if interface:
                cmd.extend(["-d", interface])
                
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_bandwidth_usage(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"nettop failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting bandwidth usage: {str(e)}")
            return {}
            
    def get_protocol_stats(self) -> Dict[str, Dict[str, int]]:
        """Get protocol-specific statistics"""
        try:
            # Use netstat for protocol stats
            cmd = ["netstat", "-s"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_protocol_stats(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting protocol stats: {str(e)}")
            return {}
            
    def get_error_stats(self) -> Dict[str, Dict[str, int]]:
        """Get network error statistics"""
        try:
            # Use netstat for error stats
            cmd = ["netstat", "-s"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_error_stats(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting error stats: {str(e)}")
            return {}
            
    def start_monitoring(
        self,
        interface: Optional[str] = None,
        interval: int = 5,
        callback: Optional[callable] = None
    ) -> None:
        """Start continuous network monitoring"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            raise RuntimeError("Monitoring already running")
            
        self.should_monitor = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interface, interval, callback),
            daemon=True
        )
        self.monitor_thread.start()
        
    def stop_monitoring(self) -> None:
        """Stop continuous monitoring"""
        self.should_monitor = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            self.monitor_thread = None
            
    def _monitor_loop(
        self,
        interface: Optional[str],
        interval: int,
        callback: Optional[callable]
    ) -> None:
        """Background monitoring loop"""
        while self.should_monitor:
            try:
                stats = {
                    "interface": self.get_interface_stats(interface),
                    "bandwidth": self.get_bandwidth_usage(interface),
                    "protocol": self.get_protocol_stats(),
                    "errors": self.get_error_stats()
                }
                
                if callback:
                    callback(stats)
                else:
                    self.stats_queue.put(stats)
                    
            except Exception as e:
                self.logger.error(f"Monitoring error: {str(e)}")
            finally:
                # Sleep for interval
                for _ in range(interval):
                    if not self.should_monitor:
                        break
                    threading.Event().wait(1)
            
    def _parse_interface_stats(self, output: str) -> Dict[str, Dict[str, Any]]:
        """Parse netstat interface statistics"""
        stats = {}
        current_interface = None
        
        lines = output.split("\n")
        if len(lines) < 2:  # Need at least header and one interface
            return stats
            
        # Get header fields
        headers = [h.lower() for h in lines[0].split()]
        
        # Parse each interface line
        for line in lines[1:]:
            if not line.strip():
                continue
                
            parts = line.split()
            if len(parts) >= len(headers):
                interface = parts[0]
                stats[interface] = {}
                
                # Map values to headers
                for i, header in enumerate(headers[1:], 1):
                    try:
                        stats[interface][header] = int(parts[i])
                    except ValueError:
                        stats[interface][header] = parts[i]
                        
        return stats
        
    def _parse_bandwidth_usage(self, output: str) -> Dict[str, Dict[str, float]]:
        """Parse nettop bandwidth output"""
        usage = {}
        
        for line in output.split("\n"):
            if not line.strip() or "." not in line:  # Skip headers and empty lines
                continue
                
            try:
                parts = line.split()
                if len(parts) >= 3:
                    process = parts[0]
                    if process not in usage:
                        usage[process] = {"in": 0.0, "out": 0.0}
                        
                    # Parse bandwidth values
                    for i, value in enumerate(parts[1:3]):
                        try:
                            # Convert to bytes/sec
                            num = float(re.findall(r'[\d.]+', value)[0])
                            unit = re.findall(r'[A-Za-z]+', value)[0].upper()
                            
                            if unit.startswith('K'):
                                num *= 1024
                            elif unit.startswith('M'):
                                num *= 1024 * 1024
                            elif unit.startswith('G'):
                                num *= 1024 * 1024 * 1024
                                
                            if i == 0:
                                usage[process]["in"] = num
                            else:
                                usage[process]["out"] = num
                        except (ValueError, IndexError):
                            continue
                            
            except Exception as e:
                self.logger.error(f"Error parsing bandwidth line: {str(e)}")
                continue
                
        return usage
        
    def _parse_protocol_stats(self, output: str) -> Dict[str, Dict[str, int]]:
        """Parse protocol statistics"""
        stats = {
            "tcp": {},
            "udp": {},
            "ip": {},
            "icmp": {}
        }
        
        current_protocol = None
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            # Detect protocol section
            lower_line = line.lower()
            if "tcp:" in lower_line:
                current_protocol = "tcp"
                continue
            elif "udp:" in lower_line:
                current_protocol = "udp"
                continue
            elif "ip:" in lower_line:
                current_protocol = "ip"
                continue
            elif "icmp:" in lower_line:
                current_protocol = "icmp"
                continue
                
            # Parse stats within current protocol section
            if current_protocol and ":" in line:
                key, value = line.split(":", 1)
                try:
                    # Extract numeric value
                    num = int(''.join(filter(str.isdigit, value)))
                    stats[current_protocol][key.strip()] = num
                except ValueError:
                    continue
                    
        return stats
        
    def _parse_error_stats(self, output: str) -> Dict[str, Dict[str, int]]:
        """Parse error statistics"""
        errors = {
            "tcp": {},
            "udp": {},
            "ip": {},
            "interface": {}
        }
        
        current_section = None
        error_keywords = ["error", "drop", "timeout", "fail", "invalid", "reset"]
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            # Detect section
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in error_keywords):
                try:
                    if "tcp:" in lower_line:
                        current_section = "tcp"
                    elif "udp:" in lower_line:
                        current_section = "udp"
                    elif "ip:" in lower_line:
                        current_section = "ip"
                    else:
                        current_section = "interface"
                        
                    if ":" in line:
                        key, value = line.split(":", 1)
                        try:
                            # Extract numeric value
                            num = int(''.join(filter(str.isdigit, value)))
                            errors[current_section][key.strip()] = num
                        except ValueError:
                            continue
                            
                except Exception as e:
                    self.logger.error(f"Error parsing error stats line: {str(e)}")
                    continue
                    
        return errors

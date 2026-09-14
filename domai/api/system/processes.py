"""
Process monitoring and management module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class ProcessMonitor:
    """Monitor system processes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_processes(self, user: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get running processes"""
        try:
            # Use ps for process info
            cmd = ["ps", "-ax", "-o", "pid,ppid,user,%cpu,%mem,state,lstart,command"]
            if user:
                cmd.extend(["-u", user])
                
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_ps_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting processes: {str(e)}")
            return []
            
    def get_process_info(self, pid: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific process"""
        try:
            # Get basic process info
            cmd = ["ps", "-p", str(pid), "-o", "pid,ppid,user,%cpu,%mem,state,lstart,command"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            processes = self._parse_ps_output(proc.stdout)
            if not processes:
                return None
                
            process = processes[0]
            
            # Add additional info
            process["files"] = self._get_open_files(pid)
            process["ports"] = self._get_network_ports(pid)
            process["env"] = self._get_environment(pid)
            
            return process
            
        except Exception as e:
            self.logger.error(f"Error getting process info: {str(e)}")
            return None
            
    def get_process_tree(self, pid: Optional[int] = None) -> Dict[int, Dict[str, Any]]:
        """Get process tree"""
        try:
            # Get all processes
            processes = self.get_processes()
            
            # Build tree structure
            tree = {}
            for process in processes:
                pid = process["pid"]
                ppid = process["ppid"]
                
                # Add to tree
                if pid not in tree:
                    tree[pid] = {"info": process, "children": []}
                else:
                    tree[pid]["info"] = process
                    
                # Add to parent's children
                if ppid in tree:
                    tree[ppid]["children"].append(pid)
                    
            return tree
            
        except Exception as e:
            self.logger.error(f"Error building process tree: {str(e)}")
            return {}
            
    def get_resource_usage(self, pid: int) -> Dict[str, Any]:
        """Get detailed resource usage for a process"""
        try:
            # Use ps for resource info
            cmd = ["ps", "-p", str(pid), "-o", "%cpu,%mem,rss,vsz,utime,stime"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_resource_usage(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting resource usage: {str(e)}")
            return {}
            
    def _parse_ps_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse ps command output"""
        processes = []
        lines = output.split("\n")
        
        if len(lines) < 2:  # Need at least header and one process
            return processes
            
        # Get header fields
        headers = lines[0].strip().lower().split()
        
        # Parse each process line
        for line in lines[1:]:
            if not line.strip():
                continue
                
            try:
                parts = line.strip().split(None, len(headers) - 1)
                if len(parts) >= len(headers):
                    process = {}
                    for i, header in enumerate(headers):
                        value = parts[i]
                        # Convert numeric values
                        if header in ["pid", "ppid"]:
                            process[header] = int(value)
                        elif header in ["%cpu", "%mem"]:
                            process[header] = float(value)
                        else:
                            process[header] = value
                    processes.append(process)
            except Exception as e:
                self.logger.error(f"Error parsing process line: {str(e)}")
                continue
                
        return processes
        
    def _get_open_files(self, pid: int) -> List[str]:
        """Get open files for a process"""
        try:
            cmd = ["lsof", "-p", str(pid), "-F", "n"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            files = []
            for line in proc.stdout.split("\n"):
                if line.startswith("n"):  # File name
                    files.append(line[1:])  # Remove 'n' prefix
                    
            return files
            
        except Exception as e:
            self.logger.error(f"Error getting open files: {str(e)}")
            return []
            
    def _get_network_ports(self, pid: int) -> List[Dict[str, Any]]:
        """Get network ports used by process"""
        try:
            cmd = ["lsof", "-i", "-a", "-p", str(pid), "-n", "-P"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            ports = []
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    try:
                        parts = line.split()
                        if len(parts) >= 9:
                            port = {
                                "protocol": parts[4],
                                "address": parts[8],
                                "state": parts[9] if len(parts) > 9 else None
                            }
                            ports.append(port)
                    except Exception as e:
                        self.logger.error(f"Error parsing port line: {str(e)}")
                        continue
                        
            return ports
            
        except Exception as e:
            self.logger.error(f"Error getting network ports: {str(e)}")
            return []
            
    def _get_environment(self, pid: int) -> Dict[str, str]:
        """Get environment variables for process"""
        try:
            cmd = ["ps", "eww", "-p", str(pid)]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            env = {}
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if "=" in line:
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip()
                    
            return env
            
        except Exception as e:
            self.logger.error(f"Error getting environment: {str(e)}")
            return {}
            
    def _parse_resource_usage(self, output: str) -> Dict[str, Any]:
        """Parse resource usage output"""
        usage = {}
        lines = output.split("\n")
        
        if len(lines) < 2:  # Need header and values
            return usage
            
        try:
            # Get header fields
            headers = lines[0].strip().lower().split()
            values = lines[1].strip().split()
            
            if len(headers) == len(values):
                for i, header in enumerate(headers):
                    try:
                        # Convert values to appropriate types
                        if header in ["%cpu", "%mem"]:
                            usage[header] = float(values[i])
                        elif header in ["rss", "vsz"]:
                            usage[header] = int(values[i])
                        else:
                            usage[header] = values[i]
                    except ValueError:
                        usage[header] = values[i]
                        
        except Exception as e:
            self.logger.error(f"Error parsing resource usage: {str(e)}")
            
        return usage
``` 
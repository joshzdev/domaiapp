"""
DNS monitoring and resolution module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

class DNSMonitor:
    """Monitor DNS activity and resolution"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_dns_servers(self) -> List[str]:
        """Get configured DNS servers"""
        try:
            # Use scutil to get DNS servers
            cmd = ["scutil", "--dns"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_dns_servers(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"scutil failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting DNS servers: {str(e)}")
            return []
            
    def resolve_name(self, hostname: str) -> List[Dict[str, Any]]:
        """Resolve hostname to IP addresses"""
        try:
            # Use dig for DNS resolution
            cmd = ["dig", "+noall", "+answer", hostname]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_dig_output(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"dig failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error resolving hostname: {str(e)}")
            return []
            
    def get_local_cache(self) -> List[Dict[str, Any]]:
        """Get local DNS cache entries"""
        try:
            # Use dscacheutil to get DNS cache
            cmd = ["dscacheutil", "-q", "host"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_cache_entries(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"dscacheutil failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting DNS cache: {str(e)}")
            return []
            
    def check_dns_sec(self, domain: str) -> Dict[str, Any]:
        """Check DNSSEC status for domain"""
        try:
            # Use dig with DNSSEC checking
            cmd = ["dig", "+dnssec", "+multi", domain, "DNSKEY"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_dnssec_status(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"dig failed: {e.stderr}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            self.logger.error(f"Error checking DNSSEC: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def _parse_dns_servers(self, output: str) -> List[str]:
        """Parse scutil DNS server output"""
        servers = []
        
        for line in output.split("\n"):
            line = line.strip()
            if "nameserver[" in line and "]" in line:
                try:
                    # Extract server IP
                    server = line.split("]")[1].strip()
                    if server:
                        servers.append(server)
                except Exception as e:
                    self.logger.error(f"Error parsing DNS server line: {str(e)}")
                    continue
                    
        return servers
        
    def _parse_dig_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse dig command output"""
        records = []
        
        for line in output.split("\n"):
            if not line.strip():
                continue
                
            try:
                parts = line.split()
                if len(parts) >= 5:
                    record = {
                        "name": parts[0],
                        "ttl": int(parts[1]),
                        "class": parts[2],
                        "type": parts[3],
                        "data": parts[4]
                    }
                    records.append(record)
            except Exception as e:
                self.logger.error(f"Error parsing dig output line: {str(e)}")
                continue
                
        return records
        
    def _parse_cache_entries(self, output: str) -> List[Dict[str, Any]]:
        """Parse DNS cache entries"""
        entries = []
        current_entry = {}
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                continue
                
            if ":" in line:
                key, value = line.split(":", 1)
                current_entry[key.strip()] = value.strip()
                
        if current_entry:
            entries.append(current_entry)
            
        return entries
        
    def _parse_dnssec_status(self, output: str) -> Dict[str, Any]:
        """Parse DNSSEC status output"""
        status = {
            "enabled": False,
            "validated": False,
            "keys": []
        }
        
        for line in output.split("\n"):
            line = line.strip().lower()
            
            # Check for DNSSEC validation
            if "flags:" in line and "ad" in line:
                status["validated"] = True
                
            # Check for DNSKEY records
            if "dnskey" in line:
                status["enabled"] = True
                try:
                    # Extract key info
                    parts = line.split()
                    if len(parts) >= 7:
                        key = {
                            "flags": int(parts[4]),
                            "protocol": int(parts[5]),
                            "algorithm": int(parts[6])
                        }
                        status["keys"].append(key)
                except Exception as e:
                    self.logger.error(f"Error parsing DNSKEY line: {str(e)}")
                    continue
                    
        return status 
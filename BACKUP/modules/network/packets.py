"""
Network packet capture and analysis module
"""

import logging
import subprocess
import threading
from typing import Optional, Dict, Any, List
from pathlib import Path

class PacketCapture:
    """Packet capture using tcpdump"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.process: Optional[subprocess.Popen] = None
        self.capture_thread: Optional[threading.Thread] = None
        self.should_capture = False
        
    def start_capture(
        self,
        interface: str = "any",
        port: Optional[int] = None,
        host: Optional[str] = None,
        protocol: Optional[str] = None,
        output_file: Optional[Path] = None,
        callback: Optional[callable] = None
    ) -> bool:
        """Start packet capture with given filters"""
        try:
            # Build tcpdump command
            cmd = ["tcpdump", "-i", interface, "-n"]
            
            # Add filters
            if port:
                cmd.extend(["port", str(port)])
            if host:
                cmd.extend(["host", host])
            if protocol:
                cmd.append(protocol)
                
            # Add output file if specified
            if output_file:
                cmd.extend(["-w", str(output_file)])
            else:
                cmd.append("-l")  # Line-buffered output
                
            # Start capture process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Start capture thread if callback provided
            if callback and not output_file:
                self.should_capture = True
                self.capture_thread = threading.Thread(
                    target=self._capture_loop,
                    args=(callback,),
                    daemon=True
                )
                self.capture_thread.start()
            
            self.logger.info(f"Started packet capture: {' '.join(cmd)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start packet capture: {str(e)}")
            return False
            
    def stop_capture(self) -> None:
        """Stop packet capture"""
        if self.process:
            try:
                self.should_capture = False
                self.process.terminate()
                self.process.wait(timeout=5)
                if self.capture_thread:
                    self.capture_thread.join(timeout=5)
                self.logger.info("Stopped packet capture")
            except Exception as e:
                self.logger.error(f"Error stopping packet capture: {str(e)}")
            finally:
                self.process = None
                self.capture_thread = None
                
    def get_stats(self) -> Dict[str, Any]:
        """Get capture statistics"""
        if not self.process:
            return {"status": "not running"}
            
        try:
            # Get process stats
            proc = subprocess.run(
                ["ps", "-p", str(self.process.pid), "-o", "%cpu,%mem"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse stats
            stats = proc.stdout.split("\n")[1].strip().split()
            return {
                "status": "running",
                "pid": self.process.pid,
                "cpu_percent": float(stats[0]),
                "memory_percent": float(stats[1])
            }
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting process stats: {e.stderr}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            self.logger.error(f"Error getting capture stats: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def analyze_capture(
        self,
        capture_file: Path,
        filters: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """Analyze captured packets"""
        try:
            # Build tcpdump read command
            cmd = ["tcpdump", "-r", str(capture_file), "-nn", "-v"]
            
            # Add any filters
            if filters:
                for key, value in filters.items():
                    cmd.extend([key, value])
                    
            # Run analysis
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse output into structured data
            packets = []
            for line in proc.stdout.split("\n"):
                if line.strip():
                    packet = self._parse_packet_line(line)
                    if packet:
                        packets.append(packet)
                        
            return packets
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Analysis failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error analyzing capture: {str(e)}")
            return []
            
    def _capture_loop(self, callback: callable) -> None:
        """Background capture loop"""
        try:
            while self.should_capture and self.process:
                line = self.process.stdout.readline()
                if not line:
                    break
                packet = self._parse_packet_line(line)
                if packet:
                    callback(packet)
        except Exception as e:
            self.logger.error(f"Error in capture loop: {str(e)}")
            
    def _parse_packet_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single packet line from tcpdump output"""
        try:
            # Basic parsing - can be enhanced based on needs
            parts = line.split()
            if len(parts) < 3:
                return None
                
            return {
                "timestamp": parts[0],
                "protocol": parts[1],
                "details": " ".join(parts[2:])
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing packet line: {str(e)}")
            return None 
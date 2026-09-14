"""
Network Security Monitor for DōmAI
Provides real-time network monitoring and analysis
"""

import logging
import threading
import queue
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import subprocess
import re
import psutil
import scapy.all as scapy
from pathlib import Path
import os
import sys
import signal
import shutil
import platform
import socket

class NetworkMonitor:
    """Real-time network security monitoring"""
    
    # Base network patterns
    BASE_PATTERNS = {
        'port_scan': r'(\d+\.){3}\d+.*SYN',
        'dns_tunnel': r'[a-zA-Z0-9-]{30,}\..*\.(com|net|org)',
        'data_exfil': r'POST.*transfer|upload|exfil',
        'c2_traffic': r'beaconing|heartbeat|check-in',
        'crypto_mining': r'(xmr|monero|btc|ethereum)',
        'tor_traffic': r'\.onion|tor2web|torproject'
    }
    
    # Platform-specific patterns
    PLATFORM_PATTERNS = {
        'darwin': {  # macOS
            'firewall_bypass': r'natpmp|upnp|bonjour',
            'vpn_detect': r'utun\d+|ppp\d+',
            'system_proxy': r'proximac|burp|charles',
            'mdns_exploit': r'\.local|_tcp\.local|_udp\.local'
        },
        'linux': {
            'container_escape': r'docker\.sock|containerd|cri-o',
            'tunnel_detect': r'tun\d+|tap\d+',
            'proxy_detect': r'squid|privoxy|polipo',
            'netfilter_bypass': r'raw\s+socket|libpcap'
        }
    }
    
    # Base packet filters
    BASE_FILTERS = {
        'tcp': 'tcp',
        'udp': 'udp',
        'icmp': 'icmp',
        'dns': 'udp port 53',
        'http': 'tcp port 80 or tcp port 443',
        'suspicious': 'tcp[13] = 0x02 or udp port 53'  # SYN packets or DNS
    }
    
    # Platform-specific filters
    PLATFORM_FILTERS = {
        'darwin': {
            'bonjour': 'udp port 5353',  # mDNS
            'airplay': 'tcp port 7000 or udp port 7011',
            'icloud': 'tcp port 443 and host *.icloud.com',
            'timemachine': 'tcp port 548 or udp port 548'
        },
        'linux': {
            'docker': 'tcp port 2375 or tcp port 2376',
            'kubernetes': 'tcp port 6443 or tcp port 10250',
            'systemd': 'tcp port 19531 or tcp port 19532',
            'journald': 'tcp port 19532'
        }
    }
    
    def __init__(self):
        self._lock = threading.Lock()
        self.active = False
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.packet_queue = queue.Queue()
        self.event_handlers: List[callable] = []
        self.capture_thread: Optional[threading.Thread] = None
        self.analysis_thread: Optional[threading.Thread] = None
        self.known_hosts: Set[str] = set()
        self.suspicious_ips: Dict[str, Dict[str, Any]] = {}
        self.temp_files: List[Path] = []
        
        # Setup platform-specific configurations
        self._setup_platform_config()
        
        # Setup logging
        self.logger = logging.getLogger("domai.network")
        self._setup_logging()
        
        # Setup signal handlers
        self._setup_signal_handlers()
        
    def _setup_platform_config(self) -> None:
        """Setup platform-specific configurations"""
        try:
            platform_name = sys.platform
            
            # Set patterns
            self.SUSPICIOUS_PATTERNS = self.BASE_PATTERNS.copy()
            if platform_name in self.PLATFORM_PATTERNS:
                self.SUSPICIOUS_PATTERNS.update(self.PLATFORM_PATTERNS[platform_name])
                
            # Set filters
            self.PACKET_FILTERS = self.BASE_FILTERS.copy()
            if platform_name in self.PLATFORM_FILTERS:
                self.PACKET_FILTERS.update(self.PLATFORM_FILTERS[platform_name])
                
            # Configure platform-specific network interfaces
            if platform_name == 'darwin':
                scapy.conf.use_pcap = True
                
        except Exception as e:
            self.logger.error(f"Failed to setup platform config: {e}")
            # Fall back to base configurations
            self.SUSPICIOUS_PATTERNS = self.BASE_PATTERNS
            self.PACKET_FILTERS = self.BASE_FILTERS
            
    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown"""
        try:
            signal.signal(signal.SIGTERM, self._handle_shutdown_signal)
            signal.signal(signal.SIGINT, self._handle_shutdown_signal)
            if sys.platform != 'win32':
                signal.signal(signal.SIGHUP, self._handle_shutdown_signal)
                
        except Exception as e:
            self.logger.error(f"Failed to setup signal handlers: {e}")
            
    def _handle_shutdown_signal(self, signum: int, frame: Any) -> None:
        """Handle shutdown signals"""
        self.logger.info(f"Received shutdown signal {signum}")
        self.cleanup()
        self.stop()
        
    def cleanup(self) -> None:
        """Cleanup resources and temporary files"""
        try:
            # Clean up temp files
            for temp_file in self.temp_files:
                try:
                    if temp_file.exists():
                        if temp_file.is_file():
                            temp_file.unlink()
                        elif temp_file.is_dir():
                            shutil.rmtree(temp_file)
                except Exception as e:
                    self.logger.error(f"Failed to remove temp file {temp_file}: {e}")
                    
            # Clean up log directory if empty
            try:
                log_dir = Path("logs/network")
                if log_dir.exists() and not any(log_dir.iterdir()):
                    log_dir.rmdir()
            except Exception as e:
                self.logger.error(f"Failed to cleanup log directory: {e}")
                
            # Clean up packet capture resources
            try:
                scapy.conf.reset()
            except Exception as e:
                self.logger.error(f"Failed to reset scapy configuration: {e}")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
            
    def _setup_logging(self) -> None:
        """Setup secure logging"""
        try:
            log_dir = Path("logs/network")
            log_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(log_dir, 0o700)
            
            log_file = log_dir / "network.log"
            log_file.touch(mode=0o600, exist_ok=True)
            self.temp_files.append(log_file)  # Track for cleanup
            
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
            
        except Exception as e:
            self.logger.error(f"Failed to setup network logging: {e}")
            
    def start(self) -> bool:
        """Start network monitoring"""
        try:
            with self._lock:
                if self.active:
                    return True
                    
                # Start packet capture
                self.active = True
                self.capture_thread = threading.Thread(
                    target=self._capture_packets,
                    daemon=True
                )
                self.capture_thread.start()
                
                # Start analysis
                self.analysis_thread = threading.Thread(
                    target=self._analyze_packets,
                    daemon=True
                )
                self.analysis_thread.start()
                
                self.logger.info("Network monitoring started")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start network monitoring: {e}")
            return False
            
    def stop(self) -> None:
        """Stop network monitoring"""
        try:
            with self._lock:
                if not self.active:
                    return
                    
                self.active = False
                
                # Stop threads
                if self.capture_thread:
                    self.capture_thread.join(timeout=5)
                if self.analysis_thread:
                    self.analysis_thread.join(timeout=5)
                    
                # Cleanup resources
                self.cleanup()
                
                self.logger.info("Network monitoring stopped")
                
        except Exception as e:
            self.logger.error(f"Failed to stop network monitoring: {e}")
            
    def start_session(self, session_id: str) -> bool:
        """Start monitoring for a session"""
        try:
            with self._lock:
                if session_id in self.sessions:
                    return True
                    
                self.sessions[session_id] = {
                    'start_time': datetime.now(),
                    'suspicious_events': [],
                    'blocked_ips': set(),
                    'monitored_ports': set(),
                    'active': True,
                    'platform': {
                        'system': platform.system(),
                        'release': platform.release(),
                        'version': platform.version(),
                        'machine': platform.machine(),
                        'network_interfaces': self._get_network_interfaces()
                    }
                }
                
                self.logger.info(f"Started network monitoring for session: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start session monitoring: {e}")
            return False
            
    def stop_session(self, session_id: str) -> bool:
        """Stop monitoring for a session"""
        try:
            with self._lock:
                if session_id not in self.sessions:
                    return True
                    
                self.sessions[session_id]['active'] = False
                del self.sessions[session_id]
                
                self.logger.info(f"Stopped network monitoring for session: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop session monitoring: {e}")
            return False
            
    def register_event_handler(self, handler: callable) -> None:
        """Register event handler"""
        self.event_handlers.append(handler)
        
    def handle_event(self, event: Dict[str, Any]) -> None:
        """Handle network security event"""
        try:
            event_type = event.get('type')
            session_id = event.get('session_id')
            
            if event_type == 'block_ip':
                self._block_ip(event['ip'], session_id)
            elif event_type == 'monitor_port':
                self._monitor_port(event['port'], session_id)
            elif event_type == 'analyze_traffic':
                self._analyze_traffic_pattern(event['pattern'], session_id)
                
        except Exception as e:
            self.logger.error(f"Failed to handle network event: {e}")
            
    def _capture_packets(self) -> None:
        """Capture network packets"""
        try:
            # Start packet capture with platform-specific filter
            filter_str = ' or '.join(self.PACKET_FILTERS.values())
            scapy.sniff(
                prn=self._process_packet,
                store=0,
                filter=filter_str,
                stop_filter=lambda _: not self.active
            )
        except Exception as e:
            self.logger.error(f"Packet capture error: {e}")
            
    def _process_packet(self, packet: scapy.Packet) -> None:
        """Process captured packet"""
        try:
            if not packet.haslayer(scapy.IP):
                return
                
            # Extract packet info
            ip_src = packet[scapy.IP].src
            ip_dst = packet[scapy.IP].dst
            
            # Update known hosts
            self.known_hosts.add(ip_src)
            self.known_hosts.add(ip_dst)
            
            # Queue for analysis
            self.packet_queue.put({
                'timestamp': datetime.now(),
                'src': ip_src,
                'dst': ip_dst,
                'proto': packet[scapy.IP].proto,
                'size': len(packet),
                'flags': self._get_tcp_flags(packet),
                'data': str(packet.payload)
            })
            
        except Exception as e:
            self.logger.error(f"Packet processing error: {e}")
            
    def _analyze_packets(self) -> None:
        """Analyze network packets"""
        while self.active:
            try:
                # Get packet from queue
                packet = self.packet_queue.get(timeout=1)
                
                # Check for suspicious patterns
                for pattern_name, pattern in self.SUSPICIOUS_PATTERNS.items():
                    if re.search(pattern, packet['data'], re.I):
                        self._handle_suspicious_traffic(
                            pattern_name,
                            packet
                        )
                        
                # Check for anomalies
                self._check_traffic_anomalies(packet)
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Packet analysis error: {e}")
                
    def _handle_suspicious_traffic(self, pattern_name: str,
                                 packet: Dict[str, Any]) -> None:
        """Handle suspicious network traffic"""
        try:
            # Update suspicious IPs tracking
            ip = packet['src']
            if ip not in self.suspicious_ips:
                self.suspicious_ips[ip] = {
                    'first_seen': datetime.now(),
                    'patterns': set(),
                    'count': 0
                }
            
            self.suspicious_ips[ip]['patterns'].add(pattern_name)
            self.suspicious_ips[ip]['count'] += 1
            
            # Generate event
            event = {
                'timestamp': datetime.now(),
                'type': 'suspicious_traffic',
                'pattern': pattern_name,
                'source_ip': ip,
                'destination_ip': packet['dst'],
                'details': {
                    'protocol': packet['proto'],
                    'size': packet['size'],
                    'flags': packet['flags']
                }
            }
            
            # Notify sessions
            self._notify_sessions(event)
            
        except Exception as e:
            self.logger.error(f"Failed to handle suspicious traffic: {e}")
            
    def _check_traffic_anomalies(self, packet: Dict[str, Any]) -> None:
        """Check for traffic anomalies"""
        try:
            ip = packet['src']
            
            # Check for port scanning
            if packet['flags'] == 'S' and ip in self.suspicious_ips:
                self._handle_port_scan(ip, packet)
                
            # Check for data exfiltration
            if packet['size'] > 10000:  # Large packets
                self._check_data_exfiltration(ip, packet)
                
            # Check for C2 traffic
            if self._check_c2_patterns(packet['data']):
                self._handle_c2_traffic(ip, packet)
                
        except Exception as e:
            self.logger.error(f"Failed to check traffic anomalies: {e}")
            
    def _handle_port_scan(self, ip: str, packet: Dict[str, Any]) -> None:
        """Handle potential port scanning"""
        try:
            # Update tracking
            if 'port_scans' not in self.suspicious_ips[ip]:
                self.suspicious_ips[ip]['port_scans'] = set()
            
            self.suspicious_ips[ip]['port_scans'].add(packet['dst'])
            
            # Check threshold
            if len(self.suspicious_ips[ip]['port_scans']) > 10:
                event = {
                    'timestamp': datetime.now(),
                    'type': 'port_scan',
                    'source_ip': ip,
                    'details': {
                        'scanned_ports': len(self.suspicious_ips[ip]['port_scans']),
                        'duration': (datetime.now() - self.suspicious_ips[ip]['first_seen']).seconds
                    }
                }
                
                self._notify_sessions(event)
                
        except Exception as e:
            self.logger.error(f"Failed to handle port scan: {e}")
            
    def _check_data_exfiltration(self, ip: str, packet: Dict[str, Any]) -> None:
        """Check for potential data exfiltration"""
        try:
            # Update tracking
            if 'data_exfil' not in self.suspicious_ips[ip]:
                self.suspicious_ips[ip]['data_exfil'] = {
                    'total_bytes': 0,
                    'start_time': datetime.now()
                }
            
            self.suspicious_ips[ip]['data_exfil']['total_bytes'] += packet['size']
            
            # Check threshold (1MB in 5 minutes)
            if self.suspicious_ips[ip]['data_exfil']['total_bytes'] > 1000000:
                duration = (datetime.now() - self.suspicious_ips[ip]['data_exfil']['start_time']).seconds
                if duration < 300:
                    event = {
                        'timestamp': datetime.now(),
                        'type': 'data_exfiltration',
                        'source_ip': ip,
                        'details': {
                            'bytes_transferred': self.suspicious_ips[ip]['data_exfil']['total_bytes'],
                            'duration': duration
                        }
                    }
                    
                    self._notify_sessions(event)
                    
        except Exception as e:
            self.logger.error(f"Failed to check data exfiltration: {e}")
            
    def _check_c2_patterns(self, data: str) -> bool:
        """Check for command and control patterns"""
        c2_patterns = [
            r'beacon\s*to\s*',
            r'check[-_]in',
            r'heartbeat',
            r'command\s*response',
            r'task\s*result'
        ]
        
        return any(re.search(pattern, data, re.I) for pattern in c2_patterns)
        
    def _handle_c2_traffic(self, ip: str, packet: Dict[str, Any]) -> None:
        """Handle potential C2 traffic"""
        try:
            # Update tracking
            if 'c2_traffic' not in self.suspicious_ips[ip]:
                self.suspicious_ips[ip]['c2_traffic'] = {
                    'count': 0,
                    'start_time': datetime.now()
                }
            
            self.suspicious_ips[ip]['c2_traffic']['count'] += 1
            
            # Check threshold (10 beacons in 5 minutes)
            if self.suspicious_ips[ip]['c2_traffic']['count'] > 10:
                duration = (datetime.now() - self.suspicious_ips[ip]['c2_traffic']['start_time']).seconds
                if duration < 300:
                    event = {
                        'timestamp': datetime.now(),
                        'type': 'c2_traffic',
                        'source_ip': ip,
                        'details': {
                            'beacon_count': self.suspicious_ips[ip]['c2_traffic']['count'],
                            'duration': duration
                        }
                    }
                    
                    self._notify_sessions(event)
                    
        except Exception as e:
            self.logger.error(f"Failed to handle C2 traffic: {e}")
            
    def _block_ip(self, ip: str, session_id: str) -> None:
        """Block an IP address"""
        try:
            if session_id in self.sessions:
                self.sessions[session_id]['blocked_ips'].add(ip)
                
                # Add platform-specific firewall rule
                if sys.platform == 'darwin':
                    subprocess.run([
                        'sudo', 'pfctl', '-t', 'domai-blocked', '-T', 'add', ip
                    ], check=True)
                elif sys.platform == 'linux':
                    subprocess.run([
                        'sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'
                    ], check=True)
                    
                self.logger.info(f"Blocked IP {ip} for session {session_id}")
                
        except Exception as e:
            self.logger.error(f"Failed to block IP {ip}: {e}")
            
    def _monitor_port(self, port: int, session_id: str) -> None:
        """Monitor specific port"""
        try:
            if session_id in self.sessions:
                self.sessions[session_id]['monitored_ports'].add(port)
                self.logger.info(f"Monitoring port {port} for session {session_id}")
                
        except Exception as e:
            self.logger.error(f"Failed to monitor port {port}: {e}")
            
    def _analyze_traffic_pattern(self, pattern: str, session_id: str) -> None:
        """Analyze specific traffic pattern"""
        try:
            if session_id in self.sessions:
                # Add custom pattern
                self.SUSPICIOUS_PATTERNS[f'custom_{session_id}'] = pattern
                self.logger.info(f"Added custom pattern for session {session_id}")
                
        except Exception as e:
            self.logger.error(f"Failed to analyze traffic pattern: {e}")
            
    def _notify_sessions(self, event: Dict[str, Any]) -> None:
        """Notify active sessions of security event"""
        try:
            for session_id, session in self.sessions.items():
                if session['active']:
                    event['session_id'] = session_id
                    
                    # Notify event handlers
                    for handler in self.event_handlers:
                        try:
                            handler(event)
                        except Exception as e:
                            self.logger.error(f"Event handler error: {e}")
                            
        except Exception as e:
            self.logger.error(f"Failed to notify sessions: {e}")
            
    def _get_tcp_flags(self, packet: scapy.Packet) -> str:
        """Get TCP flags from packet"""
        try:
            if packet.haslayer(scapy.TCP):
                flags = []
                if packet[scapy.TCP].flags & 0x02:  # SYN
                    flags.append('S')
                if packet[scapy.TCP].flags & 0x10:  # ACK
                    flags.append('A')
                if packet[scapy.TCP].flags & 0x01:  # FIN
                    flags.append('F')
                if packet[scapy.TCP].flags & 0x04:  # RST
                    flags.append('R')
                if packet[scapy.TCP].flags & 0x08:  # PSH
                    flags.append('P')
                if packet[scapy.TCP].flags & 0x20:  # URG
                    flags.append('U')
                return ''.join(flags)
        except Exception:
            pass
        return ''
        
    def _get_network_interfaces(self) -> Dict[str, Any]:
        """Get network interface information"""
        try:
            interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                interfaces[interface] = {
                    'addresses': [],
                    'stats': None
                }
                for addr in addrs:
                    if addr.family in (socket.AF_INET, socket.AF_INET6):
                        interfaces[interface]['addresses'].append({
                            'address': addr.address,
                            'netmask': addr.netmask,
                            'family': 'IPv4' if addr.family == socket.AF_INET else 'IPv6'
                        })
                        
                # Get interface stats
                try:
                    stats = psutil.net_if_stats()[interface]
                    interfaces[interface]['stats'] = {
                        'speed': stats.speed,
                        'mtu': stats.mtu,
                        'up': stats.isup,
                        'duplex': stats.duplex
                    }
                except Exception:
                    pass
                    
            return interfaces
            
        except Exception as e:
            self.logger.error(f"Failed to get network interfaces: {e}")
            return {}
</rewritten_file> 
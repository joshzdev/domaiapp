"""
System Resource and Security Monitor for DōmAI
Provides real-time system monitoring and analysis
"""

import logging
import threading
import queue
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import psutil
import os
import sys
import signal
import shutil
from pathlib import Path
import re
import platform

class SystemMonitor:
    """Real-time system resource and security monitoring"""
    
    # Base resource thresholds
    BASE_THRESHOLDS = {
        'cpu_percent': 90.0,
        'memory_percent': 85.0,
        'disk_percent': 90.0,
        'network_io_bytes': 100000000,  # 100MB/s
        'process_count': 500
    }
    
    # Platform-specific thresholds
    PLATFORM_THRESHOLDS = {
        'darwin': {  # macOS
            'cpu_percent': 85.0,  # More conservative for laptop usage
            'memory_percent': 80.0,
            'disk_percent': 85.0,
            'network_io_bytes': 50000000,  # 50MB/s for wireless
            'process_count': 400
        },
        'linux': {
            'cpu_percent': 95.0,  # Server-grade thresholds
            'memory_percent': 90.0,
            'disk_percent': 95.0,
            'network_io_bytes': 200000000,  # 200MB/s for server NICs
            'process_count': 1000
        }
    }
    
    # Base security patterns
    BASE_PATTERNS = {
        'root_escalation': r'sudo|su\s|root',
        'shell_spawn': r'bash|sh\s|zsh|python\s',
        'file_access': r'cat\s|vim\s|nano\s|less\s',
        'network_tools': r'nc\s|netcat|nmap|wireshark',
        'crypto_mining': r'xmr|monero|btc|mining',
        'data_exfil': r'scp|rsync|sftp|curl'
    }
    
    # Platform-specific patterns
    PLATFORM_PATTERNS = {
        'darwin': {
            'root_escalation': r'sudo|su\s|root|dscl\s.*?-passwd',
            'system_control': r'launchctl|systemsetup|diskutil',
            'network_control': r'networksetup|pfctl|scutil',
            'kernel_ext': r'kextload|kextutil'
        },
        'linux': {
            'root_escalation': r'sudo|su\s|root|passwd|chroot',
            'system_control': r'systemctl|service|init\s',
            'network_control': r'iptables|netfilter|tc\s',
            'kernel_mod': r'modprobe|insmod|rmmod'
        }
    }
    
    def __init__(self):
        self._lock = threading.Lock()
        self.active = False
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.event_queue = queue.Queue()
        self.event_handlers: List[callable] = []
        self.monitor_thread: Optional[threading.Thread] = None
        self.analysis_thread: Optional[threading.Thread] = None
        self.baseline: Dict[str, Any] = {}
        self.suspicious_processes: Dict[str, Dict[str, Any]] = {}
        self.temp_files: List[Path] = []
        
        # Setup platform-specific configurations
        self._setup_platform_config()
        
        # Setup logging
        self.logger = logging.getLogger("domai.system")
        self._setup_logging()
        
        # Setup signal handlers
        self._setup_signal_handlers()
        
    def _setup_platform_config(self) -> None:
        """Setup platform-specific configurations"""
        try:
            platform_name = sys.platform
            
            # Set thresholds
            self.THRESHOLDS = self.BASE_THRESHOLDS.copy()
            if platform_name in self.PLATFORM_THRESHOLDS:
                self.THRESHOLDS.update(self.PLATFORM_THRESHOLDS[platform_name])
                
            # Set patterns
            self.SUSPICIOUS_PATTERNS = self.BASE_PATTERNS.copy()
            if platform_name in self.PLATFORM_PATTERNS:
                self.SUSPICIOUS_PATTERNS.update(self.PLATFORM_PATTERNS[platform_name])
                
        except Exception as e:
            self.logger.error(f"Failed to setup platform config: {e}")
            # Fall back to base configurations
            self.THRESHOLDS = self.BASE_THRESHOLDS
            self.SUSPICIOUS_PATTERNS = self.BASE_PATTERNS
            
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
                log_dir = Path("logs/system")
                if log_dir.exists() and not any(log_dir.iterdir()):
                    log_dir.rmdir()
            except Exception as e:
                self.logger.error(f"Failed to cleanup log directory: {e}")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
            
    def _setup_logging(self) -> None:
        """Setup secure logging"""
        try:
            log_dir = Path("logs/system")
            log_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(log_dir, 0o700)
            
            log_file = log_dir / "system.log"
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
            self.logger.error(f"Failed to setup system logging: {e}")
            
    def start(self) -> bool:
        """Start system monitoring"""
        try:
            with self._lock:
                if self.active:
                    return True
                    
                # Establish baseline
                self._establish_baseline()
                
                # Start monitoring
                self.active = True
                self.monitor_thread = threading.Thread(
                    target=self._monitor_system,
                    daemon=True
                )
                self.monitor_thread.start()
                
                # Start analysis
                self.analysis_thread = threading.Thread(
                    target=self._analyze_events,
                    daemon=True
                )
                self.analysis_thread.start()
                
                self.logger.info("System monitoring started")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start system monitoring: {e}")
            return False
            
    def stop(self) -> None:
        """Stop system monitoring"""
        try:
            with self._lock:
                if not self.active:
                    return
                    
                self.active = False
                
                # Stop threads
                if self.monitor_thread:
                    self.monitor_thread.join(timeout=5)
                if self.analysis_thread:
                    self.analysis_thread.join(timeout=5)
                    
                # Cleanup resources
                self.cleanup()
                
                self.logger.info("System monitoring stopped")
                
        except Exception as e:
            self.logger.error(f"Failed to stop system monitoring: {e}")
            
    def start_session(self, session_id: str) -> bool:
        """Start monitoring for a session"""
        try:
            with self._lock:
                if session_id in self.sessions:
                    return True
                    
                self.sessions[session_id] = {
                    'start_time': datetime.now(),
                    'suspicious_events': [],
                    'monitored_processes': set(),
                    'resource_usage': {},
                    'active': True,
                    'platform': {
                        'system': platform.system(),
                        'release': platform.release(),
                        'version': platform.version(),
                        'machine': platform.machine(),
                        'processor': platform.processor()
                    }
                }
                
                self.logger.info(f"Started system monitoring for session: {session_id}")
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
                
                self.logger.info(f"Stopped system monitoring for session: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop session monitoring: {e}")
            return False
            
    def register_event_handler(self, handler: callable) -> None:
        """Register event handler"""
        self.event_handlers.append(handler)
        
    def _establish_baseline(self) -> None:
        """Establish system baseline"""
        try:
            self.baseline = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'disk': {disk.mountpoint: psutil.disk_usage(disk.mountpoint)._asdict()
                        for disk in psutil.disk_partitions()},
                'network': psutil.net_io_counters()._asdict(),
                'process_count': len(psutil.pids()),
                'load_avg': os.getloadavg(),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to establish baseline: {e}")
            
    def _monitor_system(self) -> None:
        """Monitor system resources and processes"""
        while self.active:
            try:
                # Collect system metrics
                metrics = {
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory': psutil.virtual_memory()._asdict(),
                    'disk': {disk.mountpoint: psutil.disk_usage(disk.mountpoint)._asdict()
                            for disk in psutil.disk_partitions()},
                    'network': psutil.net_io_counters()._asdict(),
                    'process_count': len(psutil.pids()),
                    'load_avg': os.getloadavg(),
                    'timestamp': datetime.now()
                }
                
                # Check thresholds
                self._check_resource_thresholds(metrics)
                
                # Monitor processes
                self._monitor_processes()
                
                # Queue metrics
                self.event_queue.put({
                    'type': 'metrics',
                    'data': metrics
                })
                
            except Exception as e:
                self.logger.error(f"System monitoring error: {e}")
                
    def _check_resource_thresholds(self, metrics: Dict[str, Any]) -> None:
        """Check resource thresholds"""
        try:
            # CPU usage
            if metrics['cpu_percent'] > self.THRESHOLDS['cpu_percent']:
                self._handle_threshold_breach('cpu', metrics['cpu_percent'])
                
            # Memory usage
            if metrics['memory']['percent'] > self.THRESHOLDS['memory_percent']:
                self._handle_threshold_breach('memory', metrics['memory']['percent'])
                
            # Disk usage
            for mountpoint, usage in metrics['disk'].items():
                if usage['percent'] > self.THRESHOLDS['disk_percent']:
                    self._handle_threshold_breach('disk', usage['percent'], mountpoint)
                    
            # Network I/O
            net_io = metrics['network']
            total_io = net_io['bytes_sent'] + net_io['bytes_recv']
            if total_io > self.THRESHOLDS['network_io_bytes']:
                self._handle_threshold_breach('network', total_io)
                
            # Process count
            if metrics['process_count'] > self.THRESHOLDS['process_count']:
                self._handle_threshold_breach('process_count', metrics['process_count'])
                
        except Exception as e:
            self.logger.error(f"Failed to check resource thresholds: {e}")
            
    def _handle_threshold_breach(self, resource: str, value: float,
                               detail: str = None) -> None:
        """Handle resource threshold breach"""
        try:
            event = {
                'timestamp': datetime.now(),
                'type': 'threshold_breach',
                'resource': resource,
                'value': value,
                'threshold': self.THRESHOLDS.get(resource, 0),
                'detail': detail
            }
            
            self.event_queue.put(event)
            
        except Exception as e:
            self.logger.error(f"Failed to handle threshold breach: {e}")
            
    def _monitor_processes(self) -> None:
        """Monitor system processes"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username']):
                try:
                    proc_info = proc.info
                    cmdline = ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else ''
                    
                    # Check for suspicious patterns
                    for pattern_name, pattern in self.SUSPICIOUS_PATTERNS.items():
                        if re.search(pattern, cmdline, re.I):
                            self._handle_suspicious_process(
                                pattern_name,
                                proc_info,
                                cmdline
                            )
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"Failed to monitor processes: {e}")
            
    def _handle_suspicious_process(self, pattern_name: str,
                                 proc_info: Dict[str, Any],
                                 cmdline: str) -> None:
        """Handle suspicious process"""
        try:
            pid = proc_info['pid']
            
            if pid not in self.suspicious_processes:
                self.suspicious_processes[pid] = {
                    'first_seen': datetime.now(),
                    'patterns': set(),
                    'info': proc_info
                }
                
            self.suspicious_processes[pid]['patterns'].add(pattern_name)
            
            event = {
                'timestamp': datetime.now(),
                'type': 'suspicious_process',
                'pattern': pattern_name,
                'process': {
                    'pid': pid,
                    'name': proc_info['name'],
                    'user': proc_info['username'],
                    'cmdline': cmdline
                }
            }
            
            self.event_queue.put(event)
            
        except Exception as e:
            self.logger.error(f"Failed to handle suspicious process: {e}")
            
    def _analyze_events(self) -> None:
        """Analyze system events"""
        while self.active:
            try:
                # Get event from queue
                event = self.event_queue.get(timeout=1)
                
                # Update sessions
                self._notify_sessions(event)
                
                # Log event
                if event['type'] != 'metrics':
                    self.logger.warning(
                        f"System event: {event['type']} - {event.get('detail', '')}"
                    )
                    
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Event analysis error: {e}")
                
    def _notify_sessions(self, event: Dict[str, Any]) -> None:
        """Notify active sessions of system event"""
        try:
            for session_id, session in self.sessions.items():
                if session['active']:
                    event['session_id'] = session_id
                    
                    # Update session metrics
                    if event['type'] == 'metrics':
                        session['resource_usage'] = event['data']
                    elif event['type'] in ['threshold_breach', 'suspicious_process']:
                        session['suspicious_events'].append(event)
                        
                    # Notify event handlers
                    for handler in self.event_handlers:
                        try:
                            handler(event)
                        except Exception as e:
                            self.logger.error(f"Event handler error: {e}")
                            
        except Exception as e:
            self.logger.error(f"Failed to notify sessions: {e}")
            
    def get_session_metrics(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a session"""
        try:
            if session_id in self.sessions:
                return self.sessions[session_id]['resource_usage']
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get session metrics: {e}")
            return None
            
    def get_session_events(self, session_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get events for a session"""
        try:
            if session_id in self.sessions:
                return self.sessions[session_id]['suspicious_events']
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get session events: {e}")
            return None 
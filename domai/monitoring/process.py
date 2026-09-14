"""
Process Monitor for DōmAI
Provides real-time process monitoring and analysis
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

class ProcessMonitor:
    """Real-time process monitoring and analysis"""
    
    # Base process thresholds
    BASE_THRESHOLDS = {
        'cpu_percent': 80.0,
        'memory_percent': 75.0,
        'open_files': 1000,
        'threads': 100,
        'connections': 50
    }
    
    # Platform-specific thresholds
    PLATFORM_THRESHOLDS = {
        'darwin': {  # macOS
            'cpu_percent': 75.0,  # More conservative for laptops
            'memory_percent': 70.0,
            'open_files': 800,
            'threads': 80,
            'connections': 40
        },
        'linux': {
            'cpu_percent': 90.0,  # Server-grade thresholds
            'memory_percent': 85.0,
            'open_files': 2000,
            'threads': 200,
            'connections': 100
        }
    }
    
    # Base process patterns
    BASE_PATTERNS = {
        'shell_injection': r'eval|exec|system|popen',
        'privilege_escalation': r'sudo|su\s|chmod\s.*777|chown',
        'network_abuse': r'nc\s|netcat|nmap|tcpdump',
        'file_tampering': r'shred|wipe|srm|truncate',
        'crypto_mining': r'minerd|cpuminer|xmrig',
        'reverse_shell': r'bash\s+-i|python\s+-c.*socket'
    }
    
    # Platform-specific patterns
    PLATFORM_PATTERNS = {
        'darwin': {
            'kernel_exploit': r'kext|sysctl\s+-w|nvram',
            'system_override': r'launchctl|defaults\s+write|systemsetup',
            'app_injection': r'DYLD_|DYLIB_|inject',
            'debug_attach': r'lldb|dtrace|xcode'
        },
        'linux': {
            'kernel_exploit': r'modprobe|insmod|rmmod|sysctl\s+-w',
            'system_override': r'systemctl|service|init\s',
            'memory_exploit': r'\/proc\/sys|\/dev\/mem|\/dev\/kmem',
            'container_escape': r'docker.*privileged|lxc.*privileged'
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
        self.watched_processes: Dict[int, Dict[str, Any]] = {}
        self.suspicious_processes: Dict[int, Dict[str, Any]] = {}
        self.temp_files: List[Path] = []
        
        # Setup platform-specific configurations
        self._setup_platform_config()
        
        # Setup logging
        self.logger = logging.getLogger("domai.process")
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
                
            # Configure platform-specific settings
            if platform_name == 'darwin':
                # Enable macOS-specific process monitoring
                os.environ['OBJC_DISABLE_GC'] = 'YES'  # Required for some process operations
                
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
                log_dir = Path("logs/process")
                if log_dir.exists() and not any(log_dir.iterdir()):
                    log_dir.rmdir()
            except Exception as e:
                self.logger.error(f"Failed to cleanup log directory: {e}")
                
            # Clean up process resources
            try:
                for pid in list(self.watched_processes.keys()):
                    self._handle_process_exit(pid)
            except Exception as e:
                self.logger.error(f"Failed to cleanup process resources: {e}")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
            
    def _setup_logging(self) -> None:
        """Setup secure logging"""
        try:
            log_dir = Path("logs/process")
            log_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(log_dir, 0o700)
            
            log_file = log_dir / "process.log"
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
            self.logger.error(f"Failed to setup process logging: {e}")
            
    def start(self) -> bool:
        """Start process monitoring"""
        try:
            with self._lock:
                if self.active:
                    return True
                    
                # Start monitoring
                self.active = True
                self.monitor_thread = threading.Thread(
                    target=self._monitor_processes,
                    daemon=True
                )
                self.monitor_thread.start()
                
                # Start analysis
                self.analysis_thread = threading.Thread(
                    target=self._analyze_events,
                    daemon=True
                )
                self.analysis_thread.start()
                
                self.logger.info("Process monitoring started")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start process monitoring: {e}")
            return False
            
    def stop(self) -> None:
        """Stop process monitoring"""
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
                
                self.logger.info("Process monitoring stopped")
                
        except Exception as e:
            self.logger.error(f"Failed to stop process monitoring: {e}")
            
    def start_session(self, session_id: str) -> bool:
        """Start monitoring for a session"""
        try:
            with self._lock:
                if session_id in self.sessions:
                    return True
                    
                self.sessions[session_id] = {
                    'start_time': datetime.now(),
                    'suspicious_events': [],
                    'watched_pids': set(),
                    'process_metrics': {},
                    'active': True,
                    'platform': {
                        'system': platform.system(),
                        'release': platform.release(),
                        'version': platform.version(),
                        'machine': platform.machine(),
                        'processor': platform.processor(),
                        'cpu_count': psutil.cpu_count(),
                        'memory_total': psutil.virtual_memory().total
                    }
                }
                
                self.logger.info(f"Started process monitoring for session: {session_id}")
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
                    
                # Stop watching all processes for this session
                for pid in list(self.sessions[session_id]['watched_pids']):
                    self.unwatch_process(pid, session_id)
                    
                self.sessions[session_id]['active'] = False
                del self.sessions[session_id]
                
                self.logger.info(f"Stopped process monitoring for session: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop session monitoring: {e}")
            return False
            
    def register_event_handler(self, handler: callable) -> None:
        """Register event handler"""
        self.event_handlers.append(handler)
        
    def watch_process(self, pid: int, session_id: str) -> bool:
        """Watch specific process"""
        try:
            if session_id not in self.sessions:
                return False
                
            if not psutil.pid_exists(pid):
                return False
                
            with self._lock:
                self.sessions[session_id]['watched_pids'].add(pid)
                if pid not in self.watched_processes:
                    self.watched_processes[pid] = {
                        'start_time': datetime.now(),
                        'sessions': set([session_id]),
                        'metrics': {},
                        'platform': {
                            'cmdline': psutil.Process(pid).cmdline(),
                            'create_time': datetime.fromtimestamp(
                                psutil.Process(pid).create_time()
                            ).isoformat(),
                            'cwd': psutil.Process(pid).cwd(),
                            'environ': dict(psutil.Process(pid).environ())
                        }
                    }
                else:
                    self.watched_processes[pid]['sessions'].add(session_id)
                    
            self.logger.info(f"Watching process {pid} for session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to watch process {pid}: {e}")
            return False
            
    def unwatch_process(self, pid: int, session_id: str) -> bool:
        """Stop watching specific process"""
        try:
            if session_id not in self.sessions:
                return False
                
            with self._lock:
                self.sessions[session_id]['watched_pids'].discard(pid)
                if pid in self.watched_processes:
                    self.watched_processes[pid]['sessions'].discard(session_id)
                    if not self.watched_processes[pid]['sessions']:
                        del self.watched_processes[pid]
                        
            self.logger.info(f"Stopped watching process {pid} for session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unwatch process {pid}: {e}")
            return False
            
    def terminate_process(self, pid: int, session_id: str) -> bool:
        """Terminate specific process"""
        try:
            if session_id not in self.sessions:
                return False
                
            if not psutil.pid_exists(pid):
                return True
                
            proc = psutil.Process(pid)
            
            # Platform-specific termination
            if sys.platform == 'darwin':
                # On macOS, use SIGTERM first, then SIGKILL
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except psutil.TimeoutExpired:
                    proc.kill()
            else:
                # On other platforms, just terminate
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except psutil.TimeoutExpired:
                    proc.kill()
                    
            self.logger.warning(f"Terminated process {pid} for session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to terminate process {pid}: {e}")
            return False
            
    def _monitor_processes(self) -> None:
        """Monitor processes"""
        while self.active:
            try:
                # Monitor all processes
                for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username']):
                    try:
                        self._check_process(proc)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                        
                # Monitor watched processes
                self._monitor_watched_processes()
                
            except Exception as e:
                self.logger.error(f"Process monitoring error: {e}")
                
    def _check_process(self, proc: psutil.Process) -> None:
        """Check individual process"""
        try:
            proc_info = proc.as_dict(attrs=[
                'pid', 'name', 'cmdline', 'username', 'cpu_percent',
                'memory_percent', 'num_threads', 'connections',
                'open_files', 'status'
            ])
            
            cmdline = ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else ''
            
            # Check for suspicious patterns
            for pattern_name, pattern in self.SUSPICIOUS_PATTERNS.items():
                if re.search(pattern, cmdline, re.I):
                    self._handle_suspicious_process(
                        pattern_name,
                        proc_info,
                        cmdline
                    )
                    
            # Check resource usage
            self._check_process_resources(proc_info)
            
        except Exception as e:
            self.logger.error(f"Failed to check process: {e}")
            
    def _monitor_watched_processes(self) -> None:
        """Monitor watched processes"""
        try:
            for pid in list(self.watched_processes.keys()):
                if not psutil.pid_exists(pid):
                    self._handle_process_exit(pid)
                    continue
                    
                try:
                    proc = psutil.Process(pid)
                    metrics = proc.as_dict(attrs=[
                        'cpu_percent', 'memory_percent', 'num_threads',
                        'connections', 'open_files', 'status'
                    ])
                    
                    # Add platform-specific metrics
                    if sys.platform == 'darwin':
                        try:
                            metrics['sandboxed'] = proc.is_running()
                        except Exception:
                            pass
                            
                    self.watched_processes[pid]['metrics'] = metrics
                    
                    # Generate metrics event
                    event = {
                        'timestamp': datetime.now(),
                        'type': 'process_metrics',
                        'pid': pid,
                        'metrics': metrics
                    }
                    
                    self.event_queue.put(event)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    self._handle_process_exit(pid)
                    
        except Exception as e:
            self.logger.error(f"Failed to monitor watched processes: {e}")
            
    def _handle_process_exit(self, pid: int) -> None:
        """Handle process exit"""
        try:
            if pid in self.watched_processes:
                event = {
                    'timestamp': datetime.now(),
                    'type': 'process_exit',
                    'pid': pid,
                    'duration': (datetime.now() - self.watched_processes[pid]['start_time']).seconds,
                    'platform': self.watched_processes[pid].get('platform', {})
                }
                
                self.event_queue.put(event)
                
                # Notify sessions
                for session_id in self.watched_processes[pid]['sessions']:
                    if session_id in self.sessions:
                        self.sessions[session_id]['watched_pids'].discard(pid)
                        
                del self.watched_processes[pid]
                
        except Exception as e:
            self.logger.error(f"Failed to handle process exit: {e}")
            
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
                    'info': proc_info,
                    'platform': {
                        'cmdline': cmdline,
                        'cwd': psutil.Process(pid).cwd(),
                        'create_time': datetime.fromtimestamp(
                            psutil.Process(pid).create_time()
                        ).isoformat()
                    }
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
                },
                'platform': self.suspicious_processes[pid]['platform']
            }
            
            self.event_queue.put(event)
            
        except Exception as e:
            self.logger.error(f"Failed to handle suspicious process: {e}")
            
    def _check_process_resources(self, proc_info: Dict[str, Any]) -> None:
        """Check process resource usage"""
        try:
            pid = proc_info['pid']
            
            # Check CPU usage
            if proc_info.get('cpu_percent', 0) > self.THRESHOLDS['cpu_percent']:
                self._handle_resource_breach('cpu', pid, proc_info)
                
            # Check memory usage
            if proc_info.get('memory_percent', 0) > self.THRESHOLDS['memory_percent']:
                self._handle_resource_breach('memory', pid, proc_info)
                
            # Check thread count
            if proc_info.get('num_threads', 0) > self.THRESHOLDS['threads']:
                self._handle_resource_breach('threads', pid, proc_info)
                
            # Check open files
            if proc_info.get('open_files') and len(proc_info['open_files']) > self.THRESHOLDS['open_files']:
                self._handle_resource_breach('open_files', pid, proc_info)
                
            # Check network connections
            if proc_info.get('connections') and len(proc_info['connections']) > self.THRESHOLDS['connections']:
                self._handle_resource_breach('connections', pid, proc_info)
                
        except Exception as e:
            self.logger.error(f"Failed to check process resources: {e}")
            
    def _handle_resource_breach(self, resource: str,
                              pid: int,
                              proc_info: Dict[str, Any]) -> None:
        """Handle process resource breach"""
        try:
            event = {
                'timestamp': datetime.now(),
                'type': 'resource_breach',
                'resource': resource,
                'pid': pid,
                'process': {
                    'name': proc_info['name'],
                    'user': proc_info['username']
                },
                'value': proc_info.get(f'{resource}_percent', 0),
                'threshold': self.THRESHOLDS[resource],
                'platform': {
                    'system': platform.system(),
                    'cpu_count': psutil.cpu_count(),
                    'memory_total': psutil.virtual_memory().total
                }
            }
            
            self.event_queue.put(event)
            
        except Exception as e:
            self.logger.error(f"Failed to handle resource breach: {e}")
            
    def _analyze_events(self) -> None:
        """Analyze process events"""
        while self.active:
            try:
                # Get event from queue
                event = self.event_queue.get(timeout=1)
                
                # Update sessions
                self._notify_sessions(event)
                
                # Log event
                if event['type'] != 'process_metrics':
                    self.logger.warning(
                        f"Process event: {event['type']} - PID: {event.get('pid', 'N/A')}"
                    )
                    
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Event analysis error: {e}")
                
    def _notify_sessions(self, event: Dict[str, Any]) -> None:
        """Notify active sessions of process event"""
        try:
            # Determine relevant sessions
            relevant_sessions = set()
            
            if event.get('pid') in self.watched_processes:
                relevant_sessions.update(self.watched_processes[event['pid']]['sessions'])
            else:
                relevant_sessions.update(self.sessions.keys())
                
            # Notify sessions
            for session_id in relevant_sessions:
                if session_id in self.sessions and self.sessions[session_id]['active']:
                    event['session_id'] = session_id
                    
                    # Update session data
                    if event['type'] == 'process_metrics':
                        self.sessions[session_id]['process_metrics'][event['pid']] = event['metrics']
                    elif event['type'] in ['suspicious_process', 'resource_breach', 'process_exit']:
                        self.sessions[session_id]['suspicious_events'].append(event)
                        
                    # Notify event handlers
                    for handler in self.event_handlers:
                        try:
                            handler(event)
                        except Exception as e:
                            self.logger.error(f"Event handler error: {e}")
                            
        except Exception as e:
            self.logger.error(f"Failed to notify sessions: {e}")
            
    def get_session_metrics(self, session_id: str) -> Optional[Dict[int, Dict[str, Any]]]:
        """Get process metrics for a session"""
        try:
            if session_id in self.sessions:
                return self.sessions[session_id]['process_metrics']
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get session metrics: {e}")
            return None
            
    def get_session_events(self, session_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get process events for a session"""
        try:
            if session_id in self.sessions:
                return self.sessions[session_id]['suspicious_events']
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get session events: {e}")
            return None 
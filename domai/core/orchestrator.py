"""Security Orchestrator for DōmAI

Coordinates security monitoring, analysis, and response.
"""

import logging
import threading
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from queue import Queue
from pathlib import Path
import os

from ..monitoring.network import NetworkMonitor
from ..monitoring.process import ProcessMonitor
from ..monitoring.filesystem import FilesystemMonitor
from ..security.manager import SecurityManager
from ..api.bridge import BridgeManager

class MonitorState:
    """Monitor state tracking"""
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"

class SecurityOrchestrator:
    """Coordinates security components and manages system state"""
    
    def __init__(self, core_system, bridge_manager: BridgeManager):
        self._lock = threading.Lock()
        self.core = core_system
        self.bridge = bridge_manager
        self.security = SecurityManager()
        
        # Initialize monitors
        self.network_monitor = NetworkMonitor()
        self.process_monitor = ProcessMonitor()
        self.filesystem_monitor = FilesystemMonitor()
        
        # Monitor state tracking
        self.monitor_states: Dict[str, str] = {
            "network": MonitorState.STOPPED,
            "process": MonitorState.STOPPED,
            "filesystem": MonitorState.STOPPED
        }
        
        # Analysis queues
        self.analysis_queue = Queue()
        self.analysis_thread = None
        self.should_run = False
        
        # Session monitoring
        self.session_monitors: Dict[str, Dict[str, bool]] = {}
        
        # Setup logging
        self.logger = logging.getLogger("domai.orchestrator")
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Setup secure logging"""
        try:
            log_dir = Path("logs/orchestrator")
            log_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(log_dir, 0o700)
            
            log_file = log_dir / "orchestrator.log"
            log_file.touch(mode=0o600, exist_ok=True)
            
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
            
        except Exception as e:
            logging.error(f"Failed to setup logging: {e}")
        
    def start_monitoring(self) -> bool:
        """Initialize security monitoring"""
        try:
            self.logger.info("Starting security monitoring")
            
            with self._lock:
                # Start core monitors
                if not self._start_system_monitors():
                    return False
                
                # Begin analysis loop
                self.should_run = True
                self.analysis_thread = threading.Thread(
                    target=self._analysis_loop,
                    daemon=True
                )
                self.analysis_thread.start()
                
                self.logger.info("Security monitoring started successfully")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop all monitoring"""
        try:
            self.logger.info("Stopping security monitoring")
            
            with self._lock:
                self.should_run = False
                if self.analysis_thread:
                    self.analysis_thread.join(timeout=5)
                
                # Stop all monitors
                self._stop_system_monitors()
                
                # Clear session monitors
                for session_id in list(self.session_monitors.keys()):
                    self.stop_session_monitoring(session_id)
                
                self.logger.info("Security monitoring stopped successfully")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop monitoring: {e}")
            return False
    
    def start_session_monitoring(self, session_id: str,
                               monitors: Optional[List[str]] = None) -> bool:
        """Start monitoring for a specific session"""
        try:
            with self._lock:
                if session_id in self.session_monitors:
                    return True
                
                # Initialize session monitors
                self.session_monitors[session_id] = {
                    "network": False,
                    "process": False,
                    "filesystem": False
                }
                
                # Start requested monitors
                if not monitors:
                    monitors = ["network", "process", "filesystem"]
                
                for monitor in monitors:
                    if monitor == "network":
                        self.network_monitor.start_session(session_id)
                        self.session_monitors[session_id]["network"] = True
                    elif monitor == "process":
                        self.process_monitor.start_session(session_id)
                        self.session_monitors[session_id]["process"] = True
                    elif monitor == "filesystem":
                        self.filesystem_monitor.start_session(session_id)
                        self.session_monitors[session_id]["filesystem"] = True
                
                self.logger.info(f"Started session monitoring: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start session monitoring: {e}")
            return False
    
    def stop_session_monitoring(self, session_id: str) -> bool:
        """Stop monitoring for a specific session"""
        try:
            with self._lock:
                if session_id not in self.session_monitors:
                    return True
                
                # Stop session monitors
                if self.session_monitors[session_id]["network"]:
                    self.network_monitor.stop_session(session_id)
                if self.session_monitors[session_id]["process"]:
                    self.process_monitor.stop_session(session_id)
                if self.session_monitors[session_id]["filesystem"]:
                    self.filesystem_monitor.stop_session(session_id)
                
                # Remove session
                del self.session_monitors[session_id]
                
                self.logger.info(f"Stopped session monitoring: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop session monitoring: {e}")
            return False
    
    def process_security_event(self, event: dict) -> Dict[str, Any]:
        """Process and analyze security event"""
        try:
            session_id = event.get("session_id")
            if not session_id or session_id not in self.session_monitors:
                raise ValueError("Invalid session ID")
            
            # Update security state
            self._update_security_state(event)
            
            # Queue for analysis
            self.analysis_queue.put(event)
            
            # Get immediate response
            response = self._get_immediate_response(event)
            
            return {
                'status': 'success',
                'response': response,
                'queued_for_analysis': True
            }
            
        except Exception as e:
            self.logger.error(f"Event processing failed: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _start_system_monitors(self) -> bool:
        """Start system monitoring components"""
        try:
            # Start network monitoring
            self.monitor_states["network"] = MonitorState.STARTING
            if not self.network_monitor.start():
                self.logger.error("Failed to start network monitor")
                return False
            self.monitor_states["network"] = MonitorState.RUNNING
            
            # Start process monitoring
            self.monitor_states["process"] = MonitorState.STARTING
            if not self.process_monitor.start():
                self.logger.error("Failed to start process monitor")
                return False
            self.monitor_states["process"] = MonitorState.RUNNING
            
            # Start filesystem monitoring
            self.monitor_states["filesystem"] = MonitorState.STARTING
            if not self.filesystem_monitor.start():
                self.logger.error("Failed to start filesystem monitor")
                return False
            self.monitor_states["filesystem"] = MonitorState.RUNNING
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start system monitors: {e}")
            return False
    
    def _stop_system_monitors(self) -> None:
        """Stop system monitoring components"""
        try:
            # Stop network monitoring
            self.monitor_states["network"] = MonitorState.STOPPING
            self.network_monitor.stop()
            self.monitor_states["network"] = MonitorState.STOPPED
            
            # Stop process monitoring
            self.monitor_states["process"] = MonitorState.STOPPING
            self.process_monitor.stop()
            self.monitor_states["process"] = MonitorState.STOPPED
            
            # Stop filesystem monitoring
            self.monitor_states["filesystem"] = MonitorState.STOPPING
            self.filesystem_monitor.stop()
            self.monitor_states["filesystem"] = MonitorState.STOPPED
            
        except Exception as e:
            self.logger.error(f"Failed to stop system monitors: {e}")
    
    def _analysis_loop(self) -> None:
        """Main security analysis loop"""
        while self.should_run:
            try:
                # Process pending analysis tasks
                while not self.analysis_queue.empty():
                    event = self.analysis_queue.get_nowait()
                    try:
                        # Analyze event
                        analysis = self.core.ai_analyzer.analyze_security_event(
                            event,
                            self._build_security_context()
                        )
                        
                        # Handle results
                        self._handle_analysis_results(analysis)
                        
                        # Send through bridge
                        self.bridge.send_analysis_result(
                            event["session_id"],
                            analysis
                        )
                        
                    except Exception as e:
                        self.logger.error(f"Analysis task error: {e}")
                    finally:
                        self.analysis_queue.task_done()
                
                time.sleep(0.1)  # Prevent CPU spinning
                
            except Exception as e:
                self.logger.error(f"Analysis loop error: {e}")
                time.sleep(5)  # Back off on error
    
    def _update_security_state(self, event: dict) -> None:
        """Update current security state"""
        try:
            event_type = event.get("type", "unknown")
            session_id = event.get("session_id")
            
            if event_type == "network":
                self.network_monitor.handle_event(event)
            elif event_type == "process":
                self.process_monitor.handle_event(event)
            elif event_type == "filesystem":
                self.filesystem_monitor.handle_event(event)
            
            # Update session state
            if session_id in self.session_monitors:
                self.session_monitors[session_id][event_type] = True
                
        except Exception as e:
            self.logger.error(f"Failed to update security state: {e}")
    
    def _get_immediate_response(self, event: dict) -> Dict[str, Any]:
        """Get immediate response for event"""
        try:
            event_type = event.get("type", "unknown")
            severity = event.get("severity", "low")
            
            if severity == "critical":
                return {
                    'type': 'alert',
                    'message': f"Critical {event_type} event detected!",
                    'actions': self._get_critical_actions(event)
                }
            elif severity == "high":
                return {
                    'type': 'warning',
                    'message': f"High severity {event_type} event detected",
                    'recommendations': self._get_recommendations(event)
                }
            else:
                return {
                    'type': 'info',
                    'message': f"Monitoring {event_type} activity",
                    'details': event.get("details", {})
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get immediate response: {e}")
            return {
                'type': 'error',
                'message': "Error processing event"
            }
    
    def _get_critical_actions(self, event: dict) -> List[str]:
        """Get critical response actions"""
        event_type = event.get("type", "unknown")
        
        if event_type == "network":
            return [
                "Block suspicious connections",
                "Enable packet capture",
                "Analyze traffic patterns"
            ]
        elif event_type == "process":
            return [
                "Monitor process activity",
                "Check resource usage",
                "Analyze process relationships"
            ]
        elif event_type == "filesystem":
            return [
                "Monitor file changes",
                "Check file integrity",
                "Analyze access patterns"
            ]
        else:
            return ["Monitor system activity"]
    
    def _get_recommendations(self, event: dict) -> List[str]:
        """Get security recommendations"""
        event_type = event.get("type", "unknown")
        
        if event_type == "network":
            return [
                "Review network connections",
                "Check firewall rules",
                "Monitor network traffic"
            ]
        elif event_type == "process":
            return [
                "Review process activity",
                "Check system resources",
                "Monitor process behavior"
            ]
        elif event_type == "filesystem":
            return [
                "Review file changes",
                "Check file permissions",
                "Monitor file access"
            ]
        else:
            return ["Monitor system activity"]
    
    def _handle_analysis_results(self, analysis: Dict[str, Any]) -> None:
        """Handle analysis results"""
        try:
            # Update security state
            if analysis.get("threats"):
                self.security.handle_threats(analysis["threats"])
            
            # Update monitoring
            if analysis.get("monitoring_updates"):
                self._update_monitoring(analysis["monitoring_updates"])
            
            # Send notifications
            if analysis.get("notifications"):
                self._send_notifications(analysis["notifications"])
                
        except Exception as e:
            self.logger.error(f"Failed to handle analysis results: {e}")
    
    def _update_monitoring(self, updates: Dict[str, Any]) -> None:
        """Update monitoring based on analysis"""
        try:
            for monitor_type, config in updates.items():
                if monitor_type == "network":
                    self.network_monitor.update_config(config)
                elif monitor_type == "process":
                    self.process_monitor.update_config(config)
                elif monitor_type == "filesystem":
                    self.filesystem_monitor.update_config(config)
                    
        except Exception as e:
            self.logger.error(f"Failed to update monitoring: {e}")
    
    def _send_notifications(self, notifications: List[Dict[str, Any]]) -> None:
        """Send security notifications"""
        try:
            for notification in notifications:
                self.bridge.send_notification(
                    notification["session_id"],
                    notification["type"],
                    notification["message"],
                    notification.get("data", {})
                )
                
        except Exception as e:
            self.logger.error(f"Failed to send notifications: {e}")
    
    def _build_security_context(self) -> Dict[str, Any]:
        """Build current security context"""
        return {
            'timestamp': datetime.now(),
            'monitor_states': self.monitor_states,
            'session_monitors': self.session_monitors,
            'analysis_queue_size': self.analysis_queue.qsize()
        }

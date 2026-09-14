"""
Monitoring Manager for DōmAI
Coordinates all monitoring components
"""

import logging
import threading
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from pathlib import Path
import os
import json

from .network import NetworkMonitor
from .system import SystemMonitor
from .process import ProcessMonitor

class MonitoringManager:
    """Coordinates all monitoring components"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.active = False
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.event_handlers: List[callable] = []
        
        # Initialize monitors
        self.network_monitor = NetworkMonitor()
        self.system_monitor = SystemMonitor()
        self.process_monitor = ProcessMonitor()
        
        # Setup logging
        self.logger = logging.getLogger("domai.monitoring")
        self._setup_logging()
        
        # Register event handlers
        self._register_monitor_handlers()
        
    def _setup_logging(self) -> None:
        """Setup secure logging"""
        try:
            log_dir = Path("logs/monitoring")
            log_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(log_dir, 0o700)
            
            log_file = log_dir / "monitoring.log"
            log_file.touch(mode=0o600, exist_ok=True)
            
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
            
        except Exception as e:
            self.logger.error(f"Failed to setup monitoring logging: {e}")
            
    def _register_monitor_handlers(self) -> None:
        """Register event handlers for all monitors"""
        self.network_monitor.register_event_handler(self._handle_network_event)
        self.system_monitor.register_event_handler(self._handle_system_event)
        self.process_monitor.register_event_handler(self._handle_process_event)
        
    def start(self) -> bool:
        """Start all monitoring components"""
        try:
            with self._lock:
                if self.active:
                    return True
                    
                # Start all monitors
                if not all([
                    self.network_monitor.start(),
                    self.system_monitor.start(),
                    self.process_monitor.start()
                ]):
                    self.stop()  # Cleanup if any monitor fails to start
                    return False
                    
                self.active = True
                self.logger.info("Monitoring manager started")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start monitoring manager: {e}")
            return False
            
    def stop(self) -> None:
        """Stop all monitoring components"""
        try:
            with self._lock:
                self.active = False
                
                # Stop all monitors
                self.network_monitor.stop()
                self.system_monitor.stop()
                self.process_monitor.stop()
                
                # Archive all active sessions
                for session_id in list(self.sessions.keys()):
                    self._archive_session_data(session_id)
                    
                self.sessions.clear()
                self.logger.info("Monitoring manager stopped")
                
        except Exception as e:
            self.logger.error(f"Failed to stop monitoring manager: {e}")
            
    def start_session(self, session_id: str) -> bool:
        """Start monitoring for a session"""
        try:
            with self._lock:
                if session_id in self.sessions:
                    return True
                    
                # Start session in all monitors
                if not all([
                    self.network_monitor.start_session(session_id),
                    self.system_monitor.start_session(session_id),
                    self.process_monitor.start_session(session_id)
                ]):
                    self.stop_session(session_id)  # Cleanup if any monitor fails
                    return False
                    
                self.sessions[session_id] = {
                    'start_time': datetime.now(),
                    'events': [],
                    'active': True
                }
                
                self.logger.info(f"Started monitoring for session: {session_id}")
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
                    
                # Stop session in all monitors
                self.network_monitor.stop_session(session_id)
                self.system_monitor.stop_session(session_id)
                self.process_monitor.stop_session(session_id)
                
                # Archive session data
                self._archive_session_data(session_id)
                
                del self.sessions[session_id]
                
                self.logger.info(f"Stopped monitoring for session: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop session monitoring: {e}")
            return False
            
    def register_event_handler(self, handler: callable) -> None:
        """Register event handler"""
        self.event_handlers.append(handler)
        
    def _handle_network_event(self, event: Dict[str, Any]) -> None:
        """Handle network monitoring event"""
        try:
            session_id = event.get('session_id')
            if session_id and session_id in self.sessions:
                event['source'] = 'network'
                self.sessions[session_id]['events'].append(event)
                
                # Notify event handlers
                self._notify_handlers(event)
                
                # Log significant events
                if event['type'] != 'metrics':
                    self.logger.warning(
                        f"Network event: {event['type']} - {event.get('detail', '')}"
                    )
                    
                # Correlate with other monitors
                self._correlate_events(event)
                
        except Exception as e:
            self.logger.error(f"Failed to handle network event: {e}")
            
    def _handle_system_event(self, event: Dict[str, Any]) -> None:
        """Handle system monitoring event"""
        try:
            session_id = event.get('session_id')
            if session_id and session_id in self.sessions:
                event['source'] = 'system'
                self.sessions[session_id]['events'].append(event)
                
                # Notify event handlers
                self._notify_handlers(event)
                
                # Log significant events
                if event['type'] != 'metrics':
                    self.logger.warning(
                        f"System event: {event['type']} - {event.get('detail', '')}"
                    )
                    
                # Correlate with other monitors
                self._correlate_events(event)
                
        except Exception as e:
            self.logger.error(f"Failed to handle system event: {e}")
            
    def _handle_process_event(self, event: Dict[str, Any]) -> None:
        """Handle process monitoring event"""
        try:
            session_id = event.get('session_id')
            if session_id and session_id in self.sessions:
                event['source'] = 'process'
                self.sessions[session_id]['events'].append(event)
                
                # Notify event handlers
                self._notify_handlers(event)
                
                # Log significant events
                if event['type'] != 'process_metrics':
                    self.logger.warning(
                        f"Process event: {event['type']} - PID: {event.get('pid', 'N/A')}"
                    )
                    
                # Correlate with other monitors
                self._correlate_events(event)
                
        except Exception as e:
            self.logger.error(f"Failed to handle process event: {e}")
            
    def _correlate_events(self, event: Dict[str, Any]) -> None:
        """Correlate events across monitors"""
        try:
            session_id = event.get('session_id')
            if not session_id or session_id not in self.sessions:
                return
                
            # Get recent events for correlation
            recent_events = self._get_recent_events(session_id, minutes=5)
            
            # Correlate based on event type
            if event['type'] == 'suspicious_process':
                self._correlate_suspicious_process(event, recent_events)
            elif event['type'] == 'suspicious_traffic':
                self._correlate_suspicious_traffic(event, recent_events)
            elif event['type'] == 'threshold_breach':
                self._correlate_threshold_breach(event, recent_events)
                
        except Exception as e:
            self.logger.error(f"Failed to correlate events: {e}")
            
    def _get_recent_events(self, session_id: str, minutes: int = 5) -> List[Dict[str, Any]]:
        """Get recent events for correlation"""
        try:
            cutoff_time = datetime.now().timestamp() - (minutes * 60)
            return [
                event for event in self.sessions[session_id]['events']
                if event['timestamp'].timestamp() > cutoff_time
            ]
        except Exception:
            return []
            
    def _correlate_suspicious_process(self, event: Dict[str, Any],
                                    recent_events: List[Dict[str, Any]]) -> None:
        """Correlate suspicious process events"""
        try:
            # Look for related network activity
            related_network = [
                e for e in recent_events
                if e['source'] == 'network'
                and e['type'] == 'suspicious_traffic'
                and e.get('process', {}).get('pid') == event['process']['pid']
            ]
            
            if related_network:
                self._generate_correlation_event(
                    'process_network_correlation',
                    event,
                    related_network
                )
                
        except Exception as e:
            self.logger.error(f"Failed to correlate suspicious process: {e}")
            
    def _correlate_suspicious_traffic(self, event: Dict[str, Any],
                                    recent_events: List[Dict[str, Any]]) -> None:
        """Correlate suspicious traffic events"""
        try:
            # Look for related process activity
            related_process = [
                e for e in recent_events
                if e['source'] == 'process'
                and e['type'] == 'suspicious_process'
                and e.get('process', {}).get('connections', [])
            ]
            
            if related_process:
                self._generate_correlation_event(
                    'traffic_process_correlation',
                    event,
                    related_process
                )
                
        except Exception as e:
            self.logger.error(f"Failed to correlate suspicious traffic: {e}")
            
    def _correlate_threshold_breach(self, event: Dict[str, Any],
                                  recent_events: List[Dict[str, Any]]) -> None:
        """Correlate threshold breach events"""
        try:
            # Look for related breaches
            related_breaches = [
                e for e in recent_events
                if e['type'] == 'threshold_breach'
                and e['resource'] != event['resource']
            ]
            
            if len(related_breaches) >= 2:
                self._generate_correlation_event(
                    'multiple_threshold_correlation',
                    event,
                    related_breaches
                )
                
        except Exception as e:
            self.logger.error(f"Failed to correlate threshold breach: {e}")
            
    def _generate_correlation_event(self, correlation_type: str,
                                  trigger_event: Dict[str, Any],
                                  related_events: List[Dict[str, Any]]) -> None:
        """Generate correlation event"""
        try:
            event = {
                'timestamp': datetime.now(),
                'type': 'correlation',
                'correlation_type': correlation_type,
                'trigger_event': trigger_event,
                'related_events': related_events,
                'session_id': trigger_event.get('session_id'),
                'source': 'correlation'
            }
            
            # Add to session events
            if event['session_id'] in self.sessions:
                self.sessions[event['session_id']]['events'].append(event)
                
            # Notify handlers
            self._notify_handlers(event)
            
            self.logger.warning(
                f"Correlation event: {correlation_type} - Session: {event['session_id']}"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate correlation event: {e}")
            
    def _notify_handlers(self, event: Dict[str, Any]) -> None:
        """Notify all event handlers"""
        for handler in self.event_handlers:
            try:
                handler(event)
            except Exception as e:
                self.logger.error(f"Event handler error: {e}")
                
    def _archive_session_data(self, session_id: str) -> None:
        """Archive session monitoring data"""
        try:
            if session_id not in self.sessions:
                return
                
            # Prepare archive data
            archive_data = {
                'session_id': session_id,
                'start_time': self.sessions[session_id]['start_time'].isoformat(),
                'end_time': datetime.now().isoformat(),
                'events': self.sessions[session_id]['events'],
                'network_metrics': self.network_monitor.get_session_metrics(session_id),
                'system_metrics': self.system_monitor.get_session_metrics(session_id),
                'process_metrics': self.process_monitor.get_session_metrics(session_id)
            }
            
            # Create archive directory
            archive_dir = Path("logs/archive")
            archive_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(archive_dir, 0o700)
            
            # Save archive file
            archive_file = archive_dir / f"session_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(archive_file, 'w') as f:
                json.dump(archive_data, f, indent=2)
            os.chmod(archive_file, 0o600)
            
            self.logger.info(f"Archived monitoring data for session: {session_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to archive session data: {e}")
            
    def get_session_events(self, session_id: str,
                          event_types: Optional[List[str]] = None,
                          sources: Optional[List[str]] = None) -> Optional[List[Dict[str, Any]]]:
        """Get filtered events for a session"""
        try:
            if session_id not in self.sessions:
                return None
                
            events = self.sessions[session_id]['events']
            
            # Filter by event type
            if event_types:
                events = [e for e in events if e['type'] in event_types]
                
            # Filter by source
            if sources:
                events = [e for e in events if e['source'] in sources]
                
            return events
            
        except Exception as e:
            self.logger.error(f"Failed to get session events: {e}")
            return None
            
    def get_session_metrics(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get all metrics for a session"""
        try:
            if session_id not in self.sessions:
                return None
                
            return {
                'network': self.network_monitor.get_session_metrics(session_id),
                'system': self.system_monitor.get_session_metrics(session_id),
                'process': self.process_monitor.get_session_metrics(session_id)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get session metrics: {e}")
            return None
            
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get monitoring summary for a session"""
        try:
            if session_id not in self.sessions:
                return None
                
            events = self.sessions[session_id]['events']
            
            # Count events by type and source
            event_counts = {}
            source_counts = {}
            
            for event in events:
                event_type = event['type']
                source = event['source']
                
                event_counts[event_type] = event_counts.get(event_type, 0) + 1
                source_counts[source] = source_counts.get(source, 0) + 1
                
            return {
                'session_id': session_id,
                'start_time': self.sessions[session_id]['start_time'].isoformat(),
                'duration': (datetime.now() - self.sessions[session_id]['start_time']).seconds,
                'total_events': len(events),
                'event_counts': event_counts,
                'source_counts': source_counts,
                'active': self.sessions[session_id]['active']
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get session summary: {e}")
            return None 
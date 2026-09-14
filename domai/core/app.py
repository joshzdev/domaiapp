"""
DōmAI Core Application Manager
Central orchestration of all DōmAI components
"""

import logging
import threading
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import os

from ..security.manager import SecurityManager
from ..monitoring.manager import MonitoringManager
from ..api.bridge import BridgeManager
from ..api.ipc import IPCHandler
from ..api.security import SecurityContext

class DomaiApp:
    """Core DōmAI application manager"""

    def __init__(self):
        # Initialize managers
        self._lock = threading.Lock()
        self.security = SecurityManager()
        self.monitoring = MonitoringManager()
        self.bridge = BridgeManager()
        self.ipc = IPCHandler()
        self.logger = logging.getLogger("domai.core")
        
        # Configure core logging
        self._setup_logging()
        
        # Application state
        self.state: Dict[str, Any] = {
            "initialized": False,
            "components": {},
            "config": {},
            "sessions": {}
        }
        
        # Start IPC handler
        self.ipc.start()
        
        # Register bridge handlers
        self._register_bridge_handlers()

    def _setup_logging(self) -> None:
        """Configure core application logging"""
        log_dir = Path("logs/core")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Secure log directory
        os.chmod(log_dir, 0o700)
        
        # Setup log file
        log_file = log_dir / "core.log"
        log_file.touch(mode=0o600, exist_ok=True)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Initialize the application"""
        try:
            self.logger.info("Initializing DōmAI application")
            
            with self._lock:
                # Load configuration
                self.state["config"] = config or {}
                
                # Initialize security
                self.state["components"]["security"] = {
                    "status": "initializing"
                }
                if not self._initialize_security():
                    return False
                self.state["components"]["security"]["status"] = "ready"
                
                # Initialize monitoring
                self.state["components"]["monitoring"] = {
                    "status": "initializing"
                }
                if not self._initialize_monitoring():
                    return False
                self.state["components"]["monitoring"]["status"] = "ready"
                
                # Initialize bridge
                self.state["components"]["bridge"] = {
                    "status": "initializing"
                }
                if not self._initialize_bridge():
                    return False
                self.state["components"]["bridge"]["status"] = "ready"
                
                self.state["initialized"] = True
                self.logger.info("DōmAI application initialized successfully")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}")
            return False

    def shutdown(self) -> bool:
        """Gracefully shutdown the application"""
        try:
            self.logger.info("Shutting down DōmAI application")
            
            with self._lock:
                # Stop monitoring
                for monitor_type in self.monitoring.get_active_monitors():
                    self.monitoring.stop_monitoring(monitor_type)
                
                # Stop bridge
                self.bridge.stop()
                
                # Stop IPC
                self.ipc.stop()
                
                # Cleanup security
                self._cleanup_security()
                
                # Clear state
                self.state["initialized"] = False
                self.state["components"].clear()
                self.state["sessions"].clear()
                
                self.logger.info("DōmAI application shutdown complete")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to shutdown application: {e}")
            return False

    def create_session(self, user_id: str, user_level: str) -> str:
        """Create new user session"""
        try:
            with self._lock:
                # Create security context
                context = SecurityContext(
                    user_id=user_id,
                    user_level=user_level,
                    timestamp=datetime.now()
                )
                
                # Create session
                session_id = self.security.create_session(context)
                
                # Store session
                self.state["sessions"][session_id] = {
                    "context": context,
                    "created": datetime.now(),
                    "last_activity": datetime.now()
                }
                
                return session_id
                
        except Exception as e:
            self.logger.error(f"Failed to create session: {e}")
            raise

    def close_session(self, session_id: str) -> bool:
        """Close user session"""
        try:
            with self._lock:
                if session_id not in self.state["sessions"]:
                    return False
                    
                # Cleanup session resources
                self.security.close_session(session_id)
                self.monitoring.stop_session_monitoring(session_id)
                self.bridge.close_session(session_id)
                
                # Remove session
                del self.state["sessions"][session_id]
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to close session: {e}")
            return False

    def handle_security_event(self, event: Dict[str, Any]) -> bool:
        """Handle security events"""
        try:
            # Validate session
            session_id = event.get("session_id")
            if not self._validate_session(session_id):
                return False
                
            # Log the event
            self.security.audit_log(
                event.get("user_id", "system"),
                event.get("action", "unknown"),
                event.get("details", {})
            )
            
            # Handle based on event type
            event_type = event.get("type", "unknown")
            if event_type == "auth":
                return self._handle_auth_event(event)
            elif event_type == "permission":
                return self._handle_permission_event(event)
            elif event_type == "monitoring":
                return self._handle_monitoring_event(event)
            else:
                self.logger.warning(f"Unknown event type: {event_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to handle security event: {e}")
            return False

    def _initialize_security(self) -> bool:
        """Initialize security components"""
        try:
            # Initialize security manager
            if not self.security.initialize():
                return False
                
            # Register security handlers
            self.bridge.register_handler(
                "security_event",
                self.handle_security_event
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Security initialization failed: {e}")
            return False

    def _initialize_monitoring(self) -> bool:
        """Initialize monitoring components"""
        try:
            # Start default monitoring
            self.monitoring.start_monitoring("network", {})
            self.monitoring.start_monitoring("process", {})
            self.monitoring.start_monitoring("filesystem", {})
            
            # Register monitoring handlers
            self.bridge.register_handler(
                "monitoring_event",
                self.monitoring.handle_event
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Monitoring initialization failed: {e}")
            return False

    def _initialize_bridge(self) -> bool:
        """Initialize native bridge"""
        try:
            return self.bridge.initialize()
        except Exception as e:
            self.logger.error(f"Bridge initialization failed: {e}")
            return False

    def _register_bridge_handlers(self) -> None:
        """Register native bridge message handlers"""
        self.bridge.register_handler(
            "create_session",
            lambda msg: self.create_session(
                msg["user_id"],
                msg["user_level"]
            )
        )
        
        self.bridge.register_handler(
            "close_session",
            lambda msg: self.close_session(msg["session_id"])
        )
        
        self.bridge.register_handler(
            "security_event",
            self.handle_security_event
        )

    def _validate_session(self, session_id: str) -> bool:
        """Validate session exists and is active"""
        with self._lock:
            if session_id not in self.state["sessions"]:
                return False
                
            # Update last activity
            self.state["sessions"][session_id]["last_activity"] = datetime.now()
            return True

    def _cleanup_security(self) -> None:
        """Cleanup security state"""
        try:
            # Close all sessions
            with self._lock:
                for session_id in list(self.state["sessions"].keys()):
                    self.close_session(session_id)
                    
            # Cleanup security manager
            self.security.cleanup()
            
        except Exception as e:
            self.logger.error(f"Security cleanup failed: {e}")

    def _handle_auth_event(self, event: Dict[str, Any]) -> bool:
        """Handle authentication events"""
        try:
            action = event.get("action")
            if action == "login":
                return bool(self.security.authenticate(event.get("credentials", {})))
            elif action == "logout":
                return self.close_session(event.get("session_id"))
            return False
        except Exception as e:
            self.logger.error(f"Failed to handle auth event: {e}")
            return False

    def _handle_permission_event(self, event: Dict[str, Any]) -> bool:
        """Handle permission events"""
        try:
            action = event.get("action")
            user_id = event.get("user_id")
            if action == "elevate":
                return self.security.elevate_permissions(
                    user_id,
                    event.get("permission")
                )
            elif action == "revoke":
                return self.security.revoke_permissions(
                    user_id,
                    event.get("permission")
                )
            return False
        except Exception as e:
            self.logger.error(f"Failed to handle permission event: {e}")
            return False

    def _handle_monitoring_event(self, event: Dict[str, Any]) -> bool:
        """Handle monitoring events"""
        try:
            action = event.get("action")
            if action == "start":
                return self.monitoring.start_monitoring(
                    event.get("monitor_type", ""),
                    event.get("config", {})
                )
            elif action == "stop":
                return self.monitoring.stop_monitoring(
                    event.get("monitor_type", "")
                )
            return False
        except Exception as e:
            self.logger.error(f"Failed to handle monitoring event: {e}")
            return False 
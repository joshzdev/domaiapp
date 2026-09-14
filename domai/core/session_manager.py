"""
Session Manager for DōmAI
Manages user sessions and preferences for MacOS security interactions
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid

@dataclass
class UserPreferences:
    """User preferences for security interactions"""
    technical_level: str = "beginner"  # beginner, intermediate, advanced
    command_confirmation: bool = True  # require confirmation for commands
    education_detail: str = "basic"    # basic, detailed, comprehensive
    notification_preferences: Dict[str, bool] = field(default_factory=lambda: {
        "security_alerts": True,
        "command_execution": True,
        "education_updates": True
    })

@dataclass
class SessionData:
    """Session data for user interaction"""
    session_id: str
    created_at: datetime
    last_activity: datetime
    preferences: UserPreferences
    context: Dict[str, Any] = field(default_factory=dict)
    command_history: list[str] = field(default_factory=list)

class SessionManager:
    """Manages user sessions and preferences"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}
        self.logger = logging.getLogger("domai.session")
        self.session_timeout = timedelta(hours=24)
        
    def create_session(self, preferences: Optional[UserPreferences] = None) -> str:
        """Create new user session"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        self.sessions[session_id] = SessionData(
            session_id=session_id,
            created_at=now,
            last_activity=now,
            preferences=preferences or UserPreferences()
        )
        
        return session_id
        
    def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session data if valid"""
        if session_id not in self.sessions:
            return None
            
        session = self.sessions[session_id]
        if self._is_session_expired(session):
            self.end_session(session_id)
            return None
            
        return session
        
    def update_session(self, session_id: str, **kwargs) -> bool:
        """Update session data"""
        session = self.get_session(session_id)
        if not session:
            return False
            
        # Update last activity
        session.last_activity = datetime.now()
        
        # Update provided fields
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
            elif key in session.context:
                session.context[key] = value
                
        return True
        
    def update_preferences(self, session_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences"""
        session = self.get_session(session_id)
        if not session:
            return False
            
        # Update individual preference fields
        for key, value in preferences.items():
            if hasattr(session.preferences, key):
                setattr(session.preferences, key, value)
                
        return True
        
    def add_command_history(self, session_id: str, command: str) -> bool:
        """Add command to session history"""
        session = self.get_session(session_id)
        if not session:
            return False
            
        session.command_history.append(command)
        return True
        
    def get_command_history(self, session_id: str) -> list[str]:
        """Get command history for session"""
        session = self.get_session(session_id)
        return session.command_history if session else []
        
    def end_session(self, session_id: str) -> bool:
        """End user session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
        
    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions"""
        expired_count = 0
        current_sessions = list(self.sessions.keys())
        
        for session_id in current_sessions:
            session = self.sessions[session_id]
            if self._is_session_expired(session):
                self.end_session(session_id)
                expired_count += 1
                
        return expired_count
        
    def _is_session_expired(self, session: SessionData) -> bool:
        """Check if session has expired"""
        return datetime.now() - session.last_activity > self.session_timeout 
#!/usr/bin/env python3
"""
FortressNexus: Core Security and Management System for DōmAI

Implements a security-first architecture that:
- Manages secure communication between components
- Handles authentication and session management
- Protects against common attack vectors
- Maintains encrypted audit logs
"""

import secrets
import hashlib
import logging
import threading
import time
from datetime import datetime
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from pathlib import Path
import os
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

@dataclass
class SecuritySession:
    id: str
    created_at: datetime
    last_rotated: datetime
    user_level: str
    security_tokens: Dict[str, str]
    command_history: List[Dict[str, Any]]
    resource_limits: Dict[str, int]

class FortressNexus:
    """Core security management system"""

    # Commands that require special validation
    HIGH_RISK_COMMANDS = {
        'network': ['tcpdump', 'wireshark', 'nmap'],
        'system': ['ps', 'top', 'lsof'],
        'file': ['find', 'grep', 'stat']
    }

    # Patterns for command injection prevention
    DANGEROUS_PATTERNS = [
        r'[;&|]',           # Command chaining
        r'[><]',            # Redirections
        r'\$[\(\{]',        # Command substitution
        r'`.*`',            # Backtick execution
        r'\bsudo\b',        # Privilege escalation
        r'\bsu\b',          # User switching
        r'\benv\b',         # Environment manipulation
        r'\bsource\b',      # Script sourcing
        r'\beval\b',        # String evaluation
        r'\bexec\b',        # Process execution
        r'\bchmod\b',       # Permission changes
        r'\bchown\b',       # Ownership changes
        r'\brm\b',          # File deletion
        r'\bmv\b',          # File moving
        r'\bcp\b',          # File copying
        r'\bcat\b > ',      # File writing
        r'\becho\b.+>',     # File writing
        r'\bwrite\b',       # Terminal writing
        r'\bkill\b',        # Process termination
        r'\bpkill\b',       # Process killing
        r'\breboot\b',      # System reboot
        r'\bshutdown\b',    # System shutdown
        r'\bpasswd\b',      # Password changes
        r'\badduser\b',     # User addition
        r'\buseradd\b',     # User addition
        r'\bchsh\b',        # Shell changes
        r'\bchfn\b',        # Finger information
        r'\bvisudo\b',      # Sudoers editing
        r'\bdscl\b',        # Directory services
        r'\blaunchctl\b',   # Service management
        r'\bsystemctl\b',   # Service control
        r'\bservice\b',     # Service management
        r'\bnetstat\b -',   # Network statistics
        r'\biftop\b',       # Network monitoring
        r'\btcpdump\b -w',  # Packet capture
        r'\bwireshark\b',   # Packet analysis
        r'\blsof\b -i',     # Network connections
        r'\bnetcat\b',      # Network utility
        r'\bnc\b',          # Network utility
        r'\bcurl\b.*-o',    # File download
        r'\bwget\b',        # File download
        r'\bftp\b',         # File transfer
        r'\bsftp\b',        # Secure file transfer
        r'\bscp\b',         # Secure copy
        r'\brsync\b',       # File synchronization
        r'\bunzip\b',       # Archive extraction
        r'\bunrar\b',       # Archive extraction
        r'\btar\b',         # Archive manipulation
        r'\bbase64\b',      # Encoding/decoding
        r'\bperl\b.*-e',    # Perl execution
        r'\bpython\b.*-c',  # Python execution
        r'\bruby\b.*-e',    # Ruby execution
        r'\bnode\b.*-e',    # Node.js execution
        r'\bphp\b.*-r',     # PHP execution
        r'\bash\b.*-c',     # Shell execution
        r'\bzsh\b.*-c',     # Shell execution
        r'\bksh\b.*-c',     # Shell execution
        r'\bcsh\b.*-c',     # Shell execution
        r'\btcsh\b.*-c',    # Shell execution
        r'\bfish\b.*-c'     # Shell execution
    ]

    def __init__(self):
        self._lock = threading.Lock()
        self.active_sessions: Dict[str, SecuritySession] = {}
        self.security_log = self._setup_secure_logging()
        self.command_validators = self._initialize_validators()
        
        # Separate public and internal state
        self._internal_state = {}
        self.public_state = {}
        
        # Start cleanup thread
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_expired_sessions,
            daemon=True
        )
        self._cleanup_thread.start()
        
    def _setup_secure_logging(self) -> logging.Logger:
        """Setup encrypted logging"""
        try:
            # Create secure log directory
            log_dir = Path("logs/security")
            log_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(log_dir, 0o700)
            
            # Generate encryption key
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(b"domai-security-logs"))
            self.fernet = Fernet(key)
            
            # Setup encrypted file handler
            class EncryptedFileHandler(logging.FileHandler):
                def __init__(self, filename, mode='a', encoding=None, delay=False, fernet=None):
                    super().__init__(filename, mode, encoding, delay)
                    self.fernet = fernet
                    
                def emit(self, record):
                    try:
                        msg = self.format(record)
                        encrypted = self.fernet.encrypt(msg.encode())
                        self.stream.write(encrypted.decode() + '\n')
                        self.flush()
                    except Exception:
                        self.handleError(record)
            
            # Configure logger
            logger = logging.getLogger('domai.security')
            log_file = log_dir / "security.encrypted.log"
            handler = EncryptedFileHandler(log_file, fernet=self.fernet)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            
            return logger
            
        except Exception as e:
            logging.error(f"Failed to setup secure logging: {e}")
            return logging.getLogger('domai.security')
        
    def create_secure_session(self, user_level: str = 'novice') -> SecuritySession:
        """Create new session with security measures"""
        session_id = self._generate_secure_id()
        session = SecuritySession(
            id=session_id,
            created_at=datetime.now(),
            last_rotated=datetime.now(),
            user_level=user_level,
            security_tokens=self._generate_security_tokens(),
            command_history=[],
            resource_limits=self._get_resource_limits(user_level)
        )
        
        with self._lock:
            self.active_sessions[session_id] = session
            self.security_log.info(
                f"New session created: {session_id[:8]}... "
                f"[level={user_level}]"
            )
        
        return session

    def validate_command(self, session_id: str, command: str) -> bool:
        """Validate command with multiple security checks"""
        if not self._validate_session(session_id):
            return False
            
        with self._lock:
            session = self.active_sessions[session_id]
            
            # Check for dangerous patterns
            if self._contains_dangerous_pattern(command):
                self.security_log.warning(
                    f"Dangerous pattern detected in command: {command[:50]}..."
                )
                return False
            
            # Run all validators
            for validator in self.command_validators:
                if not validator(command, session):
                    self.security_log.warning(
                        f"Command validation failed: {command[:50]}..."
                    )
                    return False
                    
            # Track command in session history
            session.command_history.append({
                'command': command,
                'timestamp': datetime.now(),
                'validated': True
            })
            
            return True

    def _generate_secure_id(self) -> str:
        """Generate cryptographically secure session ID"""
        return secrets.token_urlsafe(32)

    def _generate_security_tokens(self) -> Dict[str, str]:
        """Generate security tokens for CSRF protection etc"""
        return {
            'csrf': secrets.token_urlsafe(32),
            'stream': secrets.token_urlsafe(32),
            'command': secrets.token_urlsafe(32)
        }

    def _validate_session(self, session_id: str) -> bool:
        """Validate session and handle rotation"""
        with self._lock:
            if session_id not in self.active_sessions:
                return False
                
            session = self.active_sessions[session_id]
            
            # Check session age and rotate if needed
            age = datetime.now() - session.last_rotated
            if age.total_seconds() > 3600:  # 1 hour
                self._rotate_session(session)
                
            return True

    def _rotate_session(self, session: SecuritySession) -> None:
        """Rotate session tokens for security"""
        # Generate new tokens
        new_tokens = self._generate_security_tokens()
        
        # Keep old tokens valid briefly for smooth transition
        old_tokens = session.security_tokens
        session.security_tokens = {
            **new_tokens,
            **{f"old_{k}": v for k, v in old_tokens.items()}
        }
        
        session.last_rotated = datetime.now()
        
        # Schedule cleanup of old tokens
        cleanup_thread = threading.Thread(
            target=self._cleanup_old_tokens,
            args=(session,),
            daemon=True
        )
        cleanup_thread.start()

    def _cleanup_old_tokens(self, session: SecuritySession) -> None:
        """Remove old tokens after grace period"""
        time.sleep(300)  # 5 minute grace period
        
        with self._lock:
            if session.id in self.active_sessions:
                session.security_tokens = {
                    k: v for k, v in session.security_tokens.items()
                    if not k.startswith('old_')
                }

    def _cleanup_expired_sessions(self) -> None:
        """Cleanup expired sessions periodically"""
        while True:
            try:
                with self._lock:
                    now = datetime.now()
                    expired = [
                        sid for sid, session in self.active_sessions.items()
                        if (now - session.last_rotated).total_seconds() > 7200  # 2 hours
                    ]
                    for sid in expired:
                        del self.active_sessions[sid]
                        self.security_log.info(f"Expired session removed: {sid[:8]}...")
            except Exception as e:
                self.security_log.error(f"Session cleanup error: {e}")
            finally:
                time.sleep(300)  # Check every 5 minutes

    def _initialize_validators(self):
        """Initialize command validation functions"""
        return [
            self._validate_command_syntax,
            self._validate_command_permissions,
            self._validate_resource_limits,
            self._validate_security_impact
        ]

    def _contains_dangerous_pattern(self, command: str) -> bool:
        """Check for dangerous command patterns"""
        return any(re.search(pattern, command) for pattern in self.DANGEROUS_PATTERNS)

    def _validate_command_syntax(self, command: str, session: SecuritySession) -> bool:
        """Validate command syntax and check for injection"""
        try:
            # Basic command structure validation
            parts = command.split()
            if not parts:
                return False
                
            # Check base command
            base_cmd = parts[0].lower()
            
            # Check for high-risk commands
            for category, commands in self.HIGH_RISK_COMMANDS.items():
                if base_cmd in commands:
                    return self._validate_high_risk_command(
                        command, category, session
                    )
                    
            return True
            
        except Exception as e:
            self.security_log.error(f"Command syntax validation error: {e}")
            return False

    def _validate_command_permissions(self, command: str, session: SecuritySession) -> bool:
        """Validate user has permission for command"""
        try:
            base_cmd = command.split()[0].lower()
            
            # Check user level permissions
            if session.user_level == 'novice':
                return base_cmd not in sum(self.HIGH_RISK_COMMANDS.values(), [])
            elif session.user_level == 'advanced':
                return not any(
                    base_cmd in cmds 
                    for category, cmds in self.HIGH_RISK_COMMANDS.items()
                    if category in ['system']
                )
                
            return True  # Expert level
            
        except Exception as e:
            self.security_log.error(f"Permission validation error: {e}")
            return False

    def _validate_resource_limits(self, command: str, session: SecuritySession) -> bool:
        """Validate command won't exceed resource limits"""
        try:
            # Check command history count
            if len(session.command_history) >= session.resource_limits['max_commands']:
                return False
                
            # Check command frequency
            recent_commands = [
                cmd for cmd in session.command_history
                if (datetime.now() - cmd['timestamp']).total_seconds() < 60
            ]
            if len(recent_commands) >= session.resource_limits['commands_per_minute']:
                return False
                
            return True
            
        except Exception as e:
            self.security_log.error(f"Resource limit validation error: {e}")
            return False

    def _validate_security_impact(self, command: str, session: SecuritySession) -> bool:
        """Validate command's security impact"""
        try:
            base_cmd = command.split()[0].lower()
            
            # Check for system-critical commands
            if base_cmd in ['shutdown', 'reboot', 'halt']:
                return False
                
            # Check for sensitive data access
            if any(pattern in command.lower() for pattern in [
                'password', 'secret', 'key', 'token', 'credential'
            ]):
                return False
                
            # Check for sensitive file access
            if any(pattern in command.lower() for pattern in [
                '/etc/shadow', '/etc/passwd', '/etc/sudoers',
                '.ssh/', 'id_rsa', 'id_dsa'
            ]):
                return False
                
            return True
            
        except Exception as e:
            self.security_log.error(f"Security impact validation error: {e}")
            return False

    def _validate_high_risk_command(self, command: str, category: str,
                                  session: SecuritySession) -> bool:
        """Validate high-risk command usage"""
        try:
            # Check user expertise level
            if session.user_level == 'novice':
                return False
                
            # Check command history for similar commands
            similar_commands = [
                cmd for cmd in session.command_history
                if any(risky in cmd['command'] 
                      for risky in self.HIGH_RISK_COMMANDS[category])
            ]
            
            # Limit frequency of high-risk commands
            if len(similar_commands) >= session.resource_limits['high_risk_commands']:
                return False
                
            return True
            
        except Exception as e:
            self.security_log.error(f"High-risk command validation error: {e}")
            return False

    def _get_resource_limits(self, user_level: str) -> Dict[str, int]:
        """Get resource limits based on user level"""
        if user_level == 'novice':
            return {
                'max_commands': 100,
                'commands_per_minute': 10,
                'high_risk_commands': 0
            }
        elif user_level == 'advanced':
            return {
                'max_commands': 500,
                'commands_per_minute': 30,
                'high_risk_commands': 5
            }
        else:  # Expert
            return {
                'max_commands': 1000,
                'commands_per_minute': 60,
                'high_risk_commands': 15
            }
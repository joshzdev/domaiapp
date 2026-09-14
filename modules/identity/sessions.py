"""
Session monitoring module
Handles login and session monitoring
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

class SessionMonitor:
    """Monitor user login sessions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get currently active user sessions"""
        try:
            # Use w command for detailed session info
            cmd = ["w", "-h"]  # -h to omit header
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"w command failed: {proc.stderr}")
                
            return self._parse_w_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting active sessions: {str(e)}")
            return []
            
    def get_user_sessions(self, username: str) -> List[Dict[str, Any]]:
        """Get sessions for specific user"""
        try:
            # Use w command filtered for user
            cmd = ["w", "-h", username]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"w command failed: {proc.stderr}")
                
            return self._parse_w_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting user sessions: {str(e)}")
            return []
            
    def get_session_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get session history"""
        try:
            # Use last command
            cmd = ["last", "-100"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"last command failed: {proc.stderr}")
                
            return self._parse_last_output(proc.stdout, limit)
            
        except Exception as e:
            self.logger.error(f"Error getting session history: {str(e)}")
            return []
            
    def get_failed_logins(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get failed login attempts"""
        try:
            # Use lastb command
            cmd = ["lastb", "-100"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"lastb command failed: {proc.stderr}")
                
            return self._parse_last_output(proc.stdout, limit)
            
        except Exception as e:
            self.logger.error(f"Error getting failed logins: {str(e)}")
            return []
            
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        try:
            stats = {
                "active_sessions": 0,
                "unique_users": set(),
                "by_type": {},
                "by_host": {}
            }
            
            # Get active sessions
            sessions = self.get_active_sessions()
            
            # Process sessions
            for session in sessions:
                stats["active_sessions"] += 1
                stats["unique_users"].add(session["user"])
                
                # Count by type
                session_type = session.get("type", "unknown")
                stats["by_type"][session_type] = stats["by_type"].get(session_type, 0) + 1
                
                # Count by host
                if "from" in session:
                    host = session["from"]
                    stats["by_host"][host] = stats["by_host"].get(host, 0) + 1
                    
            # Convert set to list for JSON serialization
            stats["unique_users"] = list(stats["unique_users"])
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting session stats: {str(e)}")
            return {}
            
    def _parse_w_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse w command output"""
        sessions = []
        
        try:
            for line in output.strip().split("\n"):
                if not line:
                    continue
                    
                parts = line.split()
                if len(parts) >= 8:
                    session = {
                        "user": parts[0],
                        "tty": parts[1],
                        "from": parts[2],
                        "login_at": parts[3],
                        "idle": parts[4],
                        "jcpu": parts[5],
                        "pcpu": parts[6],
                        "what": " ".join(parts[7:])
                    }
                    
                    # Determine session type
                    if session["tty"].startswith("pts"):
                        session["type"] = "ssh" if session["from"] != "-" else "terminal"
                    elif session["tty"].startswith("tty"):
                        session["type"] = "console"
                    else:
                        session["type"] = "other"
                        
                    sessions.append(session)
                    
        except Exception as e:
            self.logger.error(f"Error parsing w output: {str(e)}")
            
        return sessions
        
    def _parse_last_output(self, output: str, limit: int) -> List[Dict[str, Any]]:
        """Parse last/lastb command output"""
        sessions = []
        count = 0
        
        try:
            for line in output.strip().split("\n"):
                if not line or "wtmp begins" in line:
                    continue
                    
                if count >= limit:
                    break
                    
                parts = line.split()
                if len(parts) >= 9:
                    session = {
                        "user": parts[0],
                        "terminal": parts[1],
                        "host": parts[2] if parts[2] != ":" else None,
                        "date": " ".join(parts[3:8]),
                        "duration": parts[8] if parts[8] != "still" else "active"
                    }
                    
                    # Parse date
                    try:
                        session["timestamp"] = datetime.strptime(
                            session["date"],
                            "%a %b %d %H:%M:%S %Y"
                        )
                    except ValueError:
                        session["timestamp"] = None
                        
                    sessions.append(session)
                    count += 1
                    
        except Exception as e:
            self.logger.error(f"Error parsing last output: {str(e)}")
            
        return sessions 
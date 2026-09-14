#!/usr/bin/env python3
"""
DōmAI Dual-Stream Manager
Handles bifurcated output streams while maintaining unified context
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import uuid
import logging
import subprocess
import threading
import queue
from enum import Enum
import weakref

class StreamType(Enum):
    CRISIS = "crisis"
    KNOWLEDGE = "knowledge"

@dataclass
class SecurityContext:
    """Unified context for both streams"""
    session_id: str
    start_time: datetime
    user_proficiency: str
    current_analysis: Dict[str, Any]
    command_history: List[Dict[str, Any]]
    findings: List[Dict[str, Any]]
    learning_opportunities: List[Dict[str, Any]]
    last_activity: datetime = datetime.now()

@dataclass
class StreamOutput:
    """Output for a specific stream"""
    stream_type: StreamType
    content: str
    timestamp: datetime
    context_id: str
    metadata: Dict[str, Any]
    priority: int = 0

class StreamHandler:
    """Handler for stream outputs with rate limiting"""
    def __init__(self, callback: Callable, rate_limit: int = 10):
        self.callback = callback
        self.rate_limit = rate_limit  # Max calls per second
        self.last_calls: List[datetime] = []
        self._lock = threading.Lock()

    def __call__(self, output: StreamOutput) -> None:
        """Handle stream output with rate limiting"""
        with self._lock:
            now = datetime.now()
            # Clean old calls
            self.last_calls = [t for t in self.last_calls 
                             if (now - t).total_seconds() < 1]
            
            # Check rate limit
            if len(self.last_calls) >= self.rate_limit:
                logging.warning("Stream handler rate limit exceeded")
                return

            # Add call and execute
            self.last_calls.append(now)
            try:
                self.callback(output)
            except Exception as e:
                logging.error(f"Stream handler error: {str(e)}")

class DualStreamManager:
    """Manages bifurcated output streams while maintaining unified context"""
    
    def __init__(self, session_timeout: int = 3600):
        self._lock = threading.Lock()
        self.contexts: Dict[str, SecurityContext] = {}
        self.crisis_handlers: Dict[str, StreamHandler] = {}
        self.knowledge_handlers: Dict[str, StreamHandler] = {}
        self.output_queues: Dict[str, Dict[StreamType, queue.Queue]] = {}
        self.active_commands: Dict[str, subprocess.Popen] = {}
        self.session_timeout = session_timeout  # seconds
        
        # Start cleanup thread
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_inactive_sessions,
            daemon=True
        )
        self._cleanup_thread.start()

    def initialize_session(self, user_proficiency: str) -> str:
        """Initialize a new dual-stream session"""
        session_id = str(uuid.uuid4())
        
        with self._lock:
            # Create context
            self.contexts[session_id] = SecurityContext(
                session_id=session_id,
                start_time=datetime.now(),
                user_proficiency=user_proficiency,
                current_analysis={},
                command_history=[],
                findings=[],
                learning_opportunities=[],
                last_activity=datetime.now()
            )
            
            # Initialize queues
            self.output_queues[session_id] = {
                StreamType.CRISIS: queue.Queue(maxsize=1000),
                StreamType.KNOWLEDGE: queue.Queue(maxsize=1000)
            }
            
        return session_id

    def process_user_input(self, session_id: str, query: str) -> Dict[str, Any]:
        """Process user input and update both streams"""
        if not self._validate_session(session_id):
            raise ValueError("Invalid or expired session")
            
        try:
            # Update last activity
            self._update_activity(session_id)
            
            # Get context
            context = self.contexts[session_id]
            
            # Analyze query
            analysis = self._analyze_query(query, context)
            
            # Update context
            with self._lock:
                context.current_analysis = analysis
            
            # Generate outputs
            crisis_output = self._generate_crisis_output(analysis, session_id)
            knowledge_output = self._generate_knowledge_output(analysis, session_id)
            
            # Queue outputs
            self._queue_output(session_id, crisis_output)
            self._queue_output(session_id, knowledge_output)
            
            # Notify handlers
            self._notify_handlers(session_id)
            
            return {
                'crisis': crisis_output,
                'knowledge': knowledge_output,
                'context': context
            }
            
        except Exception as e:
            logging.error(f"Error processing input: {str(e)}")
            raise

    def register_crisis_handler(self, session_id: str, handler: Callable,
                              rate_limit: int = 10) -> None:
        """Register handler for crisis stream"""
        with self._lock:
            self.crisis_handlers[session_id] = StreamHandler(handler, rate_limit)

    def register_knowledge_handler(self, session_id: str, handler: Callable,
                                 rate_limit: int = 10) -> None:
        """Register handler for knowledge stream"""
        with self._lock:
            self.knowledge_handlers[session_id] = StreamHandler(handler, rate_limit)

    def close_session(self, session_id: str) -> None:
        """Close a session and cleanup resources"""
        with self._lock:
            # Stop any active commands
            if session_id in self.active_commands:
                process = self.active_commands[session_id]
                try:
                    process.terminate()
                    process.wait(timeout=5.0)
                except Exception:
                    try:
                        process.kill()
                    except Exception:
                        pass
                del self.active_commands[session_id]
            
            # Remove handlers
            self.crisis_handlers.pop(session_id, None)
            self.knowledge_handlers.pop(session_id, None)
            
            # Clear queues
            self.output_queues.pop(session_id, None)
            
            # Remove context
            self.contexts.pop(session_id, None)

    def _validate_session(self, session_id: str) -> bool:
        """Validate session exists and is active"""
        with self._lock:
            if session_id not in self.contexts:
                return False
                
            context = self.contexts[session_id]
            if (datetime.now() - context.last_activity).total_seconds() > self.session_timeout:
                self.close_session(session_id)
                return False
                
            return True

    def _update_activity(self, session_id: str) -> None:
        """Update session last activity time"""
        with self._lock:
            if session_id in self.contexts:
                self.contexts[session_id].last_activity = datetime.now()

    def _queue_output(self, session_id: str, output: StreamOutput) -> None:
        """Queue stream output"""
        try:
            queue = self.output_queues[session_id][output.stream_type]
            if queue.full():
                # Remove oldest item if queue is full
                try:
                    queue.get_nowait()
                except queue.Empty:
                    pass
            queue.put_nowait(output)
        except Exception as e:
            logging.error(f"Error queueing output: {str(e)}")

    def _notify_handlers(self, session_id: str) -> None:
        """Notify registered handlers of new output"""
        try:
            # Process crisis queue
            if session_id in self.crisis_handlers:
                queue = self.output_queues[session_id][StreamType.CRISIS]
                while not queue.empty():
                    try:
                        output = queue.get_nowait()
                        self.crisis_handlers[session_id](output)
                    except Exception as e:
                        logging.error(f"Crisis handler error: {str(e)}")
                    finally:
                        queue.task_done()
            
            # Process knowledge queue
            if session_id in self.knowledge_handlers:
                queue = self.output_queues[session_id][StreamType.KNOWLEDGE]
                while not queue.empty():
                    try:
                        output = queue.get_nowait()
                        self.knowledge_handlers[session_id](output)
                    except Exception as e:
                        logging.error(f"Knowledge handler error: {str(e)}")
                    finally:
                        queue.task_done()
                        
        except Exception as e:
            logging.error(f"Error notifying handlers: {str(e)}")

    def _cleanup_inactive_sessions(self) -> None:
        """Cleanup inactive sessions periodically"""
        while True:
            try:
                now = datetime.now()
                with self._lock:
                    inactive = [
                        sid for sid, ctx in self.contexts.items()
                        if (now - ctx.last_activity).total_seconds() > self.session_timeout
                    ]
                    for session_id in inactive:
                        self.close_session(session_id)
            except Exception as e:
                logging.error(f"Session cleanup error: {str(e)}")
            finally:
                # Sleep for 5 minutes
                threading.Event().wait(300)

    def _analyze_query(self, query: str, context: SecurityContext) -> Dict[str, Any]:
        """Analyze user query"""
        # TODO: Implement query analysis with native bridge
        return {
            'query': query,
            'timestamp': datetime.now(),
            'user_level': context.user_proficiency
        }

    def _generate_crisis_output(self, analysis: Dict[str, Any],
                              session_id: str) -> StreamOutput:
        """Generate crisis-focused output"""
        # TODO: Implement crisis output generation with native bridge
        return StreamOutput(
            stream_type=StreamType.CRISIS,
            content="Processing security query...",
            timestamp=datetime.now(),
            context_id=session_id,
            metadata=analysis,
            priority=1
        )

    def _generate_knowledge_output(self, analysis: Dict[str, Any],
                                 session_id: str) -> StreamOutput:
        """Generate knowledge-focused output"""
        # TODO: Implement knowledge output generation with native bridge
        return StreamOutput(
            stream_type=StreamType.KNOWLEDGE,
            content="Analyzing security implications...",
            timestamp=datetime.now(),
            context_id=session_id,
            metadata=analysis,
            priority=0
        )

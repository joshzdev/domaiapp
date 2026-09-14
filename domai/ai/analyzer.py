"""Core AI Analysis Engine for DōmAI

Provides real-time security analysis with dual-stream output capabilities.
"""

import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from collections import deque
import logging

from .model_config import ModelConfig, ModelProvider, ModelParameters, ModelConfigManager
from .llm_provider import LLMManager

@dataclass
class SecurityContext:
    """Rich context for security analysis"""
    event_history: List[dict]
    user_proficiency: str
    system_state: dict
    threat_context: dict

@dataclass
class StreamOutput:
    """Dual-stream output structure"""
    crisis: str  # Immediate security response
    knowledge: str  # Educational/contextual content
    timestamp: datetime
    context_id: str
    metadata: Dict[str, Any]

class AIAnalyzer:
    """Enhanced AI analysis engine with dual-stream support"""
    def __init__(self):
        self.context_window = deque(maxlen=100)
        self.analysis_cache = {}
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.command_templates = self._load_command_templates()
        self.prompt_templates = self._load_prompt_templates()
        self.llm_manager = LLMManager()
        self.config_manager = ModelConfigManager()
        
    async def process_user_query(self, query: str, user_proficiency: str) -> Tuple[str, StreamOutput]:
        """Process natural language security query"""
        try:
            # Get model configurations
            config = self.config_manager.get_config(ModelProvider.OPENAI)
            
            # Generate dual-stream response
            crisis, knowledge = await self.llm_manager.generate_dual_stream(
                query,
                config,
                stream=False
            )
            
            # Generate command if needed
            command = await self._generate_command(query, crisis)
            
            output = StreamOutput(
                crisis=crisis,
                knowledge=knowledge,
                timestamp=datetime.now(),
                context_id=str(uuid.uuid4()),
                metadata={'command': command}
            )
            
            return command, output
            
        except Exception as e:
            logging.error(f"Query processing failed: {str(e)}")
            return None, self._get_fallback_output()

    async def analyze_security_event(self, event: dict, context: SecurityContext) -> StreamOutput:
        """Analyze security event with dual-stream output"""
        try:
            # Add to context window
            self.context_window.append(event)
            
            # Get cached analysis if available
            cache_key = self._generate_cache_key(event)
            if cache_key in self.analysis_cache:
                return self.analysis_cache[cache_key]
            
            # Get model configurations
            config = self.config_manager.get_config(ModelProvider.OPENAI)
            
            # Generate dual-stream analysis
            crisis, knowledge = await self.llm_manager.generate_dual_stream(
                self._format_event_prompt(event, context),
                config,
                stream=False
            )
            
            output = StreamOutput(
                crisis=crisis,
                knowledge=knowledge,
                timestamp=datetime.now(),
                context_id=str(uuid.uuid4()),
                metadata={'event': event}
            )
            
            # Cache result
            self.analysis_cache[cache_key] = output
            
            return output
            
        except Exception as e:
            logging.error(f"Event analysis failed: {str(e)}")
            return self._get_fallback_output()

    def _load_command_templates(self) -> Dict[str, Dict[str, str]]:
        """Load command templates for different security tools"""
        return {
            'tcpdump': {
                'basic': 'tcpdump -i any -n',
                'detailed': 'tcpdump -i any -n -vv',
                'exploit_scan': 'tcpdump -i any -n "tcp[tcpflags] & (tcp-syn) != 0"',
                'connection_track': 'tcpdump -i any -n "tcp[tcpflags] & (tcp-syn|tcp-fin|tcp-rst) != 0"'
            }
        }

    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load LLM prompt templates"""
        return {
            'query_analysis': """Analyze this security-related query:
                              {query}
                              User proficiency: {proficiency}
                              Determine:
                              1. Primary security concern
                              2. Appropriate security tools
                              3. Required monitoring approach""",
            'event_analysis': """Analyze this security event:
                              {event}
                              Recent context: {context}
                              Generate both:
                              1. Immediate security response
                              2. Educational explanation"""
        }
        
    async def _generate_command(self, query: str, crisis_response: str) -> Optional[str]:
        """Generate appropriate command based on query and crisis response"""
        try:
            config = self.config_manager.get_config(ModelProvider.OPENAI)
            prompt = f"""Based on this security query and response, suggest an appropriate command:
                     Query: {query}
                     Response: {crisis_response}
                     Available commands: {json.dumps(self.command_templates)}"""
                     
            command = await self.llm_manager.generate(prompt, config)
            return command.strip()
            
        except Exception as e:
            logging.error(f"Command generation failed: {str(e)}")
            return None
            
    def _format_event_prompt(self, event: dict, context: SecurityContext) -> str:
        """Format prompt for event analysis"""
        return f"""Analyze this security event in the current context:
                Event: {json.dumps(event)}
                User proficiency: {context.user_proficiency}
                Recent events: {json.dumps(list(self.context_window)[-5:])}
                Active threats: {json.dumps(context.threat_context)}"""

    def _generate_cache_key(self, event: dict) -> str:
        """Generate cache key for event"""
        return f"{event.get('type')}:{event.get('id', str(uuid.uuid4()))}"

    def _get_fallback_output(self) -> StreamOutput:
        """Generate fallback output when analysis fails"""
        return StreamOutput(
            crisis="Security analysis temporarily unavailable",
            knowledge="System is continuing to monitor for security events",
            timestamp=datetime.now(),
            context_id=str(uuid.uuid4()),
            metadata={}
        )

    # Additional methods would be implemented here...

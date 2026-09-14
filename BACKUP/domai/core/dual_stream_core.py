#!/usr/bin/env python3
"""
DōmAI Dual Stream Core
Handles parallel crisis and knowledge streams with integrated LLM analysis
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import subprocess
import logging
import queue
import threading
import uuid

@dataclass
class StreamOutput:
    crisis: str
    knowledge: str
    timestamp: datetime
    metadata: Dict[str, any]

class CommandTemplate:
    def __init__(self, command: str, friendly_name: str, description: str):
        self.command = command
        self.friendly_name = friendly_name
        self.description = description

class SecurityCommand:
    """Security command execution and analysis"""
    
    COMMAND_TEMPLATES = {
        'network_listen': CommandTemplate(
            'lsof -i -n -P | grep LISTEN',
            'Check for hidden listening ports',
            'Identifies programs accepting network connections'
        ),
        'active_connections': CommandTemplate(
            'netstat -tunapl',
            'Show active network connections',
            'Lists all programs communicating over the network'
        ),
        'basic_capture': CommandTemplate(
            'tcpdump -i any -n',
            'Monitor network traffic',
            'Captures and analyzes network packets in real-time'
        ),
        'suspicious_traffic': CommandTemplate(
            'tcpdump -i any -n "tcp[tcpflags] & (tcp-syn|tcp-rst) != 0"',
            'Check for suspicious connection attempts',
            'Monitors for potential port scans or attacks'
        ),
        'dns_queries': CommandTemplate(
            'tcpdump -i any -n port 53',
            'Monitor DNS queries',
            'Shows domain name lookups from your system'
        ),
        'process_connections': CommandTemplate(
            'lsof -i -n -P',
            'Show process network activity',
            'Lists which programs are making network connections'
        )
    }

    def __init__(self):
        self.active_commands: Dict[str, subprocess.Popen] = {}
        self.output_handlers: Dict[str, queue.Queue] = {}
        self.output_threads: Dict[str, threading.Thread] = {}

    def execute(self, command_type: str, params: Optional[Dict] = None) -> Tuple[queue.Queue, str]:
        """Execute security command and return output queue"""
        if command_type not in self.COMMAND_TEMPLATES:
            raise ValueError(f"Unknown command type: {command_type}")

        template = self.COMMAND_TEMPLATES[command_type]
        command = self._build_command(template.command, params)

        # Create output queue
        output_queue = queue.Queue()
        command_id = f"{command_type}_{uuid.uuid4()}"
        self.output_handlers[command_id] = output_queue

        try:
            # Start command
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                bufsize=1
            )
            
            self.active_commands[command_id] = process

            # Start output handler thread
            thread = threading.Thread(
                target=self._handle_output,
                args=(command_id, process),
                daemon=True
            )
            self.output_threads[command_id] = thread
            thread.start()

            return output_queue, command_id

        except Exception as e:
            logging.error(f"Failed to execute command: {str(e)}")
            raise

    def _build_command(self, base_command: str, params: Optional[Dict] = None) -> str:
        """Build command with parameters"""
        if not params:
            return base_command

        # Add parameters based on command type
        # TODO: Implement parameter handling
        return base_command

    def _handle_output(self, command_id: str, process: subprocess.Popen):
        """Handle command output streams"""
        try:
            for line in process.stdout:
                # Put output in queue
                if command_id in self.output_handlers:
                    self.output_handlers[command_id].put({
                        'type': 'output',
                        'content': line.strip(),
                        'timestamp': datetime.now().isoformat()
                    })

        except Exception as e:
            logging.error(f"Error handling command output: {str(e)}")

        finally:
            # Cleanup
            if command_id in self.active_commands:
                del self.active_commands[command_id]
            if command_id in self.output_handlers:
                self.output_handlers[command_id].put(None)  # Signal completion
                del self.output_handlers[command_id]
            if command_id in self.output_threads:
                del self.output_threads[command_id]

class DualStreamAnalyzer:
    """Analyzes security data and generates dual-stream output"""

    def __init__(self):
        self.command_executor = SecurityCommand()
        self.analysis_cache = {}

    def analyze_security_concern(self, query: str, user_level: str) -> StreamOutput:
        """Process security concern and generate dual-stream response"""
        try:
            # Analyze query intent
            commands = self._determine_commands(query)

            # Generate initial response
            response = StreamOutput(
                crisis=self._format_crisis_plan(commands),
                knowledge=self._format_knowledge_context(commands),
                timestamp=datetime.now(),
                metadata={'commands': commands}
            )

            return response

        except Exception as e:
            logging.error(f"Analysis failed: {str(e)}")
            return self._get_fallback_output()

    def process_command_output(self, command_type: str, output: str, user_level: str) -> StreamOutput:
        """Process command output for both streams"""
        try:
            # Get command template
            template = SecurityCommand.COMMAND_TEMPLATES[command_type]

            # Generate dual-stream analysis
            crisis = self._analyze_for_crisis(output, command_type)
            knowledge = self._analyze_for_knowledge(output, command_type, template)

            return StreamOutput(
                crisis=crisis,
                knowledge=knowledge,
                timestamp=datetime.now(),
                metadata={
                    'command_type': command_type,
                    'user_level': user_level
                }
            )

        except Exception as e:
            logging.error(f"Output analysis failed: {str(e)}")
            return self._get_fallback_output()

    def _determine_commands(self, query: str) -> List[str]:
        """Determine appropriate commands based on query"""
        # TODO: Implement LLM-based command selection
        return ['network_listen', 'active_connections']

    def _analyze_for_crisis(self, output: str, command_type: str) -> str:
        """Generate crisis stream analysis"""
        # TODO: Implement LLM crisis analysis
        return f"Analyzing {command_type} output..."

    def _analyze_for_knowledge(self, output: str, command_type: str, template: CommandTemplate) -> str:
        """Generate knowledge stream analysis"""
        # TODO: Implement LLM knowledge analysis
        return f"Understanding {template.friendly_name}..."

    def _format_crisis_plan(self, commands: List[str]) -> str:
        """Format crisis stream plan"""
        plans = [SecurityCommand.COMMAND_TEMPLATES[cmd].friendly_name 
                for cmd in commands]
        return "Planning to:\n" + "\n".join(f"- {plan}" for plan in plans)

    def _format_knowledge_context(self, commands: List[str]) -> str:
        """Format knowledge stream context"""
        explanations = [SecurityCommand.COMMAND_TEMPLATES[cmd].description 
                       for cmd in commands]
        return "What we're doing:\n" + "\n".join(f"- {exp}" for exp in explanations)

    def _get_fallback_output(self) -> StreamOutput:
        """Generate fallback output when analysis fails"""
        return StreamOutput(
            crisis="Continuing security checks...",
            knowledge="System is monitoring for issues...",
            timestamp=datetime.now(),
            metadata={'fallback': True}
        )

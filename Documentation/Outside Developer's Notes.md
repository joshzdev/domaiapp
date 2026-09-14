
Notes from a third-party developer:

I have reviewed the code and note the following. Should my understanding conflict with any of the original files, the original files should take precedence:

Enclosed are the initial modules for the DōmAI application, including both Python backend and SwiftUI frontend components. Below you will find detailed instructions for understanding, building upon, and testing these modules to align with our vision for the dual-stream application.

### Project Overview

**DōmAI** aims to revolutionize MacOS security through natural language AI interaction using a dual-stream approach: this offers users immediate crisis responses coupled in one stream of input and output, with explanations and educational insights in the other stream. Leveraging AI models, our goal is to simplify complex security tasks for end-users and provide a unified interface for all MacOS security tools.

### Enclosed Files

1. **Python Backend (Directory: domai-backend/)**
   - **AI Module (ai/analyzer.py):** Handles interaction with the AI model to generate responses.
   - **Core System (core/app.py):** Manages application logic.
   - **Command Line Interface (cli.py):** Provides a basic CLI for interaction.
   - **requirements.txt:** List of dependencies needed for the backend.

2. **SwiftUI Frontend (Directory: DōmAIApp/)**
   - **ContentView.swift:** Basic user interface in SwiftUI for interacting with the backend.

### Installation and Setup

#### Python Backend

1. **Set Up the Environment:**
   - Create a virtual environment and activate it:

     ```bash
     python3 -m venv domai-venv
     source domai-venv/bin/activate
     ```

2. **Install Dependencies:**
   - Use the provided `requirements.txt` to install dependencies:

     ```bash
     pip install -r requirements.txt
     ```

3. **Run the CLI:**
   - Use the CLI for initial testing:

     ```bash
     python cli.py --query "I think my network is under attack"
     ```

#### SwiftUI Frontend

1. **Open Xcode:**
   - Open the project located in `DōmAIApp/` and run the initial UI to see a basic interface.

2. **Enhance User Interaction:**
   - Develop interactive components to handle user queries and display outputs from the backend.

### Developer Tasks

1. **AI and Backend Integration:**
   - Finalize AI model selection and fine-tune the model using frameworks like Hugging Face Transformers.
   - Enhance the dual-stream processing logic to tailor responses more accurately to both user queries and educational needs.

2. **Frontend-Backend Communication:**
   - Establish a robust communication link between the SwiftUI frontend and Python backend, potentially using PythonKit or an IPC method.

3. **Iterative Testing:**
   - Work closely with the user experience team to conduct initial testing of both crisis and educational streams.
   - Gather feedback and refine output quality, ensuring consistent performance.

4. **Documentation:**
   - As development progresses, maintain comprehensive documentation to facilitate continual development and potential intellectual property assessments.

With these initial structures in place, your task is to develop the dual-stream capabilities fully, ensuring a seamless user experience and integrating sophisticated AI interactions. Your expertise is critical in transforming this foundational code into a cutting-edge security solution.

Best Regards,
[Your Name/Team]


PS

Let me provide a comprehensive analysis of the codebase based on the project documentation and structure, focusing on the core purpose and priorities.

## Core Purpose & Vision

DōmAI is a macOS security & maintenance application that focuses on natural language interaction and adaptive learning. The key aspects are:

1. **Natural Language Interface**

- Users communicate security concerns naturally without technical jargon
- AI adapts to user's expertise level
- Progressive complexity revelation

2. **Dual-Stream Architecture**

- Crisis Stream: For immediate security responses
- Knowledge Stream: For learning and understanding
- Both streams operate in parallel with context-aware explanations

3. **Dynamic Complexity Adaptation**

- Interface transforms from beginner to advanced levels
- Makes complex security tools accessible
- No forced progression paths

## Core Architecture

The codebase is organized into several key components:

1. **Core (`domai/core/`)**

- `fortress_nexus.py`: Central security orchestration
- `dual_stream_core.py`: Manages the dual-stream interface
- `orchestrator.py`: Coordinates system components
- `permission_manager.py`: Handles security permissions

2. **AI Integration (`domai/ai/`)**

- `analyzer.py`: Security analysis engine
- Natural language processing
- Context management
- Adaptive learning

3. **Modules System**

- Files (`modules/files/`): File system security
- Identity (`modules/identity/`): User management & permissions
- Network (`modules/network/`): Network security & firewall
- System (`modules/system/`): System monitoring & management

4. **Native Bridge (API)**

- SwiftUI interface integration
- IPC via Unix Domain Sockets
- Security-focused message passing
- Permission boundaries

## Key Features & Implementation

1. **Security Management**

```python
# From modules/network/firewall.py
class FirewallManager:
    """Manage macOS packet filter firewall"""
    def get_status(self) -> Dict[str, Union[str, FirewallStatus]]:
        """Get firewall status"""
```

2. **Identity & Permissions**

```python
# From modules/identity/__init__.py
from .users import UserManager
from .permissions import PermissionManager
from .sessions import SessionMonitor
```

3. **System Monitoring**

```python
# From modules/system/__init__.py
from .processes import ProcessMonitor
from .kernel import KernelMonitor
from .hardware import HardwareMonitor
```

## Development Setup

Requirements:

- macOS 14+ (Apple Silicon optimized)
- Python 3.8+
- Xcode 15+

Key dependencies (from `requirements.txt`):
```
cryptography>=3.4.7
pyobjc-core>=9.2
pydantic>=1.8.2
scapy>=2.5.0
```

## Testing & Quality

The project uses:

- pytest for testing
- mypy for type checking
- flake8 for linting
- black for code formatting

From `pytest.ini`:
```ini
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    security: marks tests as security-related
```

## Security Considerations

1. **Permission Model**

- Fine-grained permission control
- Resource access management
- Security policy enforcement
- Audit logging

2. **Data Security**

- Encrypted storage
- Secure key management
- Data isolation
- Access controls

3. **Network Security**

- Packet analysis
- Traffic monitoring
- Port scanning detection
- Connection tracking

## Documentation Structure

The documentation is comprehensive and well-organized:

- `VISION.md`: Project goals and philosophy
- `ARCHITECTURE.md`: Technical design and structure
- `SECURITY_GUIDE.md`: Security implementation details
- `USER_GUIDE.md`: End-user documentation
- `DEVELOPMENT.md`: Developer setup and guidelines

## License & Support

- MIT License
- Technical Contact: ai@domai.dev
- Security Team: security@domai.dev

This codebase represents a sophisticated macOS security application with a strong focus on user interaction through natural language and adaptive learning. The architecture emphasizes security, modularity, and user education through its dual-stream approach.






PS Here is the terminal out put when running tree and file contentn commands:


joshua@JZMBP domai-app % ls -R
# or
tree
Documentation		pytest.ini		setup.py
domai			requirements.txt	tests
modules			setup.cfg

./Documentation:
API.md				LICENSE
ARCHITECTURE.md			Outside Developer's Notes.md
CHANGELOG.md			README BACKUP.md
COMPLETE_ACTION_LOG.md		README.md
DEVELOPMENT.md			SECURITY_GUIDE.md
HANDOFF.md			USER_GUIDE.md
Josh's_Homework.md		VISION.md

./domai:
__init__.py	api		core		ui
ai		cli.py		monitoring	utils

./domai/ai:
__init__.py	analyzer.py

./domai/api:
__init__.py

./domai/core:
__init__.py		dual_stream_core.py	stream_manager.py
analysis_pipeline.py	fortress_nexus.py	streams.py
app.py			orchestrator.py
command_executor.py	permission_manager.py

./domai/monitoring:
__init__.py	manager.py	network.py	process.py	system.py

./domai/ui:
__init__.py

./domai/utils:
__init__.py

./modules:
files		identity	network		system

./modules/files:
__init__.py	changes.py	integrity.py	permissions.py	storage.py

./modules/identity:
__init__.py	access.py	permissions.py	sessions.py	users.py

./modules/network:
__init__.py	dns.py		packets.py	services.py
connections.py	firewall.py	ports.py	stats.py

./modules/system:
__init__.py	hardware.py	kernel.py	processes.py	services.py

./tests:
files		identity	network		system

./tests/files:

./tests/identity:

./tests/network:

./tests/system:
zsh: command not found: #
zsh: command not found: tree
joshua@JZMBP domai-app % find . -name "*.py" -type f -exec cat {} \;
#!/usr/bin/env python3
"""
DōmAI - Intelligent Security Alliance
Setup script for package installation
"""

import os
from setuptools import setup, find_packages

setup(
    name="domai",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cryptography>=3.4.7",
        "psutil>=5.8.0",
        "pyobjc-core>=9.2",
        "pyobjc-framework-Cocoa>=9.2",
        "pyobjc-framework-Security>=9.2",
        "pyobjc-framework-SystemConfiguration>=9.2",
        "bcrypt>=3.2.0",
        "pydantic>=1.8.2",
        "watchdog>=2.1.0",
        "scapy>=2.4.5",
        "pyOpenSSL>=20.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-asyncio>=0.15.1",
            "pytest-cov>=2.12.1",
            "black>=21.7b0",
            "flake8>=3.9.2",
            "mypy>=0.910",
            "isort>=5.9.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "domai=domai.cli:main",
        ],
    },
    author="DōmAI Security Alliance",
    author_email="humans@domai.dev",
    description="Native macOS security & maintenance with natural language interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/domai-security/domai",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
) """
Terminal UI components for DōmAI
UI implementation pending user requirements
"""
#!/usr/bin/env python3
"""
Dual Stream Core Implementation for DōmAI

Implements parallel crisis and knowledge streams with unified context.
Each security event/analysis maintains integrity across both streams
while presenting different aspects of the same information.

Author: Claude
Created: December 2024
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from collections import deque
import logging
import json
import uuid

class StreamType(Enum):
    CRISIS = "crisis"  # Immediate security response
    KNOWLEDGE = "knowledge"  # Educational/contextual content

@dataclass
class SecurityContext:
    """Shared context between streams"""
    session_id: str
    timestamp: datetime
    user_level: str
    command_history: List[str]
    active_threats: List[Dict[str, Any]]
    learning_opportunities: List[str]

@dataclass
class StreamOutput:
    """Output structure for either stream"""
    content: str
    stream_type: StreamType
    context_id: str
    timestamp: datetime
    metadata: Dict[str, Any]
    priority: int = 0  # Higher numbers = more urgent

class DualStreamManager:
    """Manages parallel crisis and knowledge streams"""
    
    def __init__(self):
        self.current_context: Optional[SecurityContext] = None
        self.crisis_buffer = deque(maxlen=1000)
        self.knowledge_buffer = deque(maxlen=1000)
        self.shared_state: Dict[str, Any] = {}
        self.learning_history: List[Dict[str, Any]] = []

    def process_security_event(self, event: Dict[str, Any], user_level: str) -> tuple[StreamOutput, StreamOutput]:
        """Process security event and generate dual-stream output"""
        try:
            # Update context
            self._update_context(event, user_level)

            # Generate stream outputs
            crisis_output = self._generate_crisis_output(event)
            knowledge_output = self._generate_knowledge_output(event)

            # Store in buffers
            self.crisis_buffer.append(crisis_output)
            self.knowledge_buffer.append(knowledge_output)

            # Track learning opportunities
            self._track_learning(event, knowledge_output)

            return crisis_output, knowledge_output

        except Exception as e:
            logging.error(f"Error processing security event: {str(e)}")
            return self._get_fallback_outputs()

    def start_command_execution(self, command: str, friendly_name: str) -> tuple[StreamOutput, StreamOutput]:
        """Begin command execution with dual-stream output"""
        try:
            # Update command history
            if self.current_context:
                self.current_context.command_history.append(command)

            # Generate initial outputs
            crisis = StreamOutput(
                content=f"Executing: {friendly_name}...",
                stream_type=StreamType.CRISIS,
                context_id=self.current_context.session_id if self.current_context else "unknown",
                timestamp=datetime.now(),
                metadata={"command": command, "stage": "start"},
                priority=1
            )

            knowledge = StreamOutput(
                content=self._get_command_explanation(command),
                stream_type=StreamType.KNOWLEDGE,
                context_id=self.current_context.session_id if self.current_context else "unknown",
                timestamp=datetime.now(),
                metadata={"command": command, "stage": "explanation"},
                priority=0
            )

            return crisis, knowledge

        except Exception as e:
            logging.error(f"Error starting command execution: {str(e)}")
            return self._get_fallback_outputs()

    def _update_context(self, event: Dict[str, Any], user_level: str):
        """Update security context"""
        if not self.current_context:
            self.current_context = SecurityContext(
                session_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                user_level=user_level,
                command_history=[],
                active_threats=[],
                learning_opportunities=[]
            )
        
        # Update threat tracking
        if event.get('severity', '').upper() in ['HIGH', 'CRITICAL']:
            self.current_context.active_threats.append({
                'type': event.get('type'),
                'details': event.get('details'),
                'timestamp': datetime.now()
            })

    def _generate_crisis_output(self, event: Dict[str, Any]) -> StreamOutput:
        """Generate crisis stream output"""
        # TODO: Replace with actual LLM generation
        severity = event.get('severity', 'UNKNOWN').upper()
        if severity in ['HIGH', 'CRITICAL']:
            content = f"ALERT: {event.get('type')} detected! {event.get('details')}"
            priority = 2
        else:
            content = f"Monitoring: {event.get('type')} - {event.get('details')}"
            priority = 1

        return StreamOutput(
            content=content,
            stream_type=StreamType.CRISIS,
            context_id=self.current_context.session_id if self.current_context else "unknown",
            timestamp=datetime.now(),
            metadata={"event_type": event.get('type')},
            priority=priority
        )

    def _generate_knowledge_output(self, event: Dict[str, Any]) -> StreamOutput:
        """Generate knowledge stream output"""
        # TODO: Replace with actual LLM generation
        content = self._get_educational_content(event.get('type'))
        
        return StreamOutput(
            content=content,
            stream_type=StreamType.KNOWLEDGE,
            context_id=self.current_context.session_id if self.current_context else "unknown",
            timestamp=datetime.now(),
            metadata={"event_type": event.get('type')},
            priority=0
        )

    def _track_learning(self, event: Dict[str, Any], knowledge_output: StreamOutput):
        """Track learning opportunities and user progression"""
        if not self.current_context:
            return

        # Record learning opportunity
        learning_event = {
            'timestamp': datetime.now(),
            'event_type': event.get('type'),
            'knowledge_shared': knowledge_output.content,
            'user_level': self.current_context.user_level
        }
        self.learning_history.append(learning_event)

        # Check for learning achievements
        self._check_learning_achievements()

    def _check_learning_achievements(self):
        """Check for learning achievements and level progression"""
        if not self.current_context:
            return

        # Example achievement checks
        knowledge_count = len(self.learning_history)
        if knowledge_count >= 10 and self.current_context.user_level == 'novice':
            self.current_context.learning_opportunities.append(
                "Ready for more advanced security concepts!"
            )

    def _get_command_explanation(self, command: str) -> str:
        """Get educational explanation of command"""
        # TODO: Replace with actual LLM-generated content
        explanations = {
            'tcpdump': "tcpdump captures and analyzes network packets in real-time...",
            'netstat': "netstat shows active network connections and listening ports...",
            'lsof': "lsof lists open files and the processes using them..."
        }
        
        for cmd, explanation in explanations.items():
            if cmd in command.lower():
                return explanation
        return "This command helps monitor system security..."

    def _get_educational_content(self, event_type: str) -> str:
        """Get educational content based on event type"""
        # TODO: Replace with actual LLM-generated content
        content_map = {
            'network_connection': "Network connections allow your computer to communicate...",
            'file_access': "File access monitoring helps detect unauthorized changes...",
            'process_launch': "Processes are programs running on your system..."
        }
        return content_map.get(event_type, "Understanding this helps improve system security...")

    def _get_fallback_outputs(self) -> tuple[StreamOutput, StreamOutput]:
        """Generate fallback outputs for error cases"""
        timestamp = datetime.now()
        context_id = self.current_context.session_id if self.current_context else "unknown"

        crisis = StreamOutput(
            content="Continuing security monitoring...",
            stream_type=StreamType.CRISIS,
            context_id=context_id,
            timestamp=timestamp,
            metadata={"error": True},
            priority=0
        )

        knowledge = StreamOutput(
            content="Security monitoring helps protect your system...",
            stream_type=StreamType.KNOWLEDGE,
            context_id=context_id,
            timestamp=timestamp,
            metadata={"error": True},
            priority=0
        )

        return crisis, knowledge
"""Command execution module with security controls."""

import logging
import subprocess
import threading
import shlex
import resource
import signal
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import re

from ..security.permission_manager import PermissionManager
from ..core.types.security import SecurityContext, UserLevel

@dataclass
class ResourceLimits:
    """Resource limits for command execution"""
    max_cpu_time: int = 30  # seconds
    max_memory: int = 512 * 1024 * 1024  # 512MB in bytes
    max_processes: int = 10
    max_file_size: int = 50 * 1024 * 1024  # 50MB in bytes

@dataclass
class CommandResult:
    """Result of a command execution."""
    output: str
    error: Optional[str]
    exit_code: int
    timestamp: datetime
    resource_usage: Dict[str, float]

class CommandExecutor:
    """Secure command execution with permission checks."""

    # Commands that are never allowed
    BLACKLISTED_COMMANDS = {
        'rm', 'srm', 'shred',  # File deletion
        'mkfs', 'fdisk',       # Disk operations
        'mount', 'umount',     # Mount operations
        'dd',                  # Direct disk access
        'chmod', 'chown',      # Permission changes
        'sudo', 'su',          # Privilege escalation
        'passwd', 'chsh'       # User management
    }

    # Regex patterns for dangerous constructs
    DANGEROUS_PATTERNS = [
        r'[|;&`$]',           # Shell operators
        r'>\s*[^"]',          # Redirections
        r'<\s*[^"]',          # Input redirections
        r'\$\(',              # Command substitution
        r'\\[^nt]'            # Escapes except \n and \t
    ]

    def __init__(self, permission_manager: PermissionManager):
        self.permission_manager = permission_manager
        self._lock = threading.Lock()
        self.active_commands: Dict[str, subprocess.Popen] = {}
        self.command_limits: Dict[str, ResourceLimits] = {}

    def execute(self, command: str, context: SecurityContext) -> CommandResult:
        """Execute a command with security checks."""
        try:
            # Validate command
            if not self._validate_command(command, context):
                return CommandResult(
                    output="",
                    error="Command validation failed: Security violation",
                    exit_code=1,
                    timestamp=datetime.now(),
                    resource_usage={}
                )

            # Get resource limits
            limits = self._get_resource_limits(context.user_level)

            # Set up command execution
            args = shlex.split(command)
            
            # Apply resource limits
            def preexec():
                resource.setrlimit(resource.RLIMIT_CPU, (limits.max_cpu_time, limits.max_cpu_time))
                resource.setrlimit(resource.RLIMIT_AS, (limits.max_memory, limits.max_memory))
                resource.setrlimit(resource.RLIMIT_NPROC, (limits.max_processes, limits.max_processes))
                resource.setrlimit(resource.RLIMIT_FSIZE, (limits.max_file_size, limits.max_file_size))

            # Execute command
            with self._lock:
                process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=preexec,
                    text=True,
                    shell=False  # Never use shell=True
                )
                self.active_commands[context.session_id] = process

            try:
                # Wait with timeout
                stdout, stderr = process.communicate(timeout=limits.max_cpu_time)
            except subprocess.TimeoutExpired:
                self._terminate_process(process)
                return CommandResult(
                    output="",
                    error="Command timed out",
                    exit_code=124,
                    timestamp=datetime.now(),
                    resource_usage=self._get_resource_usage(process)
                )
            finally:
                # Cleanup
                with self._lock:
                    if context.session_id in self.active_commands:
                        del self.active_commands[context.session_id]

            return CommandResult(
                output=stdout,
                error=stderr if stderr else None,
                exit_code=process.returncode,
                timestamp=datetime.now(),
                resource_usage=self._get_resource_usage(process)
            )

        except Exception as e:
            logging.error(f"Command execution failed: {str(e)}")
            return CommandResult(
                output="",
                error=str(e),
                exit_code=1,
                timestamp=datetime.now(),
                resource_usage={}
            )

    def stop(self, session_id: str) -> bool:
        """Stop a running command."""
        with self._lock:
            if session_id in self.active_commands:
                process = self.active_commands[session_id]
                self._terminate_process(process)
                del self.active_commands[session_id]
                return True
        return False

    def _validate_command(self, command: str, context: SecurityContext) -> bool:
        """Validate command for security."""
        try:
            # Split command into parts
            parts = shlex.split(command)
            if not parts:
                return False

            # Check base command
            base_cmd = parts[0].lower()
            if base_cmd in self.BLACKLISTED_COMMANDS:
                logging.warning(f"Blocked blacklisted command: {base_cmd}")
                return False

            # Check for dangerous patterns
            for pattern in self.DANGEROUS_PATTERNS:
                if re.search(pattern, command):
                    logging.warning(f"Blocked command with dangerous pattern: {pattern}")
                    return False

            # Validate through permission manager
            if not self.permission_manager.check_permission(f"execute_{base_cmd}"):
                logging.warning(f"Permission denied for command: {base_cmd}")
                return False

            return True

        except Exception as e:
            logging.error(f"Command validation failed: {str(e)}")
            return False

    def _get_resource_limits(self, user_level: UserLevel) -> ResourceLimits:
        """Get resource limits based on user level."""
        if user_level == UserLevel.ADMIN:
            return ResourceLimits(
                max_cpu_time=300,    # 5 minutes
                max_memory=2 * 1024 * 1024 * 1024,  # 2GB
                max_processes=50,
                max_file_size=500 * 1024 * 1024  # 500MB
            )
        elif user_level == UserLevel.ADVANCED:
            return ResourceLimits(
                max_cpu_time=120,    # 2 minutes
                max_memory=1024 * 1024 * 1024,  # 1GB
                max_processes=20,
                max_file_size=100 * 1024 * 1024  # 100MB
            )
        else:
            return ResourceLimits()  # Default limits

    def _terminate_process(self, process: subprocess.Popen) -> None:
        """Safely terminate a process."""
        try:
            process.terminate()
            try:
                process.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        except Exception as e:
            logging.error(f"Process termination failed: {str(e)}")

    def _get_resource_usage(self, process: subprocess.Popen) -> Dict[str, float]:
        """Get resource usage statistics for a process."""
        try:
            with process.stdout, process.stderr:
                usage = resource.getrusage(resource.RUSAGE_CHILDREN)
                return {
                    'user_time': usage.ru_utime,
                    'system_time': usage.ru_stime,
                    'max_rss': usage.ru_maxrss,
                    'shared_memory': usage.ru_ixrss,
                    'unshared_memory': usage.ru_idrss,
                    'page_faults': usage.ru_majflt,
                    'block_input': usage.ru_inblock,
                    'block_output': usage.ru_oublock
                }
        except Exception as e:
            logging.error(f"Failed to get resource usage: {str(e)}")
            return {}
from .fortress_nexus import FortressNexus
from .stream_manager import DualStreamManager
from .command_executor import CommandExecutor
from .types.security import SecurityEvent, SecurityLevel, UserLevel # type: ignore#!/usr/bin/env python3
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
            }#!/usr/bin/env python3
"""
DōmAI Permission Management System
Handles elevated privileges securely with user consent and audit logging
"""

import os
import pwd
import grp
import logging
import threading
from typing import Dict, List, Optional, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import time
from pathlib import Path

class PrivilegeLevel(Enum):
    NORMAL = "normal"         # No special privileges
    ELEVATED = "elevated"     # Some system access (e.g., reading system files)
    ADMIN = "admin"          # Full system access (requires sudo/root)

@dataclass
class Permission:
    name: str
    level: PrivilegeLevel
    description: str
    reason: str
    commands: List[str]
    alternatives: List[str]
    expiry: Optional[datetime] = None
    rate_limit: int = 10  # Max requests per minute

class PermissionManager:
    """Manages system permissions and privileged operations"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.granted_permissions: Dict[str, Permission] = {}
        self.permission_requests: Dict[str, List[datetime]] = {}
        self._setup_audit_logging()
        
        # Define known permissions
        self.permissions: Dict[str, Permission] = {
            "packet_capture": Permission(
                name="packet_capture",
                level=PrivilegeLevel.ADMIN,
                description="Capture network packets",
                reason="Required for network monitoring and security analysis",
                commands=["tcpdump"],
                alternatives=["Wireshark (GUI)", "tshark (CLI)"]
            ),
            "process_monitor": Permission(
                name="process_monitor",
                level=PrivilegeLevel.ELEVATED,
                description="Monitor system processes",
                reason="Required for security monitoring",
                commands=["ps", "top", "lsof"],
                alternatives=["Activity Monitor (GUI)"]
            ),
            "file_monitor": Permission(
                name="file_monitor",
                level=PrivilegeLevel.ELEVATED,
                description="Monitor filesystem changes",
                reason="Required for security monitoring",
                commands=["fswatch", "fs_usage"],
                alternatives=["Folder watching (limited)"]
            )
        }
        
        # Start cleanup thread
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_expired_permissions,
            daemon=True
        )
        self._cleanup_thread.start()
        
    def _setup_audit_logging(self) -> None:
        """Setup secure audit logging"""
        log_dir = Path("logs/security")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Secure log directory
        os.chmod(log_dir, 0o700)
        
        # Setup audit log file
        self.audit_log_file = log_dir / "permissions.log"
        self.audit_log_file.touch(mode=0o600, exist_ok=True)
        
        # Configure logger
        audit_handler = logging.FileHandler(self.audit_log_file)
        audit_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        
        self.audit_logger = logging.getLogger("domai.security.permissions")
        self.audit_logger.addHandler(audit_handler)
        self.audit_logger.setLevel(logging.INFO)
        
    def check_permission(self, permission_name: str) -> bool:
        """Check if permission is currently granted"""
        if not self._validate_permission_name(permission_name):
            return False
            
        with self._lock:
            if permission_name not in self.granted_permissions:
                return False
                
            perm = self.granted_permissions[permission_name]
            if perm.expiry and datetime.now() > perm.expiry:
                self.release_permission(permission_name)
                return False
                
            return True
            
    def request_permission(self, permission_name: str) -> bool:
        """Request permission with rate limiting and validation"""
        if not self._validate_permission_name(permission_name):
            return False
            
        with self._lock:
            # Check rate limiting
            if not self._check_rate_limit(permission_name):
                self.audit_logger.warning(
                    f"Rate limit exceeded for permission: {permission_name}"
                )
                return False
                
            # Get permission definition
            perm = self.permissions[permission_name]
            
            try:
                # Log permission request
                self._log_request(permission_name, perm.level)
                
                # Check current privileges
                current_privileges = self._get_current_privileges()
                
                # Handle elevation if needed
                if perm.level == PrivilegeLevel.ADMIN and current_privileges != PrivilegeLevel.ADMIN:
                    if not self._request_elevation(perm):
                        return False
                        
                # Grant permission with expiry
                self.granted_permissions[permission_name] = Permission(
                    **perm.__dict__,
                    expiry=datetime.now() + timedelta(minutes=30)
                )
                
                self._log_grant(permission_name)
                return True
                
            except Exception as e:
                self.audit_logger.error(
                    f"Permission request failed: {str(e)}"
                )
                return False
                
    def release_permission(self, permission_name: str) -> None:
        """Release a previously granted permission"""
        if not self._validate_permission_name(permission_name):
            return
            
        with self._lock:
            if permission_name in self.granted_permissions:
                del self.granted_permissions[permission_name]
                self._log_release(permission_name)
                
    def _validate_permission_name(self, name: str) -> bool:
        """Validate permission name exists"""
        return name in self.permissions
        
    def _check_rate_limit(self, permission_name: str) -> bool:
        """Check rate limiting for permission requests"""
        now = datetime.now()
        
        # Initialize request history
        if permission_name not in self.permission_requests:
            self.permission_requests[permission_name] = []
            
        # Clean old requests
        self.permission_requests[permission_name] = [
            t for t in self.permission_requests[permission_name]
            if (now - t).total_seconds() < 60
        ]
        
        # Check limit
        perm = self.permissions[permission_name]
        if len(self.permission_requests[permission_name]) >= perm.rate_limit:
            return False
            
        # Add new request
        self.permission_requests[permission_name].append(now)
        return True
        
    def _cleanup_expired_permissions(self) -> None:
        """Cleanup expired permissions periodically"""
        while True:
            try:
                with self._lock:
                    now = datetime.now()
                    expired = [
                        name for name, perm in self.granted_permissions.items()
                        if perm.expiry and now > perm.expiry
                    ]
                    for name in expired:
                        self.release_permission(name)
                        
            except Exception as e:
                self.audit_logger.error(
                    f"Permission cleanup failed: {str(e)}"
                )
                
            time.sleep(60)  # Check every minute
            
    def _log_request(self, permission_name: str, level: PrivilegeLevel) -> None:
        """Log permission request to audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "request",
            "permission": permission_name,
            "level": level.value,
            "process_id": os.getpid(),
            "user": pwd.getpwuid(os.getuid())[0]
        }
        self.audit_logger.info(f"Permission request: {json.dumps(entry)}")
        
    def _log_grant(self, permission_name: str) -> None:
        """Log permission grant to audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "grant",
            "permission": permission_name,
            "process_id": os.getpid(),
            "user": pwd.getpwuid(os.getuid())[0]
        }
        self.audit_logger.info(f"Permission granted: {json.dumps(entry)}")
        
    def _log_release(self, permission_name: str) -> None:
        """Log permission release to audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "release",
            "permission": permission_name,
            "process_id": os.getpid(),
            "user": pwd.getpwuid(os.getuid())[0]
        }
        self.audit_logger.info(f"Permission released: {json.dumps(entry)}")
        
    def get_command_wrapper(self, command: str) -> Optional[str]:
        """Get appropriate wrapper for privileged command"""
        # Find permission that includes this command
        for perm in self.permissions.values():
            if command in perm.commands:
                if self.check_permission(perm.name):
                    if perm.level == PrivilegeLevel.ADMIN:
                        return "sudo"  # Use sudo for admin commands
                break
                
        return None
        
    def _get_current_privileges(self) -> PrivilegeLevel:
        """Determine current process privileges"""
        if os.geteuid() == 0:
            return PrivilegeLevel.ADMIN
            
        # Check group membership
        groups = [g.gr_name for g in grp.getgrall() if pwd.getpwuid(os.getuid())[0] in g.gr_mem]
        if "admin" in groups:
            return PrivilegeLevel.ELEVATED
            
        return PrivilegeLevel.NORMAL
        
    def _request_elevation(self, permission: Permission) -> bool:
        """Request privilege elevation from user"""
        # This would integrate with system's privilege elevation
        # For now, we'll assume it's handled externally
        return True
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
            return False #!/usr/bin/env python3
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
#!/usr/bin/env python3
"""
DōmAI Security Analysis Pipeline
Handles both real-time and historical security data analysis with terminal-like flexibility
"""

import logging
import threading
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import queue
import uuid

from ..security.data_store import (
    SecureDataStore, DataType, TimeRange, DataQuery,
    QueryFilter
)
from ..ai.analyzer import AIAnalyzer
from .types.security import SecurityEvent, SecurityLevel
from .stream_manager import StreamType, StreamOutput
from ..api.bridge import BridgeManager

class AnalysisScope(Enum):
    REAL_TIME = "real_time"
    HISTORICAL = "historical"
    SPECIFIED_RANGE = "specified_range"

@dataclass
class AnalysisContext:
    """Context for security analysis"""
    scope: AnalysisScope
    time_range: Optional[TimeRange]
    user_expertise: str
    system_state: Dict[str, Any]
    recent_events: List[Dict[str, Any]]
    related_findings: List[Dict[str, Any]]
    session_id: str

@dataclass
class AnalysisResult:
    """Result of security analysis"""
    findings: List[Dict[str, Any]]
    patterns: List[Dict[str, Any]]
    threats: List[Dict[str, Any]]
    recommendations: List[str]
    learning_points: List[str]
    timestamp: datetime
    session_id: str

class SecurityAnalysisPipeline:
    """Comprehensive security analysis pipeline with terminal-like flexibility"""
    
    def __init__(self, bridge_manager: BridgeManager):
        self._lock = threading.Lock()
        self.data_store = SecureDataStore()
        self.ai_analyzer = AIAnalyzer()
        self.bridge = bridge_manager
        self.logger = logging.getLogger(__name__)
        
        # Analysis queues
        self.analysis_queues: Dict[str, queue.Queue] = {}
        self.analysis_threads: Dict[str, threading.Thread] = {}
        self.active_analyses: Dict[str, bool] = {}
        
        # Register bridge handlers
        self._register_bridge_handlers()
        
    def analyze_security_data(
        self,
        source: str,
        scope: AnalysisScope,
        user_expertise: str,
        session_id: str,
        time_spec: Optional[str] = None,
        filters: Optional[List[Dict[str, Any]]] = None,
        pattern: Optional[str] = None,
        context_lines: int = 0,
        sort_by: Optional[str] = None,
        sort_desc: bool = False,
        limit: Optional[int] = None,
        aggregation: Optional[str] = None,
        group_by: Optional[str] = None
    ) -> StreamOutput:
        """Analyze security data with terminal-like flexibility"""
        try:
            # Validate inputs
            if not self._validate_inputs(source, scope, user_expertise):
                raise ValueError("Invalid analysis parameters")
            
            # Parse time specification
            time_range = self._parse_time_spec(time_spec, scope)
            
            # Build analysis context
            analysis_context = self._build_context(
                source,
                scope,
                user_expertise,
                time_range,
                session_id
            )
            
            # Convert filters to QueryFilters
            query_filters = self._build_query_filters(filters)
            
            # Build data query
            query = self._build_query(
                source,
                time_range,
                query_filters,
                sort_by,
                sort_desc,
                limit,
                aggregation,
                group_by
            )
            
            # Get data with pattern matching if specified
            data = self._get_data(query, pattern, context_lines)
            
            # Queue analysis
            analysis_id = self._queue_analysis(
                data,
                source,
                analysis_context
            )
            
            # Return initial response
            return StreamOutput(
                crisis=self._get_initial_crisis_response(analysis_id),
                knowledge=self._get_initial_knowledge_response(analysis_id),
                timestamp=datetime.now(),
                metadata={
                    'analysis_id': analysis_id,
                    'scope': scope.value,
                    'source': source,
                    'time_range': time_range._asdict() if time_range else None,
                    'pattern': pattern,
                    'filters': filters,
                    'status': 'queued'
                }
            )
            
        except Exception as e:
            self.logger.error(f"Analysis pipeline error: {str(e)}")
            return self._get_fallback_output(session_id)
            
    def _validate_inputs(self, source: str, scope: AnalysisScope,
                        user_expertise: str) -> bool:
        """Validate analysis input parameters"""
        try:
            # Validate source
            if not source or not isinstance(source, str):
                return False
                
            # Validate scope
            if not isinstance(scope, AnalysisScope):
                return False
                
            # Validate user expertise
            if not user_expertise or not isinstance(user_expertise, str):
                return False
                
            return True
            
        except Exception:
            return False
            
    def _parse_time_spec(self, time_spec: Optional[str],
                        scope: AnalysisScope) -> Optional[TimeRange]:
        """Parse time specification"""
        try:
            if time_spec:
                return TimeRange.from_string(time_spec)
            elif scope == AnalysisScope.REAL_TIME:
                return TimeRange(
                    datetime.now() - timedelta(minutes=5),
                    datetime.now()
                )
            else:
                return TimeRange(
                    datetime.now() - timedelta(days=1),
                    datetime.now()
                )
        except Exception as e:
            self.logger.error(f"Time spec parsing error: {str(e)}")
            raise
            
    def _build_query_filters(self,
                           filters: Optional[List[Dict[str, Any]]]) -> Optional[List[QueryFilter]]:
        """Convert filters to QueryFilters"""
        if not filters:
            return None
            
        try:
            return [
                QueryFilter(
                    field=f['field'],
                    operator=f['operator'],
                    value=f['value']
                )
                for f in filters
            ]
        except Exception as e:
            self.logger.error(f"Filter conversion error: {str(e)}")
            raise
            
    def _build_query(self, source: str, time_range: Optional[TimeRange],
                    filters: Optional[List[QueryFilter]], sort_by: Optional[str],
                    sort_desc: bool, limit: Optional[int],
                    aggregation: Optional[str],
                    group_by: Optional[str]) -> DataQuery:
        """Build data query"""
        try:
            return DataQuery(
                data_type=self.data_store._map_source_to_data_type(source),
                time_range=time_range,
                filters=filters,
                sort_by=sort_by,
                sort_desc=sort_desc,
                limit=limit,
                aggregation=aggregation,
                group_by=group_by
            )
        except Exception as e:
            self.logger.error(f"Query building error: {str(e)}")
            raise
            
    def _get_data(self, query: DataQuery, pattern: Optional[str],
                 context_lines: int) -> List[Dict[str, Any]]:
        """Get data from data store"""
        try:
            if pattern:
                return self.data_store.grep_data(
                    query.data_type,
                    pattern,
                    query.time_range,
                    context_lines=context_lines
                )
            else:
                return self.data_store.query_data(query)
        except Exception as e:
            self.logger.error(f"Data retrieval error: {str(e)}")
            raise
            
    def _queue_analysis(self, data: List[Dict[str, Any]], source: str,
                       context: AnalysisContext) -> str:
        """Queue analysis for processing"""
        analysis_id = str(uuid.uuid4())
        
        with self._lock:
            # Create analysis queue
            self.analysis_queues[analysis_id] = queue.Queue()
            self.active_analyses[analysis_id] = True
            
            # Start analysis thread
            thread = threading.Thread(
                target=self._analysis_worker,
                args=(analysis_id, data, source, context),
                daemon=True
            )
            self.analysis_threads[analysis_id] = thread
            thread.start()
            
        return analysis_id
            
    def _analysis_worker(self, analysis_id: str, data: List[Dict[str, Any]],
                        source: str, context: AnalysisContext) -> None:
        """Worker thread for analysis processing"""
        try:
            # Perform analysis
            analysis = self._analyze_data(data, source, context)
            
            # Generate stream outputs
            crisis_stream = self._generate_crisis_response(
                analysis,
                context
            )
            
            knowledge_stream = self._generate_knowledge_content(
                analysis,
                context
            )
            
            # Send results through bridge
            self.bridge.send_analysis_result(
                analysis_id,
                crisis_stream,
                knowledge_stream,
                context.session_id
            )
            
        except Exception as e:
            self.logger.error(f"Analysis worker error: {str(e)}")
            self.bridge.send_analysis_error(
                analysis_id,
                str(e),
                context.session_id
            )
        finally:
            with self._lock:
                # Cleanup
                self.active_analyses[analysis_id] = False
                self.analysis_queues.pop(analysis_id, None)
                self.analysis_threads.pop(analysis_id, None)
                
    def _analyze_data(self, data: List[Dict[str, Any]], source: str,
                     context: AnalysisContext) -> AnalysisResult:
        """Analyze collected security data"""
        try:
            # Identify patterns
            patterns = self._identify_patterns(data, context)
            
            # Assess threats
            threats = self._assess_threats(data, patterns, context)
            
            # Generate findings
            findings = self._generate_findings(
                data,
                patterns,
                threats,
                context
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                findings,
                threats,
                context
            )
            
            # Generate learning points
            learning_points = self._generate_learning_points(
                findings,
                threats,
                context
            )
            
            return AnalysisResult(
                findings=findings,
                patterns=patterns,
                threats=threats,
                recommendations=recommendations,
                learning_points=learning_points,
                timestamp=datetime.now(),
                session_id=context.session_id
            )
            
        except Exception as e:
            self.logger.error(f"Data analysis error: {str(e)}")
            raise
            
    def _identify_patterns(self, data: List[Dict[str, Any]],
                         context: AnalysisContext) -> List[Dict[str, Any]]:
        """Identify patterns in security data"""
        # TODO: Implement pattern identification with AI analyzer
        return []
        
    def _assess_threats(self, data: List[Dict[str, Any]],
                       patterns: List[Dict[str, Any]],
                       context: AnalysisContext) -> List[Dict[str, Any]]:
        """Assess threats from patterns"""
        # TODO: Implement threat assessment with AI analyzer
        return []
        
    def _generate_findings(self, data: List[Dict[str, Any]],
                         patterns: List[Dict[str, Any]],
                         threats: List[Dict[str, Any]],
                         context: AnalysisContext) -> List[Dict[str, Any]]:
        """Generate security findings"""
        # TODO: Implement finding generation with AI analyzer
        return []
        
    def _generate_recommendations(self, findings: List[Dict[str, Any]],
                                threats: List[Dict[str, Any]],
                                context: AnalysisContext) -> List[str]:
        """Generate security recommendations"""
        # TODO: Implement recommendation generation with AI analyzer
        return []
        
    def _generate_learning_points(self, findings: List[Dict[str, Any]],
                                threats: List[Dict[str, Any]],
                                context: AnalysisContext) -> List[str]:
        """Generate learning points"""
        # TODO: Implement learning point generation with AI analyzer
        return []
        
    def _get_initial_crisis_response(self, analysis_id: str) -> str:
        """Get initial crisis stream response"""
        return f"Starting security analysis {analysis_id}..."
        
    def _get_initial_knowledge_response(self, analysis_id: str) -> str:
        """Get initial knowledge stream response"""
        return f"Preparing analysis context {analysis_id}..."
        
    def _get_fallback_output(self, session_id: str) -> StreamOutput:
        """Generate fallback output for error cases"""
        return StreamOutput(
            crisis="Continuing security monitoring...",
            knowledge="System is analyzing security data...",
            timestamp=datetime.now(),
            metadata={
                'fallback': True,
                'session_id': session_id
            }
        )
        
    def _register_bridge_handlers(self) -> None:
        """Register handlers for bridge messages"""
        self.bridge.register_handler(
            "cancel_analysis",
            self._handle_cancel_analysis
        )
        
    def _handle_cancel_analysis(self, message: Dict[str, Any]) -> None:
        """Handle analysis cancellation request"""
        analysis_id = message.get("analysis_id")
        if not analysis_id:
            return
            
        with self._lock:
            if analysis_id in self.active_analyses:
                self.active_analyses[analysis_id] = False
</rewritten_file> """DōmAI Security Alliance Core Package

Version: 1.0.0
Authors: Claude & Joshua
"""

from .core.domai_framework import DōmAICore
from .core.orchestrator import SecurityOrchestrator
from .ai.analyzer import AIAnalyzer, SecurityContext, StreamOutput"""
Utility functions for DōmAI
"""

from .logging import setup_logging, get_logger # type: ignore
from .crypto import encrypt_data, decrypt_data # type: ignore
from .validation import validate_input, sanitize_command # type: ignore
from .system import get_system_info, check_permissions # type: ignore
from .formatting import format_output, colorize # type: ignore

__all__ = [
    'setup_logging',
    'get_logger',
    'encrypt_data',
    'decrypt_data',
    'validate_input',
    'sanitize_command',
    'get_system_info',
    'check_permissions',
    'format_output',
    'colorize'
]
"""
DōmAI Command Line Interface
Dual-stream interface with flexible output control
"""

import click
import json
import subprocess
import shlex
import sys
import threading
import queue
from pathlib import Path
from typing import Dict, Any, Optional, List, TextIO
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from .core.app import DomaiApp
from .core.analysis_pipeline import AnalysisScope
from .security.data_store import TimeRange

# Global application instance
app = DomaiApp()

class StreamConfig:
    """Configuration for output streams"""
    def __init__(self):
        self.crisis_stream = sys.stdout
        self.education_stream = sys.stdout
        self.education_file = None
        self.show_education = True
        
    def set_education_file(self, filepath: str):
        """Set file for educational content"""
        self.education_file = open(filepath, 'a')
        self.education_stream = self.education_file
        
    def close(self):
        """Clean up file handles"""
        if self.education_file:
            self.education_file.close()

# Global stream configuration
stream_config = StreamConfig()

@click.group()
def cli():
    """DōmAI - Just tell me what you need"""
    pass

@cli.command()
@click.argument('request', nargs=-1)
@click.option('--quiet', '-q', is_flag=True, help='Hide educational content from terminal')
@click.option('--education-file', '-f', help='Save educational content to file')
def help(request: tuple, quiet: bool, education_file: Optional[str]):
    """Just tell me what you need help with
    
    Examples:
    \b
    # Immediate help
    domai help my network activity is high
    
    # Hide educational content from terminal
    domai help -q my cpu is maxed out
    
    # Save educational content to file
    domai help -f learning.txt suspicious process running
    
    # Both quiet and save to file
    domai help -q -f learning.txt what is accessing my camera
    """
    # Configure streams
    if quiet:
        stream_config.show_education = False
    if education_file:
        stream_config.set_education_file(education_file)
    
    try:
        query = ' '.join(request)
        
        # Handle streams using threads
        _handle_streams(query)
    finally:
        # Cleanup
        stream_config.close()

def _handle_streams(query: str):
    """Handle both crisis and educational streams"""
    # Set up streaming response
    crisis_queue = queue.Queue()
    education_queue = queue.Queue()
    
    # Start the crisis and education streams
    producer_thread = threading.Thread(
        target=app.stream_response,
        args=(query, crisis_queue, education_queue),
        daemon=True
    )
    
    crisis_thread = threading.Thread(
        target=_handle_crisis_stream,
        args=(crisis_queue,),
        daemon=True
    )
    
    education_thread = threading.Thread(
        target=_handle_education_stream,
        args=(education_queue,),
        daemon=True
    )
    
    # Start all threads
    producer_thread.start()
    crisis_thread.start()
    education_thread.start()
    
    # Wait for all threads to complete
    producer_thread.join()
    crisis_thread.join()
    education_thread.join()

def _handle_crisis_stream(queue_obj: queue.Queue):
    """Handle crisis stream output"""
    while True:
        try:
            msg = queue_obj.get(timeout=1)  # 1 second timeout
            if msg is None:  # End of stream
                break
                
            if isinstance(msg, dict):
                if msg.get('type') == 'command':
                    # Execute command
                    cmd = msg['command']
                    click.echo(f"\n$ {cmd}", file=stream_config.crisis_stream)
                    try:
                        output = subprocess.check_output(
                            shlex.split(cmd),
                            stderr=subprocess.STDOUT,
                            text=True
                        )
                        click.echo(output, file=stream_config.crisis_stream)
                    except subprocess.CalledProcessError as e:
                        click.echo(f"Error: {e.output}", file=stream_config.crisis_stream)
                        
                elif msg.get('type') == 'analysis':
                    click.echo(f"\nAnalysis:", file=stream_config.crisis_stream)
                    click.echo(msg['content'], file=stream_config.crisis_stream)
                    
                elif msg.get('type') == 'action':
                    click.echo(f"\nRecommended Action:", file=stream_config.crisis_stream)
                    click.echo(f"- {msg['content']}", file=stream_config.crisis_stream)
            else:
                click.echo(msg, file=stream_config.crisis_stream)
                
            queue_obj.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            click.echo(f"Error in crisis stream: {str(e)}", file=sys.stderr)
            break

def _handle_education_stream(queue_obj: queue.Queue):
    """Handle educational stream output"""
    while True:
        try:
            msg = queue_obj.get(timeout=1)  # 1 second timeout
            if msg is None:  # End of stream
                break
                
            # Write to education stream if enabled
            if stream_config.show_education or stream_config.education_file:
                if isinstance(msg, dict):
                    if msg.get('type') == 'concept':
                        click.echo(f"\nConcept:", file=stream_config.education_stream)
                        click.echo(msg['content'], file=stream_config.education_stream)
                        
                    elif msg.get('type') == 'explanation':
                        click.echo(f"\nExplanation:", file=stream_config.education_stream)
                        click.echo(msg['content'], file=stream_config.education_stream)
                        
                    elif msg.get('type') == 'resource':
                        click.echo(f"\nResource:", file=stream_config.education_stream)
                        click.echo(f"- {msg['content']}", file=stream_config.education_stream)
                else:
                    click.echo(msg, file=stream_config.education_stream)
                    
            queue_obj.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            click.echo(f"Error in education stream: {str(e)}", file=sys.stderr)
            break

@cli.command()
@click.argument('command', nargs=-1)
@click.option('--quiet', '-q', is_flag=True, help='Hide educational content')
@click.option('--education-file', '-f', help='Save educational content to file')
def run(command: tuple, quiet: bool, education_file: Optional[str]):
    """Run commands with real-time dual stream output
    
    Examples:
    \b
    # Run with both streams
    domai run tcpdump -i any
    
    # Hide educational content
    domai run -q netstat -an
    
    # Save education to file
    domai run -f learning.txt ps aux
    """
    # Configure streams
    if quiet:
        stream_config.show_education = False
    if education_file:
        stream_config.set_education_file(education_file)
    
    try:
        cmd = ' '.join(command)
        _handle_command_streams(cmd)
    finally:
        stream_config.close()

def _handle_command_streams(cmd: str):
    """Handle streaming for command execution"""
    crisis_queue = queue.Queue()
    education_queue = queue.Queue()
    
    # Start command execution with streaming
    producer_thread = threading.Thread(
        target=app.stream_command_execution,
        args=(cmd, crisis_queue, education_queue),
        daemon=True
    )
    
    crisis_thread = threading.Thread(
        target=_handle_crisis_stream,
        args=(crisis_queue,),
        daemon=True
    )
    
    education_thread = threading.Thread(
        target=_handle_education_stream,
        args=(education_queue,),
        daemon=True
    )
    
    # Start all threads
    producer_thread.start()
    crisis_thread.start()
    education_thread.start()
    
    # Wait for all threads to complete
    producer_thread.join()
    crisis_thread.join()
    education_thread.join()

def main():
    """Main entry point"""
    try:
        cli()
    finally:
        # Ensure cleanup
        stream_config.close()

if __name__ == "__main__":
    main() """Core AI Analysis Engine for DōmAI

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
        
    def process_user_query(self, query: str, user_proficiency: str) -> Tuple[str, StreamOutput]:
        """Process natural language security query"""
        try:
            # Analyze query intent
            analysis = self._analyze_query_intent(query, user_proficiency)
            
            # Generate appropriate command if needed
            command = self._generate_security_command(analysis)
            
            # Generate dual-stream output
            output = StreamOutput(
                crisis=self._generate_crisis_response(analysis),
                knowledge=self._generate_knowledge_content(analysis),
                timestamp=datetime.now(),
                context_id=str(uuid.uuid4()),
                metadata={'command': command}
            )
            
            return command, output
            
        except Exception as e:
            logging.error(f"Query processing failed: {str(e)}")
            return None, self._get_fallback_output()

    def analyze_security_event(self, event: dict, context: SecurityContext) -> StreamOutput:
        """Analyze security event with dual-stream output"""
        try:
            # Add to context window
            self.context_window.append(event)
            
            # Get cached analysis if available
            cache_key = self._generate_cache_key(event)
            if cache_key in self.analysis_cache:
                return self.analysis_cache[cache_key]
            
            # Generate fresh analysis
            analysis = self._analyze_event(event, context)
            
            # Generate dual-stream output
            output = StreamOutput(
                crisis=self._format_crisis_analysis(analysis),
                knowledge=self._format_knowledge_analysis(analysis),
                timestamp=datetime.now(),
                context_id=str(uuid.uuid4()),
                metadata=analysis.get('metadata', {})
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
"""
AI/LLM integration for DōmAI
"""

from .analyzer import SecurityAnalyzer
from .nlp import NLProcessor
from .context import ContextManager
from .learning import AdaptiveEngine

__all__ = [
    'SecurityAnalyzer',
    'NLProcessor',
    'ContextManager',
    'AdaptiveEngine'
]
"""
Native bridge interface for DōmAI
"""

from .bridge import BridgeManager
from .ipc import IPCHandler
from .security import SecurityContext

__all__ = [
    'BridgeManager',
    'IPCHandler',
    'SecurityContext'
]
"""
System Resource and Security Monitor for DōmAI
Provides real-time system monitoring and analysis
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

class SystemMonitor:
    """Real-time system resource and security monitoring"""
    
    # Base resource thresholds
    BASE_THRESHOLDS = {
        'cpu_percent': 90.0,
        'memory_percent': 85.0,
        'disk_percent': 90.0,
        'network_io_bytes': 100000000,  # 100MB/s
        'process_count': 500
    }
    
    # Platform-specific thresholds
    PLATFORM_THRESHOLDS = {
        'darwin': {  # macOS
            'cpu_percent': 85.0,  # More conservative for laptop usage
            'memory_percent': 80.0,
            'disk_percent': 85.0,
            'network_io_bytes': 50000000,  # 50MB/s for wireless
            'process_count': 400
        },
        'linux': {
            'cpu_percent': 95.0,  # Server-grade thresholds
            'memory_percent': 90.0,
            'disk_percent': 95.0,
            'network_io_bytes': 200000000,  # 200MB/s for server NICs
            'process_count': 1000
        }
    }
    
    # Base security patterns
    BASE_PATTERNS = {
        'root_escalation': r'sudo|su\s|root',
        'shell_spawn': r'bash|sh\s|zsh|python\s',
        'file_access': r'cat\s|vim\s|nano\s|less\s',
        'network_tools': r'nc\s|netcat|nmap|wireshark',
        'crypto_mining': r'xmr|monero|btc|mining',
        'data_exfil': r'scp|rsync|sftp|curl'
    }
    
    # Platform-specific patterns
    PLATFORM_PATTERNS = {
        'darwin': {
            'root_escalation': r'sudo|su\s|root|dscl\s.*?-passwd',
            'system_control': r'launchctl|systemsetup|diskutil',
            'network_control': r'networksetup|pfctl|scutil',
            'kernel_ext': r'kextload|kextutil'
        },
        'linux': {
            'root_escalation': r'sudo|su\s|root|passwd|chroot',
            'system_control': r'systemctl|service|init\s',
            'network_control': r'iptables|netfilter|tc\s',
            'kernel_mod': r'modprobe|insmod|rmmod'
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
        self.baseline: Dict[str, Any] = {}
        self.suspicious_processes: Dict[str, Dict[str, Any]] = {}
        self.temp_files: List[Path] = []
        
        # Setup platform-specific configurations
        self._setup_platform_config()
        
        # Setup logging
        self.logger = logging.getLogger("domai.system")
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
                log_dir = Path("logs/system")
                if log_dir.exists() and not any(log_dir.iterdir()):
                    log_dir.rmdir()
            except Exception as e:
                self.logger.error(f"Failed to cleanup log directory: {e}")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
            
    def _setup_logging(self) -> None:
        """Setup secure logging"""
        try:
            log_dir = Path("logs/system")
            log_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(log_dir, 0o700)
            
            log_file = log_dir / "system.log"
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
            self.logger.error(f"Failed to setup system logging: {e}")
            
    def start(self) -> bool:
        """Start system monitoring"""
        try:
            with self._lock:
                if self.active:
                    return True
                    
                # Establish baseline
                self._establish_baseline()
                
                # Start monitoring
                self.active = True
                self.monitor_thread = threading.Thread(
                    target=self._monitor_system,
                    daemon=True
                )
                self.monitor_thread.start()
                
                # Start analysis
                self.analysis_thread = threading.Thread(
                    target=self._analyze_events,
                    daemon=True
                )
                self.analysis_thread.start()
                
                self.logger.info("System monitoring started")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start system monitoring: {e}")
            return False
            
    def stop(self) -> None:
        """Stop system monitoring"""
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
                
                self.logger.info("System monitoring stopped")
                
        except Exception as e:
            self.logger.error(f"Failed to stop system monitoring: {e}")
            
    def start_session(self, session_id: str) -> bool:
        """Start monitoring for a session"""
        try:
            with self._lock:
                if session_id in self.sessions:
                    return True
                    
                self.sessions[session_id] = {
                    'start_time': datetime.now(),
                    'suspicious_events': [],
                    'monitored_processes': set(),
                    'resource_usage': {},
                    'active': True,
                    'platform': {
                        'system': platform.system(),
                        'release': platform.release(),
                        'version': platform.version(),
                        'machine': platform.machine(),
                        'processor': platform.processor()
                    }
                }
                
                self.logger.info(f"Started system monitoring for session: {session_id}")
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
                    
                self.sessions[session_id]['active'] = False
                del self.sessions[session_id]
                
                self.logger.info(f"Stopped system monitoring for session: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop session monitoring: {e}")
            return False
            
    def register_event_handler(self, handler: callable) -> None:
        """Register event handler"""
        self.event_handlers.append(handler)
        
    def _establish_baseline(self) -> None:
        """Establish system baseline"""
        try:
            self.baseline = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'disk': {disk.mountpoint: psutil.disk_usage(disk.mountpoint)._asdict()
                        for disk in psutil.disk_partitions()},
                'network': psutil.net_io_counters()._asdict(),
                'process_count': len(psutil.pids()),
                'load_avg': os.getloadavg(),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to establish baseline: {e}")
            
    def _monitor_system(self) -> None:
        """Monitor system resources and processes"""
        while self.active:
            try:
                # Collect system metrics
                metrics = {
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory': psutil.virtual_memory()._asdict(),
                    'disk': {disk.mountpoint: psutil.disk_usage(disk.mountpoint)._asdict()
                            for disk in psutil.disk_partitions()},
                    'network': psutil.net_io_counters()._asdict(),
                    'process_count': len(psutil.pids()),
                    'load_avg': os.getloadavg(),
                    'timestamp': datetime.now()
                }
                
                # Check thresholds
                self._check_resource_thresholds(metrics)
                
                # Monitor processes
                self._monitor_processes()
                
                # Queue metrics
                self.event_queue.put({
                    'type': 'metrics',
                    'data': metrics
                })
                
            except Exception as e:
                self.logger.error(f"System monitoring error: {e}")
                
    def _check_resource_thresholds(self, metrics: Dict[str, Any]) -> None:
        """Check resource thresholds"""
        try:
            # CPU usage
            if metrics['cpu_percent'] > self.THRESHOLDS['cpu_percent']:
                self._handle_threshold_breach('cpu', metrics['cpu_percent'])
                
            # Memory usage
            if metrics['memory']['percent'] > self.THRESHOLDS['memory_percent']:
                self._handle_threshold_breach('memory', metrics['memory']['percent'])
                
            # Disk usage
            for mountpoint, usage in metrics['disk'].items():
                if usage['percent'] > self.THRESHOLDS['disk_percent']:
                    self._handle_threshold_breach('disk', usage['percent'], mountpoint)
                    
            # Network I/O
            net_io = metrics['network']
            total_io = net_io['bytes_sent'] + net_io['bytes_recv']
            if total_io > self.THRESHOLDS['network_io_bytes']:
                self._handle_threshold_breach('network', total_io)
                
            # Process count
            if metrics['process_count'] > self.THRESHOLDS['process_count']:
                self._handle_threshold_breach('process_count', metrics['process_count'])
                
        except Exception as e:
            self.logger.error(f"Failed to check resource thresholds: {e}")
            
    def _handle_threshold_breach(self, resource: str, value: float,
                               detail: str = None) -> None:
        """Handle resource threshold breach"""
        try:
            event = {
                'timestamp': datetime.now(),
                'type': 'threshold_breach',
                'resource': resource,
                'value': value,
                'threshold': self.THRESHOLDS.get(resource, 0),
                'detail': detail
            }
            
            self.event_queue.put(event)
            
        except Exception as e:
            self.logger.error(f"Failed to handle threshold breach: {e}")
            
    def _monitor_processes(self) -> None:
        """Monitor system processes"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username']):
                try:
                    proc_info = proc.info
                    cmdline = ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else ''
                    
                    # Check for suspicious patterns
                    for pattern_name, pattern in self.SUSPICIOUS_PATTERNS.items():
                        if re.search(pattern, cmdline, re.I):
                            self._handle_suspicious_process(
                                pattern_name,
                                proc_info,
                                cmdline
                            )
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"Failed to monitor processes: {e}")
            
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
                    'info': proc_info
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
                }
            }
            
            self.event_queue.put(event)
            
        except Exception as e:
            self.logger.error(f"Failed to handle suspicious process: {e}")
            
    def _analyze_events(self) -> None:
        """Analyze system events"""
        while self.active:
            try:
                # Get event from queue
                event = self.event_queue.get(timeout=1)
                
                # Update sessions
                self._notify_sessions(event)
                
                # Log event
                if event['type'] != 'metrics':
                    self.logger.warning(
                        f"System event: {event['type']} - {event.get('detail', '')}"
                    )
                    
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Event analysis error: {e}")
                
    def _notify_sessions(self, event: Dict[str, Any]) -> None:
        """Notify active sessions of system event"""
        try:
            for session_id, session in self.sessions.items():
                if session['active']:
                    event['session_id'] = session_id
                    
                    # Update session metrics
                    if event['type'] == 'metrics':
                        session['resource_usage'] = event['data']
                    elif event['type'] in ['threshold_breach', 'suspicious_process']:
                        session['suspicious_events'].append(event)
                        
                    # Notify event handlers
                    for handler in self.event_handlers:
                        try:
                            handler(event)
                        except Exception as e:
                            self.logger.error(f"Event handler error: {e}")
                            
        except Exception as e:
            self.logger.error(f"Failed to notify sessions: {e}")
            
    def get_session_metrics(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a session"""
        try:
            if session_id in self.sessions:
                return self.sessions[session_id]['resource_usage']
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get session metrics: {e}")
            return None
            
    def get_session_events(self, session_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get events for a session"""
        try:
            if session_id in self.sessions:
                return self.sessions[session_id]['suspicious_events']
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get session events: {e}")
            return None """
DōmAI Monitoring Package
Provides comprehensive monitoring capabilities
"""

from .manager import MonitoringManager
from .network import NetworkMonitor
from .system import SystemMonitor
from .process import ProcessMonitor

__all__ = [
    'MonitoringManager',
    'NetworkMonitor',
    'SystemMonitor',
    'ProcessMonitor'
]

# Version
__version__ = '1.0.0'

# Default monitoring manager instance
_default_manager = None

def get_manager() -> MonitoringManager:
    """Get the default monitoring manager instance"""
    global _default_manager
    if _default_manager is None:
        _default_manager = MonitoringManager()
    return _default_manager """
Network Security Monitor for DōmAI
Provides real-time network monitoring and analysis
"""

import logging
import threading
import queue
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import subprocess
import re
import psutil
import scapy.all as scapy
from pathlib import Path
import os
import sys
import signal
import shutil
import platform
import socket

class NetworkMonitor:
    """Real-time network security monitoring"""
    
    # Base network patterns
    BASE_PATTERNS = {
        'port_scan': r'(\d+\.){3}\d+.*SYN',
        'dns_tunnel': r'[a-zA-Z0-9-]{30,}\..*\.(com|net|org)',
        'data_exfil': r'POST.*transfer|upload|exfil',
        'c2_traffic': r'beaconing|heartbeat|check-in',
        'crypto_mining': r'(xmr|monero|btc|ethereum)',
        'tor_traffic': r'\.onion|tor2web|torproject'
    }
    
    # Platform-specific patterns
    PLATFORM_PATTERNS = {
        'darwin': {  # macOS
            'firewall_bypass': r'natpmp|upnp|bonjour',
            'vpn_detect': r'utun\d+|ppp\d+',
            'system_proxy': r'proximac|burp|charles',
            'mdns_exploit': r'\.local|_tcp\.local|_udp\.local'
        },
        'linux': {
            'container_escape': r'docker\.sock|containerd|cri-o',
            'tunnel_detect': r'tun\d+|tap\d+',
            'proxy_detect': r'squid|privoxy|polipo',
            'netfilter_bypass': r'raw\s+socket|libpcap'
        }
    }
    
    # Base packet filters
    BASE_FILTERS = {
        'tcp': 'tcp',
        'udp': 'udp',
        'icmp': 'icmp',
        'dns': 'udp port 53',
        'http': 'tcp port 80 or tcp port 443',
        'suspicious': 'tcp[13] = 0x02 or udp port 53'  # SYN packets or DNS
    }
    
    # Platform-specific filters
    PLATFORM_FILTERS = {
        'darwin': {
            'bonjour': 'udp port 5353',  # mDNS
            'airplay': 'tcp port 7000 or udp port 7011',
            'icloud': 'tcp port 443 and host *.icloud.com',
            'timemachine': 'tcp port 548 or udp port 548'
        },
        'linux': {
            'docker': 'tcp port 2375 or tcp port 2376',
            'kubernetes': 'tcp port 6443 or tcp port 10250',
            'systemd': 'tcp port 19531 or tcp port 19532',
            'journald': 'tcp port 19532'
        }
    }
    
    def __init__(self):
        self._lock = threading.Lock()
        self.active = False
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.packet_queue = queue.Queue()
        self.event_handlers: List[callable] = []
        self.capture_thread: Optional[threading.Thread] = None
        self.analysis_thread: Optional[threading.Thread] = None
        self.known_hosts: Set[str] = set()
        self.suspicious_ips: Dict[str, Dict[str, Any]] = {}
        self.temp_files: List[Path] = []
        
        # Setup platform-specific configurations
        self._setup_platform_config()
        
        # Setup logging
        self.logger = logging.getLogger("domai.network")
        self._setup_logging()
        
        # Setup signal handlers
        self._setup_signal_handlers()
        
    def _setup_platform_config(self) -> None:
        """Setup platform-specific configurations"""
        try:
            platform_name = sys.platform
            
            # Set patterns
            self.SUSPICIOUS_PATTERNS = self.BASE_PATTERNS.copy()
            if platform_name in self.PLATFORM_PATTERNS:
                self.SUSPICIOUS_PATTERNS.update(self.PLATFORM_PATTERNS[platform_name])
                
            # Set filters
            self.PACKET_FILTERS = self.BASE_FILTERS.copy()
            if platform_name in self.PLATFORM_FILTERS:
                self.PACKET_FILTERS.update(self.PLATFORM_FILTERS[platform_name])
                
            # Configure platform-specific network interfaces
            if platform_name == 'darwin':
                scapy.conf.use_pcap = True
                
        except Exception as e:
            self.logger.error(f"Failed to setup platform config: {e}")
            # Fall back to base configurations
            self.SUSPICIOUS_PATTERNS = self.BASE_PATTERNS
            self.PACKET_FILTERS = self.BASE_FILTERS
            
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
                log_dir = Path("logs/network")
                if log_dir.exists() and not any(log_dir.iterdir()):
                    log_dir.rmdir()
            except Exception as e:
                self.logger.error(f"Failed to cleanup log directory: {e}")
                
            # Clean up packet capture resources
            try:
                scapy.conf.reset()
            except Exception as e:
                self.logger.error(f"Failed to reset scapy configuration: {e}")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
            
    def _setup_logging(self) -> None:
        """Setup secure logging"""
        try:
            log_dir = Path("logs/network")
            log_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(log_dir, 0o700)
            
            log_file = log_dir / "network.log"
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
            self.logger.error(f"Failed to setup network logging: {e}")
            
    def start(self) -> bool:
        """Start network monitoring"""
        try:
            with self._lock:
                if self.active:
                    return True
                    
                # Start packet capture
                self.active = True
                self.capture_thread = threading.Thread(
                    target=self._capture_packets,
                    daemon=True
                )
                self.capture_thread.start()
                
                # Start analysis
                self.analysis_thread = threading.Thread(
                    target=self._analyze_packets,
                    daemon=True
                )
                self.analysis_thread.start()
                
                self.logger.info("Network monitoring started")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start network monitoring: {e}")
            return False
            
    def stop(self) -> None:
        """Stop network monitoring"""
        try:
            with self._lock:
                if not self.active:
                    return
                    
                self.active = False
                
                # Stop threads
                if self.capture_thread:
                    self.capture_thread.join(timeout=5)
                if self.analysis_thread:
                    self.analysis_thread.join(timeout=5)
                    
                # Cleanup resources
                self.cleanup()
                
                self.logger.info("Network monitoring stopped")
                
        except Exception as e:
            self.logger.error(f"Failed to stop network monitoring: {e}")
            
    def start_session(self, session_id: str) -> bool:
        """Start monitoring for a session"""
        try:
            with self._lock:
                if session_id in self.sessions:
                    return True
                    
                self.sessions[session_id] = {
                    'start_time': datetime.now(),
                    'suspicious_events': [],
                    'blocked_ips': set(),
                    'monitored_ports': set(),
                    'active': True,
                    'platform': {
                        'system': platform.system(),
                        'release': platform.release(),
                        'version': platform.version(),
                        'machine': platform.machine(),
                        'network_interfaces': self._get_network_interfaces()
                    }
                }
                
                self.logger.info(f"Started network monitoring for session: {session_id}")
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
                    
                self.sessions[session_id]['active'] = False
                del self.sessions[session_id]
                
                self.logger.info(f"Stopped network monitoring for session: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop session monitoring: {e}")
            return False
            
    def register_event_handler(self, handler: callable) -> None:
        """Register event handler"""
        self.event_handlers.append(handler)
        
    def handle_event(self, event: Dict[str, Any]) -> None:
        """Handle network security event"""
        try:
            event_type = event.get('type')
            session_id = event.get('session_id')
            
            if event_type == 'block_ip':
                self._block_ip(event['ip'], session_id)
            elif event_type == 'monitor_port':
                self._monitor_port(event['port'], session_id)
            elif event_type == 'analyze_traffic':
                self._analyze_traffic_pattern(event['pattern'], session_id)
                
        except Exception as e:
            self.logger.error(f"Failed to handle network event: {e}")
            
    def _capture_packets(self) -> None:
        """Capture network packets"""
        try:
            # Start packet capture with platform-specific filter
            filter_str = ' or '.join(self.PACKET_FILTERS.values())
            scapy.sniff(
                prn=self._process_packet,
                store=0,
                filter=filter_str,
                stop_filter=lambda _: not self.active
            )
        except Exception as e:
            self.logger.error(f"Packet capture error: {e}")
            
    def _process_packet(self, packet: scapy.Packet) -> None:
        """Process captured packet"""
        try:
            if not packet.haslayer(scapy.IP):
                return
                
            # Extract packet info
            ip_src = packet[scapy.IP].src
            ip_dst = packet[scapy.IP].dst
            
            # Update known hosts
            self.known_hosts.add(ip_src)
            self.known_hosts.add(ip_dst)
            
            # Queue for analysis
            self.packet_queue.put({
                'timestamp': datetime.now(),
                'src': ip_src,
                'dst': ip_dst,
                'proto': packet[scapy.IP].proto,
                'size': len(packet),
                'flags': self._get_tcp_flags(packet),
                'data': str(packet.payload)
            })
            
        except Exception as e:
            self.logger.error(f"Packet processing error: {e}")
            
    def _analyze_packets(self) -> None:
        """Analyze network packets"""
        while self.active:
            try:
                # Get packet from queue
                packet = self.packet_queue.get(timeout=1)
                
                # Check for suspicious patterns
                for pattern_name, pattern in self.SUSPICIOUS_PATTERNS.items():
                    if re.search(pattern, packet['data'], re.I):
                        self._handle_suspicious_traffic(
                            pattern_name,
                            packet
                        )
                        
                # Check for anomalies
                self._check_traffic_anomalies(packet)
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Packet analysis error: {e}")
                
    def _handle_suspicious_traffic(self, pattern_name: str,
                                 packet: Dict[str, Any]) -> None:
        """Handle suspicious network traffic"""
        try:
            # Update suspicious IPs tracking
            ip = packet['src']
            if ip not in self.suspicious_ips:
                self.suspicious_ips[ip] = {
                    'first_seen': datetime.now(),
                    'patterns': set(),
                    'count': 0
                }
            
            self.suspicious_ips[ip]['patterns'].add(pattern_name)
            self.suspicious_ips[ip]['count'] += 1
            
            # Generate event
            event = {
                'timestamp': datetime.now(),
                'type': 'suspicious_traffic',
                'pattern': pattern_name,
                'source_ip': ip,
                'destination_ip': packet['dst'],
                'details': {
                    'protocol': packet['proto'],
                    'size': packet['size'],
                    'flags': packet['flags']
                }
            }
            
            # Notify sessions
            self._notify_sessions(event)
            
        except Exception as e:
            self.logger.error(f"Failed to handle suspicious traffic: {e}")
            
    def _check_traffic_anomalies(self, packet: Dict[str, Any]) -> None:
        """Check for traffic anomalies"""
        try:
            ip = packet['src']
            
            # Check for port scanning
            if packet['flags'] == 'S' and ip in self.suspicious_ips:
                self._handle_port_scan(ip, packet)
                
            # Check for data exfiltration
            if packet['size'] > 10000:  # Large packets
                self._check_data_exfiltration(ip, packet)
                
            # Check for C2 traffic
            if self._check_c2_patterns(packet['data']):
                self._handle_c2_traffic(ip, packet)
                
        except Exception as e:
            self.logger.error(f"Failed to check traffic anomalies: {e}")
            
    def _handle_port_scan(self, ip: str, packet: Dict[str, Any]) -> None:
        """Handle potential port scanning"""
        try:
            # Update tracking
            if 'port_scans' not in self.suspicious_ips[ip]:
                self.suspicious_ips[ip]['port_scans'] = set()
            
            self.suspicious_ips[ip]['port_scans'].add(packet['dst'])
            
            # Check threshold
            if len(self.suspicious_ips[ip]['port_scans']) > 10:
                event = {
                    'timestamp': datetime.now(),
                    'type': 'port_scan',
                    'source_ip': ip,
                    'details': {
                        'scanned_ports': len(self.suspicious_ips[ip]['port_scans']),
                        'duration': (datetime.now() - self.suspicious_ips[ip]['first_seen']).seconds
                    }
                }
                
                self._notify_sessions(event)
                
        except Exception as e:
            self.logger.error(f"Failed to handle port scan: {e}")
            
    def _check_data_exfiltration(self, ip: str, packet: Dict[str, Any]) -> None:
        """Check for potential data exfiltration"""
        try:
            # Update tracking
            if 'data_exfil' not in self.suspicious_ips[ip]:
                self.suspicious_ips[ip]['data_exfil'] = {
                    'total_bytes': 0,
                    'start_time': datetime.now()
                }
            
            self.suspicious_ips[ip]['data_exfil']['total_bytes'] += packet['size']
            
            # Check threshold (1MB in 5 minutes)
            if self.suspicious_ips[ip]['data_exfil']['total_bytes'] > 1000000:
                duration = (datetime.now() - self.suspicious_ips[ip]['data_exfil']['start_time']).seconds
                if duration < 300:
                    event = {
                        'timestamp': datetime.now(),
                        'type': 'data_exfiltration',
                        'source_ip': ip,
                        'details': {
                            'bytes_transferred': self.suspicious_ips[ip]['data_exfil']['total_bytes'],
                            'duration': duration
                        }
                    }
                    
                    self._notify_sessions(event)
                    
        except Exception as e:
            self.logger.error(f"Failed to check data exfiltration: {e}")
            
    def _check_c2_patterns(self, data: str) -> bool:
        """Check for command and control patterns"""
        c2_patterns = [
            r'beacon\s*to\s*',
            r'check[-_]in',
            r'heartbeat',
            r'command\s*response',
            r'task\s*result'
        ]
        
        return any(re.search(pattern, data, re.I) for pattern in c2_patterns)
        
    def _handle_c2_traffic(self, ip: str, packet: Dict[str, Any]) -> None:
        """Handle potential C2 traffic"""
        try:
            # Update tracking
            if 'c2_traffic' not in self.suspicious_ips[ip]:
                self.suspicious_ips[ip]['c2_traffic'] = {
                    'count': 0,
                    'start_time': datetime.now()
                }
            
            self.suspicious_ips[ip]['c2_traffic']['count'] += 1
            
            # Check threshold (10 beacons in 5 minutes)
            if self.suspicious_ips[ip]['c2_traffic']['count'] > 10:
                duration = (datetime.now() - self.suspicious_ips[ip]['c2_traffic']['start_time']).seconds
                if duration < 300:
                    event = {
                        'timestamp': datetime.now(),
                        'type': 'c2_traffic',
                        'source_ip': ip,
                        'details': {
                            'beacon_count': self.suspicious_ips[ip]['c2_traffic']['count'],
                            'duration': duration
                        }
                    }
                    
                    self._notify_sessions(event)
                    
        except Exception as e:
            self.logger.error(f"Failed to handle C2 traffic: {e}")
            
    def _block_ip(self, ip: str, session_id: str) -> None:
        """Block an IP address"""
        try:
            if session_id in self.sessions:
                self.sessions[session_id]['blocked_ips'].add(ip)
                
                # Add platform-specific firewall rule
                if sys.platform == 'darwin':
                    subprocess.run([
                        'sudo', 'pfctl', '-t', 'domai-blocked', '-T', 'add', ip
                    ], check=True)
                elif sys.platform == 'linux':
                    subprocess.run([
                        'sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'
                    ], check=True)
                    
                self.logger.info(f"Blocked IP {ip} for session {session_id}")
                
        except Exception as e:
            self.logger.error(f"Failed to block IP {ip}: {e}")
            
    def _monitor_port(self, port: int, session_id: str) -> None:
        """Monitor specific port"""
        try:
            if session_id in self.sessions:
                self.sessions[session_id]['monitored_ports'].add(port)
                self.logger.info(f"Monitoring port {port} for session {session_id}")
                
        except Exception as e:
            self.logger.error(f"Failed to monitor port {port}: {e}")
            
    def _analyze_traffic_pattern(self, pattern: str, session_id: str) -> None:
        """Analyze specific traffic pattern"""
        try:
            if session_id in self.sessions:
                # Add custom pattern
                self.SUSPICIOUS_PATTERNS[f'custom_{session_id}'] = pattern
                self.logger.info(f"Added custom pattern for session {session_id}")
                
        except Exception as e:
            self.logger.error(f"Failed to analyze traffic pattern: {e}")
            
    def _notify_sessions(self, event: Dict[str, Any]) -> None:
        """Notify active sessions of security event"""
        try:
            for session_id, session in self.sessions.items():
                if session['active']:
                    event['session_id'] = session_id
                    
                    # Notify event handlers
                    for handler in self.event_handlers:
                        try:
                            handler(event)
                        except Exception as e:
                            self.logger.error(f"Event handler error: {e}")
                            
        except Exception as e:
            self.logger.error(f"Failed to notify sessions: {e}")
            
    def _get_tcp_flags(self, packet: scapy.Packet) -> str:
        """Get TCP flags from packet"""
        try:
            if packet.haslayer(scapy.TCP):
                flags = []
                if packet[scapy.TCP].flags & 0x02:  # SYN
                    flags.append('S')
                if packet[scapy.TCP].flags & 0x10:  # ACK
                    flags.append('A')
                if packet[scapy.TCP].flags & 0x01:  # FIN
                    flags.append('F')
                if packet[scapy.TCP].flags & 0x04:  # RST
                    flags.append('R')
                if packet[scapy.TCP].flags & 0x08:  # PSH
                    flags.append('P')
                if packet[scapy.TCP].flags & 0x20:  # URG
                    flags.append('U')
                return ''.join(flags)
        except Exception:
            pass
        return ''
        
    def _get_network_interfaces(self) -> Dict[str, Any]:
        """Get network interface information"""
        try:
            interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                interfaces[interface] = {
                    'addresses': [],
                    'stats': None
                }
                for addr in addrs:
                    if addr.family in (socket.AF_INET, socket.AF_INET6):
                        interfaces[interface]['addresses'].append({
                            'address': addr.address,
                            'netmask': addr.netmask,
                            'family': 'IPv4' if addr.family == socket.AF_INET else 'IPv6'
                        })
                        
                # Get interface stats
                try:
                    stats = psutil.net_if_stats()[interface]
                    interfaces[interface]['stats'] = {
                        'speed': stats.speed,
                        'mtu': stats.mtu,
                        'up': stats.isup,
                        'duplex': stats.duplex
                    }
                except Exception:
                    pass
                    
            return interfaces
            
        except Exception as e:
            self.logger.error(f"Failed to get network interfaces: {e}")
            return {}
</rewritten_file> """
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
            return None """
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
            return None """
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
            
        return sessions """
User management module
Handles user tracking and management
"""

import logging
import pwd
import grp
import subprocess
from typing import Optional, Dict, Any, List, Set
from pathlib import Path
from datetime import datetime

class UserManager:
    """Manage and track system users"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_users(self) -> List[Dict[str, Any]]:
        """Get list of system users"""
        try:
            users = []
            
            # Get all users from passwd
            for user in pwd.getpwall():
                try:
                    # Get user groups
                    groups = [g.gr_name for g in grp.getgrall() if user.pw_name in g.gr_mem]
                    primary_group = grp.getgrgid(user.pw_gid).gr_name
                    if primary_group not in groups:
                        groups.append(primary_group)
                        
                    users.append({
                        "username": user.pw_name,
                        "uid": user.pw_uid,
                        "gid": user.pw_gid,
                        "full_name": user.pw_gecos,
                        "home": user.pw_dir,
                        "shell": user.pw_shell,
                        "groups": groups
                    })
                except Exception as e:
                    self.logger.error(f"Error processing user {user.pw_name}: {str(e)}")
                    continue
                    
            return users
            
        except Exception as e:
            self.logger.error(f"Error getting users: {str(e)}")
            return []
            
    def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a user"""
        try:
            # Get basic user info
            user = pwd.getpwnam(username)
            
            # Get groups
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            primary_group = grp.getgrgid(user.pw_gid).gr_name
            if primary_group not in groups:
                groups.append(primary_group)
                
            # Get login history
            last_login = self._get_last_login(username)
            
            # Get processes
            processes = self._get_user_processes(username)
            
            return {
                "username": user.pw_name,
                "uid": user.pw_uid,
                "gid": user.pw_gid,
                "full_name": user.pw_gecos,
                "home": user.pw_dir,
                "shell": user.pw_shell,
                "groups": groups,
                "last_login": last_login,
                "processes": processes
            }
            
        except KeyError:
            self.logger.error(f"User not found: {username}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting user info: {str(e)}")
            return None
            
    def get_active_users(self) -> List[Dict[str, Any]]:
        """Get currently active users"""
        try:
            # Use who command
            cmd = ["who"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"who failed: {proc.stderr}")
                
            return self._parse_who_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting active users: {str(e)}")
            return []
            
    def get_login_history(self, username: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get user login history"""
        try:
            # Use last command
            cmd = ["last", "-100"]
            if username:
                cmd.append(username)
                
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"last failed: {proc.stderr}")
                
            return self._parse_last_output(proc.stdout, limit)
            
        except Exception as e:
            self.logger.error(f"Error getting login history: {str(e)}")
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
                raise Exception(f"lastb failed: {proc.stderr}")
                
            return self._parse_last_output(proc.stdout, limit)
            
        except Exception as e:
            self.logger.error(f"Error getting failed logins: {str(e)}")
            return []
            
    def _get_last_login(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user's last login"""
        try:
            history = self.get_login_history(username, 1)
            return history[0] if history else None
            
        except Exception as e:
            self.logger.error(f"Error getting last login: {str(e)}")
            return None
            
    def _get_user_processes(self, username: str) -> List[Dict[str, Any]]:
        """Get processes owned by user"""
        try:
            # Use ps command
            cmd = ["ps", "-u", username, "-o", "pid,ppid,%cpu,%mem,command"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"ps failed: {proc.stderr}")
                
            return self._parse_ps_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting user processes: {str(e)}")
            return []
            
    def _parse_who_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse who command output"""
        users = []
        
        try:
            for line in output.strip().split("\n"):
                if not line:
                    continue
                    
                parts = line.split()
                if len(parts) >= 5:
                    user = {
                        "username": parts[0],
                        "terminal": parts[1],
                        "date": " ".join(parts[2:5])
                    }
                    
                    # Add host if present
                    if len(parts) >= 6:
                        user["host"] = parts[5].strip("()")
                        
                    users.append(user)
                    
        except Exception as e:
            self.logger.error(f"Error parsing who output: {str(e)}")
            
        return users
        
    def _parse_last_output(self, output: str, limit: int) -> List[Dict[str, Any]]:
        """Parse last/lastb command output"""
        logins = []
        count = 0
        
        try:
            for line in output.strip().split("\n"):
                if not line or "wtmp begins" in line:
                    continue
                    
                if count >= limit:
                    break
                    
                parts = line.split()
                if len(parts) >= 9:
                    login = {
                        "username": parts[0],
                        "terminal": parts[1],
                        "host": parts[2] if parts[2] != ":" else None,
                        "date": " ".join(parts[3:8]),
                        "duration": parts[8] if parts[8] != "still" else "active"
                    }
                    logins.append(login)
                    count += 1
                    
        except Exception as e:
            self.logger.error(f"Error parsing last output: {str(e)}")
            
        return logins
        
    def _parse_ps_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse ps command output"""
        processes = []
        
        try:
            lines = output.strip().split("\n")
            if len(lines) < 2:  # Need header and at least one process
                return processes
                
            # Parse header
            headers = lines[0].lower().split()
            
            # Parse processes
            for line in lines[1:]:
                parts = line.split(None, len(headers) - 1)
                if len(parts) >= len(headers):
                    process = {}
                    for i, header in enumerate(headers):
                        # Convert numeric values
                        if header in ["pid", "ppid"]:
                            process[header] = int(parts[i])
                        elif header in ["%cpu", "%mem"]:
                            process[header] = float(parts[i])
                        else:
                            process[header] = parts[i]
                    processes.append(process)
                    
        except Exception as e:
            self.logger.error(f"Error parsing ps output: {str(e)}")
            
        return processes """
Access control monitoring module
Handles access control monitoring and management
"""

import logging
import subprocess
import pwd
import grp
from typing import Optional, Dict, Any, List, Set
from pathlib import Path
from datetime import datetime

class AccessMonitor:
    """Monitor access control and authentication"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_sudo_config(self) -> Dict[str, Any]:
        """Get sudo configuration"""
        try:
            # Read sudoers file
            cmd = ["sudo", "cat", "/etc/sudoers"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"Failed to read sudoers: {proc.stderr}")
                
            return self._parse_sudoers(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting sudo config: {str(e)}")
            return {}
            
    def get_pam_config(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get PAM configuration"""
        try:
            configs = {}
            
            # Common PAM service files
            pam_files = [
                "common-auth",
                "common-account",
                "common-password",
                "common-session",
                "sudo"
            ]
            
            # Read each PAM file
            for pam_file in pam_files:
                path = Path(f"/etc/pam.d/{pam_file}")
                if path.exists():
                    try:
                        text = path.read_text()
                        configs[pam_file] = self._parse_pam_config(text)
                    except Exception as e:
                        self.logger.error(f"Error reading {pam_file}: {str(e)}")
                        continue
                        
            return configs
            
        except Exception as e:
            self.logger.error(f"Error getting PAM config: {str(e)}")
            return {}
            
    def get_ssh_config(self) -> Dict[str, Any]:
        """Get SSH configuration"""
        try:
            config = {
                "allow_users": [],
                "deny_users": [],
                "allow_groups": [],
                "deny_groups": [],
                "settings": {}
            }
            
            # Read sshd config
            path = Path("/etc/ssh/sshd_config")
            if path.exists():
                text = path.read_text()
                config.update(self._parse_ssh_config(text))
                
            return config
            
        except Exception as e:
            self.logger.error(f"Error getting SSH config: {str(e)}")
            return {}
            
    def get_login_config(self) -> Dict[str, Any]:
        """Get login configuration"""
        try:
            config = {}
            
            # Read login.defs
            path = Path("/etc/login.defs")
            if path.exists():
                text = path.read_text()
                config["login_defs"] = self._parse_login_defs(text)
                
            # Read login.access
            path = Path("/etc/security/login.access")
            if path.exists():
                text = path.read_text()
                config["login_access"] = self._parse_login_access(text)
                
            return config
            
        except Exception as e:
            self.logger.error(f"Error getting login config: {str(e)}")
            return {}
            
    def check_user_access(self, username: str) -> Dict[str, bool]:
        """Check user's access permissions"""
        try:
            access = {
                "can_login": False,
                "can_sudo": False,
                "ssh_allowed": False,
                "is_locked": False
            }
            
            # Check if account is locked
            cmd = ["passwd", "-S", username]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode == 0:
                access["is_locked"] = "L" in proc.stdout
                
            # Check sudo access
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            access["can_sudo"] = "sudo" in groups or "admin" in groups or "wheel" in groups
            
            # Check SSH access
            ssh_config = self.get_ssh_config()
            
            if ssh_config["allow_users"] and username not in ssh_config["allow_users"]:
                access["ssh_allowed"] = False
            elif username in ssh_config["deny_users"]:
                access["ssh_allowed"] = False
            elif any(g in ssh_config["allow_groups"] for g in groups):
                access["ssh_allowed"] = True
            elif any(g in ssh_config["deny_groups"] for g in groups):
                access["ssh_allowed"] = False
            else:
                access["ssh_allowed"] = True
                
            # Check if user can login
            try:
                user = pwd.getpwnam(username)
                access["can_login"] = user.pw_shell not in ["/sbin/nologin", "/bin/false"]
            except KeyError:
                access["can_login"] = False
                
            return access
            
        except Exception as e:
            self.logger.error(f"Error checking user access: {str(e)}")
            return {
                "can_login": False,
                "can_sudo": False,
                "ssh_allowed": False,
                "is_locked": True
            }
            
    def _parse_sudoers(self, content: str) -> Dict[str, Any]:
        """Parse sudoers file content"""
        config = {
            "aliases": {
                "user": {},
                "runas": {},
                "host": {},
                "command": {}
            },
            "defaults": [],
            "rules": []
        }
        
        try:
            current_section = None
            
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                if line.startswith("User_Alias"):
                    current_section = "user"
                    config["aliases"]["user"].update(self._parse_alias(line))
                elif line.startswith("Runas_Alias"):
                    current_section = "runas"
                    config["aliases"]["runas"].update(self._parse_alias(line))
                elif line.startswith("Host_Alias"):
                    current_section = "host"
                    config["aliases"]["host"].update(self._parse_alias(line))
                elif line.startswith("Cmnd_Alias"):
                    current_section = "command"
                    config["aliases"]["command"].update(self._parse_alias(line))
                elif line.startswith("Defaults"):
                    config["defaults"].append(self._parse_defaults(line))
                else:
                    rule = self._parse_sudo_rule(line)
                    if rule:
                        config["rules"].append(rule)
                        
        except Exception as e:
            self.logger.error(f"Error parsing sudoers: {str(e)}")
            
        return config
        
    def _parse_pam_config(self, content: str) -> List[Dict[str, Any]]:
        """Parse PAM configuration file"""
        rules = []
        
        try:
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split()
                if len(parts) >= 3:
                    rule = {
                        "type": parts[0],
                        "control": parts[1],
                        "module": parts[2],
                        "args": parts[3:] if len(parts) > 3 else []
                    }
                    rules.append(rule)
                    
        except Exception as e:
            self.logger.error(f"Error parsing PAM config: {str(e)}")
            
        return rules
        
    def _parse_ssh_config(self, content: str) -> Dict[str, Any]:
        """Parse SSH configuration file"""
        config = {
            "allow_users": [],
            "deny_users": [],
            "allow_groups": [],
            "deny_groups": [],
            "settings": {}
        }
        
        try:
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0].lower()
                    value = " ".join(parts[1:])
                    
                    if key == "allowusers":
                        config["allow_users"].extend(value.split())
                    elif key == "denyusers":
                        config["deny_users"].extend(value.split())
                    elif key == "allowgroups":
                        config["allow_groups"].extend(value.split())
                    elif key == "denygroups":
                        config["deny_groups"].extend(value.split())
                    else:
                        config["settings"][key] = value
                        
        except Exception as e:
            self.logger.error(f"Error parsing SSH config: {str(e)}")
            
        return config
        
    def _parse_login_defs(self, content: str) -> Dict[str, Any]:
        """Parse login.defs file"""
        config = {}
        
        try:
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0]
                    value = " ".join(parts[1:])
                    config[key] = value
                    
        except Exception as e:
            self.logger.error(f"Error parsing login.defs: {str(e)}")
            
        return config
        
    def _parse_login_access(self, content: str) -> List[Dict[str, Any]]:
        """Parse login.access file"""
        rules = []
        
        try:
            for line in content.split("\n"):
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split(":")
                if len(parts) == 3:
                    rule = {
                        "permission": parts[0],
                        "users": parts[1].split(),
                        "origins": parts[2].split()
                    }
                    rules.append(rule)
                    
        except Exception as e:
            self.logger.error(f"Error parsing login.access: {str(e)}")
            
        return rules
        
    def _parse_alias(self, line: str) -> Dict[str, List[str]]:
        """Parse sudoers alias line"""
        aliases = {}
        
        try:
            parts = line.split("=", 1)
            if len(parts) == 2:
                name = parts[0].split()[-1]
                values = [v.strip() for v in parts[1].split(",")]
                aliases[name] = values
                
        except Exception as e:
            self.logger.error(f"Error parsing alias: {str(e)}")
            
        return aliases
        
    def _parse_defaults(self, line: str) -> Dict[str, Any]:
        """Parse sudoers defaults line"""
        defaults = {
            "type": "global",
            "target": None,
            "options": {}
        }
        
        try:
            parts = line.split()
            if ">" in parts[0]:
                defaults["type"] = "runas"
                defaults["target"] = parts[0].split(">")[1]
            elif ":" in parts[0]:
                defaults["type"] = "user"
                defaults["target"] = parts[0].split(":")[1]
            elif "@" in parts[0]:
                defaults["type"] = "host"
                defaults["target"] = parts[0].split("@")[1]
                
            for option in parts[1:]:
                if "=" in option:
                    key, value = option.split("=", 1)
                    defaults["options"][key] = value
                else:
                    defaults["options"][option] = True
                    
        except Exception as e:
            self.logger.error(f"Error parsing defaults: {str(e)}")
            
        return defaults
        
    def _parse_sudo_rule(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse sudoers rule line"""
        try:
            parts = line.split()
            if len(parts) >= 2:
                rule = {
                    "user": parts[0],
                    "host": "ALL",
                    "runas": "ALL",
                    "commands": []
                }
                
                # Parse host specification
                if parts[1] != "ALL":
                    rule["host"] = parts[1]
                    
                # Parse command specification
                cmd_part = " ".join(parts[2:])
                if "=" in cmd_part:
                    runas, cmds = cmd_part.split("=", 1)
                    if runas:
                        rule["runas"] = runas.strip("()")
                    rule["commands"] = [c.strip() for c in cmds.split(",")]
                else:
                    rule["commands"] = [cmd_part]
                    
                return rule
                
        except Exception as e:
            self.logger.error(f"Error parsing sudo rule: {str(e)}")
            
        return None """
Identity module
Provides user and access management capabilities
"""

from .users import UserManager
from .permissions import PermissionManager
from .sessions import SessionMonitor
from .access import AccessMonitor

__all__ = [
    'UserManager',
    'PermissionManager',
    'SessionMonitor',
    'AccessMonitor'
]
"""
Permission management module
Handles user and group permission management
"""

import logging
import pwd
import grp
import os
import stat
import subprocess
from typing import Optional, Dict, Any, List, Set
from pathlib import Path

class PermissionManager:
    """Manage user and group permissions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def check_user_permission(self, username: str, path: str) -> Dict[str, bool]:
        """Check user's permissions for a path"""
        try:
            # Get user info
            user = pwd.getpwnam(username)
            
            # Get user's groups
            groups = [g.gr_gid for g in grp.getgrall() if username in g.gr_mem]
            groups.append(user.pw_gid)
            
            # Get file info
            path_obj = Path(path)
            if not path_obj.exists():
                return {
                    "exists": False,
                    "read": False,
                    "write": False,
                    "execute": False
                }
                
            stat_result = path_obj.stat()
            
            # Check if user is owner
            is_owner = stat_result.st_uid == user.pw_uid
            # Check if user is in group
            in_group = stat_result.st_gid in groups
            
            mode = stat_result.st_mode
            
            return {
                "exists": True,
                "read": (
                    (is_owner and bool(mode & stat.S_IRUSR)) or
                    (in_group and bool(mode & stat.S_IRGRP)) or
                    bool(mode & stat.S_IROTH)
                ),
                "write": (
                    (is_owner and bool(mode & stat.S_IWUSR)) or
                    (in_group and bool(mode & stat.S_IWGRP)) or
                    bool(mode & stat.S_IWOTH)
                ),
                "execute": (
                    (is_owner and bool(mode & stat.S_IXUSR)) or
                    (in_group and bool(mode & stat.S_IXGRP)) or
                    bool(mode & stat.S_IXOTH)
                )
            }
            
        except KeyError:
            self.logger.error(f"User not found: {username}")
            return {"exists": False, "read": False, "write": False, "execute": False}
        except Exception as e:
            self.logger.error(f"Error checking permissions: {str(e)}")
            return {"exists": True, "read": False, "write": False, "execute": False}
            
    def get_user_capabilities(self, username: str) -> Dict[str, Any]:
        """Get user's system capabilities"""
        try:
            # Get user info
            user = pwd.getpwnam(username)
            
            # Get groups
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            primary_group = grp.getgrgid(user.pw_gid).gr_name
            if primary_group not in groups:
                groups.append(primary_group)
                
            # Check sudo access
            sudo_access = self._check_sudo_access(username)
            
            # Check admin group membership
            admin_groups = {"admin", "sudo", "wheel", "staff"}
            is_admin = bool(admin_groups.intersection(groups))
            
            return {
                "uid": user.pw_uid,
                "is_root": user.pw_uid == 0,
                "primary_group": primary_group,
                "groups": groups,
                "is_admin": is_admin,
                "sudo_access": sudo_access,
                "home_directory": user.pw_dir,
                "shell": user.pw_shell
            }
            
        except KeyError:
            self.logger.error(f"User not found: {username}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting capabilities: {str(e)}")
            return {}
            
    def get_group_permissions(self, group: str, path: str) -> Dict[str, bool]:
        """Check group's permissions for a path"""
        try:
            # Get group info
            group_info = grp.getgrnam(group)
            
            # Get file info
            path_obj = Path(path)
            if not path_obj.exists():
                return {
                    "exists": False,
                    "read": False,
                    "write": False,
                    "execute": False
                }
                
            stat_result = path_obj.stat()
            
            # Check if path belongs to group
            is_group = stat_result.st_gid == group_info.gr_gid
            
            mode = stat_result.st_mode
            
            return {
                "exists": True,
                "read": is_group and bool(mode & stat.S_IRGRP),
                "write": is_group and bool(mode & stat.S_IWGRP),
                "execute": is_group and bool(mode & stat.S_IXGRP)
            }
            
        except KeyError:
            self.logger.error(f"Group not found: {group}")
            return {"exists": False, "read": False, "write": False, "execute": False}
        except Exception as e:
            self.logger.error(f"Error checking group permissions: {str(e)}")
            return {"exists": True, "read": False, "write": False, "execute": False}
            
    def scan_user_permissions(self, 
                            username: str,
                            paths: List[str]
                            ) -> Dict[str, Dict[str, bool]]:
        """Scan multiple paths for user permissions"""
        results = {}
        
        try:
            for path in paths:
                try:
                    results[path] = self.check_user_permission(username, path)
                except Exception as e:
                    self.logger.error(f"Error checking {path}: {str(e)}")
                    results[path] = {
                        "exists": False,
                        "read": False,
                        "write": False,
                        "execute": False,
                        "error": str(e)
                    }
                    
        except Exception as e:
            self.logger.error(f"Error scanning permissions: {str(e)}")
            
        return results
        
    def get_effective_permissions(self, 
                                username: str,
                                path: str
                                ) -> Dict[str, Any]:
        """Get effective permissions including ACLs"""
        try:
            # Get basic permissions
            basic_perms = self.check_user_permission(username, path)
            
            # Get ACL permissions
            acl_perms = self._get_acl_permissions(username, path)
            
            # Get extended attributes
            xattrs = self._get_extended_attributes(path)
            
            return {
                "basic": basic_perms,
                "acl": acl_perms,
                "xattr": xattrs
            }
            
        except Exception as e:
            self.logger.error(f"Error getting effective permissions: {str(e)}")
            return {}
            
    def _check_sudo_access(self, username: str) -> bool:
        """Check if user has sudo access"""
        try:
            # Check sudo group membership
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            return "sudo" in groups or "admin" in groups or "wheel" in groups
            
        except Exception as e:
            self.logger.error(f"Error checking sudo access: {str(e)}")
            return False
            
    def _get_acl_permissions(self, username: str, path: str) -> Dict[str, bool]:
        """Get ACL permissions for path"""
        try:
            cmd = ["ls", "-le", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                return {"read": False, "write": False, "execute": False}
                
            return self._parse_acl_output(proc.stdout, username)
            
        except Exception as e:
            self.logger.error(f"Error getting ACL permissions: {str(e)}")
            return {"read": False, "write": False, "execute": False}
            
    def _get_extended_attributes(self, path: str) -> List[str]:
        """Get extended attributes of path"""
        try:
            cmd = ["xattr", "-l", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                return []
                
            return [line.strip() for line in proc.stdout.split("\n") if line.strip()]
            
        except Exception as e:
            self.logger.error(f"Error getting extended attributes: {str(e)}")
            return []
            
    def _parse_acl_output(self, output: str, username: str) -> Dict[str, bool]:
        """Parse ACL command output"""
        perms = {"read": False, "write": False, "execute": False}
        
        try:
            for line in output.split("\n"):
                if line.strip().startswith(f"user:{username}:"):
                    perm_str = line.split(":")[-1].strip()
                    perms["read"] = "r" in perm_str
                    perms["write"] = "w" in perm_str
                    perms["execute"] = "x" in perm_str
                    break
                    
        except Exception as e:
            self.logger.error(f"Error parsing ACL output: {str(e)}")
            
        return perms """
Network services monitoring module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class ServiceMonitor:
    """Monitor network services and daemons"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_listening_services(self) -> List[Dict[str, Any]]:
        """Get all network services listening for connections"""
        try:
            # Use lsof to get listening services
            cmd = ["lsof", "-i", "-P", "-n"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_listening_services(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"lsof failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting listening services: {str(e)}")
            return []
            
    def get_service_info(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific service"""
        try:
            # First check launchctl for the service
            cmd = ["launchctl", "list"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            services = self._parse_launchctl_output(proc.stdout)
            service = next((s for s in services if service_name in s["name"]), None)
            
            if service:
                # Get process info if running
                if service["pid"] > 0:
                    service["connections"] = self._get_process_connections(service["pid"])
                    service["ports"] = self._get_process_ports(service["pid"])
                    
            return service
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"launchctl failed: {e.stderr}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting service info: {str(e)}")
            return None
            
    def get_active_services(self) -> List[Dict[str, Any]]:
        """Get all active network services"""
        try:
            # Combine launchctl and netstat info
            services = []
            
            # Get launchctl services
            cmd = ["launchctl", "list"]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            launchd_services = self._parse_launchctl_output(proc.stdout)
            
            # Get network info for running services
            for service in launchd_services:
                if service["pid"] > 0:  # If service is running
                    service["connections"] = self._get_process_connections(service["pid"])
                    service["ports"] = self._get_process_ports(service["pid"])
                    if service["connections"] or service["ports"]:
                        services.append(service)
                        
            return services
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"launchctl failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting active services: {str(e)}")
            return []
            
    def _parse_listening_services(self, output: str) -> List[Dict[str, Any]]:
        """Parse lsof output for listening services"""
        services = []
        
        for line in output.split("\n")[1:]:  # Skip header
            if "LISTEN" in line:
                try:
                    parts = line.split()
                    if len(parts) >= 9:
                        service = {
                            "name": parts[0],
                            "pid": int(parts[1]),
                            "user": parts[2],
                            "protocol": parts[4],
                            "address": parts[8],
                            "state": "LISTENING"
                        }
                        services.append(service)
                except Exception as e:
                    self.logger.error(f"Error parsing service line: {str(e)}")
                    continue
                    
        return services
        
    def _parse_launchctl_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse launchctl list output"""
        services = []
        
        for line in output.split("\n")[1:]:  # Skip header
            try:
                parts = line.split()
                if len(parts) >= 3:
                    service = {
                        "pid": int(parts[0]) if parts[0] != "-" else 0,
                        "status": int(parts[1]) if parts[1] != "-" else 0,
                        "name": parts[2],
                        "connections": [],
                        "ports": []
                    }
                    services.append(service)
            except Exception as e:
                self.logger.error(f"Error parsing launchctl line: {str(e)}")
                continue
                
        return services
        
    def _get_process_connections(self, pid: int) -> List[Dict[str, Any]]:
        """Get network connections for a specific process"""
        try:
            cmd = ["lsof", "-i", "-a", "-p", str(pid), "-n", "-P"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            connections = []
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    try:
                        parts = line.split()
                        if len(parts) >= 9:
                            conn = {
                                "protocol": parts[4],
                                "address": parts[8],
                                "state": parts[9] if len(parts) > 9 else "UNKNOWN"
                            }
                            connections.append(conn)
                    except Exception as e:
                        self.logger.error(f"Error parsing connection: {str(e)}")
                        continue
                        
            return connections
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting process connections: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting process connections: {str(e)}")
            return []
            
    def _get_process_ports(self, pid: int) -> List[int]:
        """Get ports used by a specific process"""
        try:
            cmd = ["lsof", "-i", "-a", "-p", str(pid), "-n", "-P"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            ports = set()
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    try:
                        parts = line.split()
                        if len(parts) >= 9:
                            # Extract port from address field
                            addr = parts[8]
                            if ":" in addr:
                                port = int(addr.split(":")[-1])
                                ports.add(port)
                    except Exception as e:
                        self.logger.error(f"Error parsing port: {str(e)}")
                        continue
                        
            return sorted(list(ports))
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting process ports: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting process ports: {str(e)}")
            return []
"""
DNS monitoring and resolution module
"""

import logging
import subprocess
from typing import Dict, Any, List, Tuple
from pathlib import Path

class DNSMonitor:
    """Monitor DNS activity and resolution"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_dns_servers(self) -> List[str]:
        """Get configured DNS servers"""
        try:
            # Use scutil to get DNS servers
            cmd = ["scutil", "--dns"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_dns_servers(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"scutil failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting DNS servers: {str(e)}")
            return []
            
    def resolve_name(self, hostname: str) -> List[Dict[str, Any]]:
        """Resolve hostname to IP addresses"""
        try:
            # Use dig for DNS resolution
            cmd = ["dig", "+noall", "+answer", hostname]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_dig_output(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"dig failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error resolving hostname: {str(e)}")
            return []
            
    def get_local_cache(self) -> List[Dict[str, Any]]:
        """Get local DNS cache entries"""
        try:
            # Use dscacheutil to get DNS cache
            cmd = ["dscacheutil", "-q", "host"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_cache_entries(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"dscacheutil failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting DNS cache: {str(e)}")
            return []
            
    def check_dns_sec(self, domain: str) -> Dict[str, Any]:
        """Check DNSSEC status for domain"""
        try:
            # Use dig with DNSSEC checking
            cmd = ["dig", "+dnssec", "+multi", domain, "DNSKEY"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_dnssec_status(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"dig failed: {e.stderr}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            self.logger.error(f"Error checking DNSSEC: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def _parse_dns_servers(self, output: str) -> List[str]:
        """Parse scutil DNS server output"""
        servers = []
        
        for line in output.split("\n"):
            line = line.strip()
            if "nameserver[" in line and "]" in line:
                try:
                    # Extract server IP
                    server = line.split("]")[1].strip()
                    if server:
                        servers.append(server)
                except Exception as e:
                    self.logger.error(f"Error parsing DNS server line: {str(e)}")
                    continue
                    
        return servers
        
    def _parse_dig_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse dig command output"""
        records = []
        
        for line in output.split("\n"):
            if not line.strip():
                continue
                
            try:
                parts = line.split()
                if len(parts) >= 5:
                    record = {
                        "name": parts[0],
                        "ttl": int(parts[1]),
                        "class": parts[2],
                        "type": parts[3],
                        "data": parts[4]
                    }
                    records.append(record)
            except Exception as e:
                self.logger.error(f"Error parsing dig output line: {str(e)}")
                continue
                
        return records
        
    def _parse_cache_entries(self, output: str) -> List[Dict[str, Any]]:
        """Parse DNS cache entries"""
        entries = []
        current_entry = {}
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                continue
                
            if ":" in line:
                key, value = line.split(":", 1)
                current_entry[key.strip()] = value.strip()
                
        if current_entry:
            entries.append(current_entry)
            
        return entries
        
    def _parse_dnssec_status(self, output: str) -> Dict[str, Any]:
        """Parse DNSSEC status output"""
        status = {
            "enabled": False,
            "validated": False,
            "keys": []
        }
        
        for line in output.split("\n"):
            line = line.strip().lower()
            
            # Check for DNSSEC validation
            if "flags:" in line and "ad" in line:
                status["validated"] = True
                
            # Check for DNSKEY records
            if "dnskey" in line:
                status["enabled"] = True
                try:
                    # Extract key info
                    parts = line.split()
                    if len(parts) >= 7:
                        key = {
                            "flags": int(parts[4]),
                            "protocol": int(parts[5]),
                            "algorithm": int(parts[6])
                        }
                        status["keys"].append(key)
                except Exception as e:
                    self.logger.error(f"Error parsing DNSKEY line: {str(e)}")
                    continue
                    
        return status """
macOS firewall management module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
import shutil
from enum import Enum, auto

class FirewallStatus(Enum):
    """Firewall status enumeration"""
    ENABLED = auto()
    DISABLED = auto()
    ERROR = auto()

class FirewallManager:
    """Manage macOS packet filter firewall"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._pfctl_path = self._get_pfctl_path()
        
    def _get_pfctl_path(self) -> Path:
        """Get the full path to pfctl binary"""
        pfctl_path = shutil.which('pfctl')
        if not pfctl_path:
            raise RuntimeError("pfctl not found. Firewall management requires root privileges.")
        return Path(pfctl_path)

    def _run_pfctl_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run pfctl command with proper security checks"""
        if not self._pfctl_path.exists():
            raise FileNotFoundError("pfctl binary not found")
            
        cmd = [str(self._pfctl_path)] + args
        
        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=10  # Add timeout
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError("pfctl command timed out")

    def get_status(self) -> Dict[str, Union[str, FirewallStatus]]:
        """Get firewall status"""
        try:
            proc = self._run_pfctl_command(["-s", "info"])
            status_dict = self._parse_status(proc.stdout)
            
            # Add enum status
            status_dict["status"] = (FirewallStatus.ENABLED 
                                   if "Enabled" in proc.stdout 
                                   else FirewallStatus.DISABLED)
            return status_dict
            
        except Exception as e:
            self.logger.error(f"Error getting firewall status: {str(e)}")
            return {"status": FirewallStatus.ERROR, "message": str(e)}

    def get_rules(self) -> List[Dict[str, str]]:
        """Get current firewall rules"""
        try:
            proc = self._run_pfctl_command(["-s", "rules"])
            return self._parse_rules(proc.stdout)
        except Exception as e:
            self.logger.error(f"Error getting firewall rules: {str(e)}")
            return []

    def get_state(self) -> List[Dict[str, str]]:
        """Get firewall state table"""
        try:
            proc = self._run_pfctl_command(["-s", "state"])
            return self._parse_state(proc.stdout)
        except Exception as e:
            self.logger.error(f"Error getting firewall state: {str(e)}")
            return []

    def update_rules(self, rules_file: Path) -> bool:
        """Update firewall rules from file"""
        try:
            if not rules_file.exists():
                raise FileNotFoundError(f"Rules file not found: {rules_file}")
                
            if not rules_file.is_file():
                raise ValueError(f"Not a regular file: {rules_file}")
                
            proc = self._run_pfctl_command(["-f", str(rules_file)])
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating firewall rules: {str(e)}")
            return False

    # ... rest of the parsing methods remain the same ...#!/usr/bin/env python3
"""
DōmAI Port Scanner Module
Provides intelligent port scanning with real-time analysis and explanation
"""

import json
import socket
import nmap # type: ignore
import logging
import threading
from queue import Queue
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ScanType(Enum):
    QUICK = "quick"       # Quick TCP scan of common ports
    FULL = "full"         # Full TCP port scan
    STEALTH = "stealth"   # SYN scan (requires root)
    SERVICE = "service"   # Service version detection
    VULN = "vuln"        # Vulnerability scan

@dataclass
class PortInfo:
    """Port scan result with context"""
    port: int
    state: str
    service: Optional[str] = None
    version: Optional[str] = None
    cpe: Optional[str] = None  # Common Platform Enumeration
    vulns: List[Dict] = None
    context: Dict = None       # Additional context about the port/service

@dataclass
class ScanResult:
    """Complete scan result for a target"""
    target: str
    scan_type: ScanType
    timestamp: datetime
    ports: List[PortInfo]
    metadata: Dict
    raw_output: str

class PortScanner:
    """Intelligent port scanner with natural language analysis"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.scan_queue = Queue()
        self.scan_thread = None
        self.should_scan = False
        self.common_ports = {
            80: "Web server (HTTP)",
            443: "Secure web server (HTTPS)",
            22: "SSH remote access",
            21: "FTP file transfer",
            25: "Email server (SMTP)",
            53: "DNS server",
            3389: "Remote Desktop",
            445: "Microsoft-DS (File sharing)",
            139: "NetBIOS",
            23: "Telnet",
        }
        
        # Port categories for context
        self.port_categories = {
            "web": [80, 443, 8080, 8443],
            "email": [25, 110, 143, 587, 993],
            "database": [1433, 3306, 5432, 27017],
            "remote_access": [22, 23, 3389, 5900],
            "file_sharing": [21, 445, 139, 2049],
        }
        
    def scan_target(
        self, 
        target: str, 
        scan_type: ScanType = ScanType.QUICK,
        ports: Optional[str] = None,
        callback: Optional[callable] = None
    ) -> ScanResult:
        """Perform port scan with real-time analysis"""
        try:
            # Build nmap arguments
            args = self._build_nmap_args(scan_type, ports)
            
            # Run scan
            raw_output = self._run_scan(target, args)
            
            # Parse results
            ports_info = self._parse_scan_results(target)
            
            # Add context to results
            self._enrich_port_info(ports_info)
            
            result = ScanResult(
                target=target,
                scan_type=scan_type,
                timestamp=datetime.now(),
                ports=ports_info,
                metadata={"args": args},
                raw_output=raw_output
            )
            
            # Call callback if provided
            if callback:
                callback(result)
                
            return result
            
        except Exception as e:
            logging.error(f"Scan failed: {str(e)}")
            raise
            
    def analyze_scan(self, result: ScanResult, user_level: str) -> Tuple[str, str]:
        """Generate dual-stream analysis of scan results"""
        try:
            # Crisis stream - immediate security concerns
            crisis = self._generate_crisis_analysis(result)
            
            # Knowledge stream - educational context
            knowledge = self._generate_knowledge_analysis(result, user_level)
            
            return crisis, knowledge
            
        except Exception as e:
            logging.error(f"Analysis failed: {str(e)}")
            return self._get_fallback_analysis()
            
    def start_continuous_scan(
        self,
        target: str,
        scan_type: ScanType = ScanType.QUICK,
        interval: int = 300,  # 5 minutes
        callback: Optional[callable] = None
    ) -> None:
        """Start continuous scanning thread"""
        if self.scan_thread and self.scan_thread.is_alive():
            raise RuntimeError("Continuous scan already running")
            
        self.should_scan = True
        self.scan_thread = threading.Thread(
            target=self._continuous_scan_loop,
            args=(target, scan_type, interval, callback),
            daemon=True
        )
        self.scan_thread.start()
        
    def stop_continuous_scan(self) -> None:
        """Stop continuous scanning"""
        self.should_scan = False
        if self.scan_thread:
            self.scan_thread.join(timeout=5)
            self.scan_thread = None
            
    def _continuous_scan_loop(
        self,
        target: str,
        scan_type: ScanType,
        interval: int,
        callback: Optional[callable]
    ) -> None:
        """Background scanning loop"""
        while self.should_scan:
            try:
                result = self.scan_target(target, scan_type)
                if callback:
                    callback(result)
            except Exception as e:
                logging.error(f"Continuous scan error: {str(e)}")
            finally:
                # Sleep for interval
                for _ in range(interval):
                    if not self.should_scan:
                        break
                    threading.Event().wait(1)
            
    def _build_nmap_args(self, scan_type: ScanType, ports: Optional[str]) -> str:
        """Build appropriate nmap arguments"""
        args = []
        
        if scan_type == ScanType.QUICK:
            args.extend(["-F", "-T4"])  # Fast scan of common ports
        elif scan_type == ScanType.FULL:
            args.extend(["-p-", "-T4"])  # All ports
        elif scan_type == ScanType.STEALTH:
            args.extend(["-sS", "-T4"])  # SYN scan
        elif scan_type == ScanType.SERVICE:
            args.extend(["-sV", "-T4"])  # Version detection
        elif scan_type == ScanType.VULN:
            args.extend(["-sV", "--script vuln", "-T4"])  # Vuln scan
            
        if ports:
            args.extend(["-p", ports])
            
        return " ".join(args)
        
    def _run_scan(self, target: str, args: str) -> str:
        """Run nmap scan"""
        try:
            self.nm.scan(hosts=target, arguments=args)
            return self.nm.get_nmap_last_output()
        except Exception as e:
            logging.error(f"Scan execution failed: {str(e)}")
            raise
            
    def _parse_scan_results(self, target: str) -> List[PortInfo]:
        """Parse nmap results into structured data"""
        ports_info = []
        
        try:
            # Get scan data for target
            if target not in self.nm.all_hosts():
                return ports_info
                
            host = self.nm[target]
            
            # Parse each protocol
            for proto in host.all_protocols():
                ports = host[proto].keys()
                
                for port in ports:
                    port_data = host[proto][port]
                    
                    port_info = PortInfo(
                        port=port,
                        state=port_data["state"],
                        service=port_data.get("name"),
                        version=port_data.get("version"),
                        cpe=port_data.get("cpe", []),
                        vulns=[],
                        context={},
                    )
                    
                    ports_info.append(port_info)
                    
            return ports_info
            
        except Exception as e:
            logging.error(f"Results parsing failed: {str(e)}")
            return ports_info
            
    def _enrich_port_info(self, ports_info: List[PortInfo]):
        """Add context and categorization to port information"""
        for port_info in ports_info:
            # Add common port description
            if port_info.port in self.common_ports:
                port_info.context["description"] = self.common_ports[port_info.port]
                
            # Add category
            for category, ports in self.port_categories.items():
                if port_info.port in ports:
                    port_info.context["category"] = category
                    break
                    
            # Add security notes
            self._add_security_context(port_info)
            
    def _add_security_context(self, port_info: PortInfo):
        """Add security-relevant context to port"""
        context = port_info.context
        
        # Check for sensitive services
        if port_info.port in [22, 23, 3389]:
            context["security_note"] = "Remote access service - ensure strong authentication"
        elif port_info.port in [80, 443]:
            context["security_note"] = "Web service - check for security headers and HTTPS"
        elif port_info.port in [139, 445]:
            context["security_note"] = "File sharing service - verify access controls"
            
    def _generate_crisis_analysis(self, result: ScanResult) -> str:
        """Generate crisis stream analysis focusing on security issues"""
        issues = []
        
        # Check for high-risk open ports
        high_risk_ports = [23, 139, 445]  # telnet, NetBIOS, SMB
        for port_info in result.ports:
            if port_info.state == "open":
                if port_info.port in high_risk_ports:
                    issues.append(f"High-risk port {port_info.port} ({port_info.service}) is open")
                    
        # Check for version information
        unidentified = [p for p in result.ports 
                       if p.state == "open" and not p.version]
        if unidentified:
            issues.append(f"Unable to identify versions for {len(unidentified)} services")
            
        # Format crisis output
        if issues:
            return "Security Concerns Found:\n" + "\n".join(f"- {issue}" for issue in issues)
        return "No immediate security concerns found in port scan"
        
    def _generate_knowledge_analysis(self, result: ScanResult, user_level: str) -> str:
        """Generate educational knowledge stream based on user level"""
        knowledge = []
        
        # Basic port information
        open_ports = [p for p in result.ports if p.state == "open"]
        if user_level == "beginner":
            knowledge.append(f"Found {len(open_ports)} open ports")
            for port in open_ports:
                if port.port in self.common_ports:
                    knowledge.append(f"Port {port.port}: {self.common_ports[port.port]}")
                    
        # More detailed for intermediate users
        elif user_level == "intermediate":
            categories = {}
            for port in open_ports:
                category = next((c for c, ports in self.port_categories.items() 
                               if port.port in ports), "other")
                if category not in categories:
                    categories[category] = []
                categories[category].append(port)
                
            for category, ports in categories.items():
                knowledge.append(f"\n{category.title()} Services:")
                for port in ports:
                    service_info = f"Port {port.port}"
                    if port.service:
                        service_info += f" ({port.service})"
                    if port.version:
                        service_info += f" version {port.version}"
                    knowledge.append(f"- {service_info}")
                    
        # Advanced includes security context
        else:
            knowledge.extend(self._generate_advanced_analysis(open_ports))
            
        return "\n".join(knowledge)
        
    def _generate_advanced_analysis(self, open_ports: List[PortInfo]) -> List[str]:
        """Generate advanced analysis with security context"""
        analysis = []
        
        # Group by security risk
        high_risk = []
        medium_risk = []
        low_risk = []
        
        for port in open_ports:
            if port.port in [23, 139, 445]:  # High risk
                high_risk.append(port)
            elif port.port in [21, 80, 3389]:  # Medium risk
                medium_risk.append(port)
            else:
                low_risk.append(port)
                
        # Format analysis
        if high_risk:
            analysis.append("\nHigh Risk Services:")
            for port in high_risk:
                analysis.append(f"- Port {port.port}: {port.context.get('security_note', '')}")
                
        if medium_risk:
            analysis.append("\nMedium Risk Services:")
            for port in medium_risk:
                analysis.append(f"- Port {port.port}: {port.context.get('security_note', '')}")
                
        if low_risk:
            analysis.append("\nLow Risk Services:")
            for port in low_risk:
                analysis.append(f"- Port {port.port}: {port.service or 'Unknown service'}")
                
        return analysis
        
    def _get_fallback_analysis(self) -> Tuple[str, str]:
        """Generate fallback analysis when normal analysis fails"""
        return (
            "Unable to generate security analysis",
            "Port scan completed but analysis failed"
        )
"""
Network connection monitoring module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
#from pathlib import Path

class ConnectionMonitor:
    """Monitor network connections using native tools"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_connections(
        self,
        port: Optional[int] = None,
        protocol: Optional[str] = None,
        state: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get current network connections"""
        try:
            # Use netstat for connection info
            cmd = ["netstat", "-an"]
            if protocol:
                if protocol.lower() == "tcp":
                    cmd.append("-p tcp")
                elif protocol.lower() == "udp":
                    cmd.append("-p udp")
                    
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse connections
            connections = []
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    conn = self._parse_netstat_line(line)
                    if conn:
                        # Apply filters
                        if port and conn.get("local_port") != port and conn.get("remote_port") != port:
                            continue
                        if state and conn.get("state") != state:
                            continue
                        connections.append(conn)
                        
            return connections
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting connections: {str(e)}")
            return []
            
    def get_listening_ports(self) -> List[Dict[str, Any]]:
        """Get listening ports"""
        try:
            # Use lsof for listening ports
            cmd = ["lsof", "-i", "-n", "-P"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse listening ports
            listening = []
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if "LISTEN" in line:
                    port = self._parse_lsof_line(line)
                    if port:
                        listening.append(port)
                        
            return listening
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"lsof failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting listening ports: {str(e)}")
            return []
            
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        try:
            # Use netstat for statistics
            cmd = ["netstat", "-s"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse statistics
            return self._parse_netstat_stats(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting connection stats: {str(e)}")
            return {}
            
    def _parse_netstat_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single netstat output line"""
        try:
            parts = line.split()
            if len(parts) < 4:
                return None
                
            # Parse local and remote addresses
            local = parts[3]
            remote = parts[4] if len(parts) > 4 else ""
            
            local_parts = local.rsplit(".", 1)
            local_addr = local_parts[0]
            local_port = int(local_parts[1]) if len(local_parts) > 1 else None
            
            remote_parts = remote.rsplit(".", 1)
            remote_addr = remote_parts[0]
            remote_port = int(remote_parts[1]) if len(remote_parts) > 1 else None
            
            return {
                "protocol": parts[0],
                "local_addr": local_addr,
                "local_port": local_port,
                "remote_addr": remote_addr,
                "remote_port": remote_port,
                "state": parts[5] if len(parts) > 5 else None
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing netstat line: {str(e)}")
            return None
            
    def _parse_lsof_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single lsof output line"""
        try:
            parts = line.split()
            if len(parts) < 8:
                return None
                
            # Parse address and port
            addr_port = parts[8]
            addr_parts = addr_port.rsplit(":", 1)
            
            return {
                "command": parts[0],
                "pid": int(parts[1]),
                "user": parts[2],
                "fd": parts[3],
                "type": parts[4],
                "address": addr_parts[0],
                "port": int(addr_parts[1])
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing lsof line: {str(e)}")
            return None
            
    def _parse_netstat_stats(self, output: str) -> Dict[str, Any]:
        """Parse netstat statistics output"""
        stats = {
            "tcp": {},
            "udp": {},
            "ip": {},
            "icmp": {}
        }
        
        current_section = None
        
        for line in output.split("\n"):
            line = line.strip()
            
            if not line:
                continue
                
            # Detect section
            if "tcp:" in line.lower():
                current_section = "tcp"
                continue
            elif "udp:" in line.lower():
                current_section = "udp"
                continue
            elif "ip:" in line.lower():
                current_section = "ip"
                continue
            elif "icmp:" in line.lower():
                current_section = "icmp"
                continue
                
            if current_section and ":" in line:
                key, value = line.split(":", 1)
                try:
                    # Extract numeric value
                    value = int(''.join(filter(str.isdigit, value)))
                    stats[current_section][key.strip()] = value
                except ValueError:
                    continue
                    
        return stats def new_func():
    """
Network security module
Provides network monitoring, packet capture, and firewall management
"""

    from .packets import PacketCapture
    from .connections import ConnectionMonitor
    from .firewall import FirewallManager
    from .services import ServiceMonitor
    from .stats import NetworkStats
    from .dns import DNSMonitor

    __all__ = [
    'PacketCapture',
    'ConnectionMonitor',
    'FirewallManager',
    'ServiceMonitor',
    'NetworkStats',
    'DNSMonitor'
]

new_func()
"""
Network statistics monitoring module
"""

import logging
import subprocess
import re
import threading
from queue import Queue
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

class NetworkStats:
    """Monitor network interface statistics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.monitor_thread = None
        self.should_monitor = False
        self.stats_queue = Queue()
        
    def get_interface_stats(self, interface: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Get statistics for network interfaces"""
        try:
            # Use netstat for interface stats
            cmd = ["netstat", "-I"]
            if interface:
                cmd.append(interface)
            else:
                cmd.append("all")  # All interfaces
                
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_interface_stats(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting interface stats: {str(e)}")
            return {}
            
    def get_bandwidth_usage(self, interface: Optional[str] = None) -> Dict[str, Dict[str, float]]:
        """Get current bandwidth usage"""
        try:
            # Use nettop for bandwidth monitoring
            cmd = ["nettop", "-P", "-L", "1", "-n"]
            if interface:
                cmd.extend(["-d", interface])
                
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_bandwidth_usage(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"nettop failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting bandwidth usage: {str(e)}")
            return {}
            
    def get_protocol_stats(self) -> Dict[str, Dict[str, int]]:
        """Get protocol-specific statistics"""
        try:
            # Use netstat for protocol stats
            cmd = ["netstat", "-s"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_protocol_stats(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting protocol stats: {str(e)}")
            return {}
            
    def get_error_stats(self) -> Dict[str, Dict[str, int]]:
        """Get network error statistics"""
        try:
            # Use netstat for error stats
            cmd = ["netstat", "-s"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_error_stats(proc.stdout)
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"netstat failed: {e.stderr}")
            return {}
        except Exception as e:
            self.logger.error(f"Error getting error stats: {str(e)}")
            return {}
            
    def start_monitoring(
        self,
        interface: Optional[str] = None,
        interval: int = 5,
        callback: Optional[callable] = None
    ) -> None:
        """Start continuous network monitoring"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            raise RuntimeError("Monitoring already running")
            
        self.should_monitor = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interface, interval, callback),
            daemon=True
        )
        self.monitor_thread.start()
        
    def stop_monitoring(self) -> None:
        """Stop continuous monitoring"""
        self.should_monitor = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            self.monitor_thread = None
            
    def _monitor_loop(
        self,
        interface: Optional[str],
        interval: int,
        callback: Optional[callable]
    ) -> None:
        """Background monitoring loop"""
        while self.should_monitor:
            try:
                stats = {
                    "interface": self.get_interface_stats(interface),
                    "bandwidth": self.get_bandwidth_usage(interface),
                    "protocol": self.get_protocol_stats(),
                    "errors": self.get_error_stats()
                }
                
                if callback:
                    callback(stats)
                else:
                    self.stats_queue.put(stats)
                    
            except Exception as e:
                self.logger.error(f"Monitoring error: {str(e)}")
            finally:
                # Sleep for interval
                for _ in range(interval):
                    if not self.should_monitor:
                        break
                    threading.Event().wait(1)
            
    def _parse_interface_stats(self, output: str) -> Dict[str, Dict[str, Any]]:
        """Parse netstat interface statistics"""
        stats = {}
        current_interface = None
        
        lines = output.split("\n")
        if len(lines) < 2:  # Need at least header and one interface
            return stats
            
        # Get header fields
        headers = [h.lower() for h in lines[0].split()]
        
        # Parse each interface line
        for line in lines[1:]:
            if not line.strip():
                continue
                
            parts = line.split()
            if len(parts) >= len(headers):
                interface = parts[0]
                stats[interface] = {}
                
                # Map values to headers
                for i, header in enumerate(headers[1:], 1):
                    try:
                        stats[interface][header] = int(parts[i])
                    except ValueError:
                        stats[interface][header] = parts[i]
                        
        return stats
        
    def _parse_bandwidth_usage(self, output: str) -> Dict[str, Dict[str, float]]:
        """Parse nettop bandwidth output"""
        usage = {}
        
        for line in output.split("\n"):
            if not line.strip() or "." not in line:  # Skip headers and empty lines
                continue
                
            try:
                parts = line.split()
                if len(parts) >= 3:
                    process = parts[0]
                    if process not in usage:
                        usage[process] = {"in": 0.0, "out": 0.0}
                        
                    # Parse bandwidth values
                    for i, value in enumerate(parts[1:3]):
                        try:
                            # Convert to bytes/sec
                            num = float(re.findall(r'[\d.]+', value)[0])
                            unit = re.findall(r'[A-Za-z]+', value)[0].upper()
                            
                            if unit.startswith('K'):
                                num *= 1024
                            elif unit.startswith('M'):
                                num *= 1024 * 1024
                            elif unit.startswith('G'):
                                num *= 1024 * 1024 * 1024
                                
                            if i == 0:
                                usage[process]["in"] = num
                            else:
                                usage[process]["out"] = num
                        except (ValueError, IndexError):
                            continue
                            
            except Exception as e:
                self.logger.error(f"Error parsing bandwidth line: {str(e)}")
                continue
                
        return usage
        
    def _parse_protocol_stats(self, output: str) -> Dict[str, Dict[str, int]]:
        """Parse protocol statistics"""
        stats = {
            "tcp": {},
            "udp": {},
            "ip": {},
            "icmp": {}
        }
        
        current_protocol = None
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            # Detect protocol section
            lower_line = line.lower()
            if "tcp:" in lower_line:
                current_protocol = "tcp"
                continue
            elif "udp:" in lower_line:
                current_protocol = "udp"
                continue
            elif "ip:" in lower_line:
                current_protocol = "ip"
                continue
            elif "icmp:" in lower_line:
                current_protocol = "icmp"
                continue
                
            # Parse stats within current protocol section
            if current_protocol and ":" in line:
                key, value = line.split(":", 1)
                try:
                    # Extract numeric value
                    num = int(''.join(filter(str.isdigit, value)))
                    stats[current_protocol][key.strip()] = num
                except ValueError:
                    continue
                    
        return stats
        
    def _parse_error_stats(self, output: str) -> Dict[str, Dict[str, int]]:
        """Parse error statistics"""
        errors = {
            "tcp": {},
            "udp": {},
            "ip": {},
            "interface": {}
        }
        
        current_section = None
        error_keywords = ["error", "drop", "timeout", "fail", "invalid", "reset"]
        
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            # Detect section
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in error_keywords):
                try:
                    if "tcp:" in lower_line:
                        current_section = "tcp"
                    elif "udp:" in lower_line:
                        current_section = "udp"
                    elif "ip:" in lower_line:
                        current_section = "ip"
                    else:
                        current_section = "interface"
                        
                    if ":" in line:
                        key, value = line.split(":", 1)
                        try:
                            # Extract numeric value
                            num = int(''.join(filter(str.isdigit, value)))
                            errors[current_section][key.strip()] = num
                        except ValueError:
                            continue
                            
                except Exception as e:
                    self.logger.error(f"Error parsing error stats line: {str(e)}")
                    continue
                    
        return errors
"""
Network packet capture and analysis module
"""

import logging
import subprocess
import threading
from typing import Optional, Dict, Any, List
from pathlib import Path

class PacketCapture:
    """Packet capture using tcpdump"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.process: Optional[subprocess.Popen] = None
        self.capture_thread: Optional[threading.Thread] = None
        self.should_capture = False
        
    def start_capture(
        self,
        interface: str = "any",
        port: Optional[int] = None,
        host: Optional[str] = None,
        protocol: Optional[str] = None,
        output_file: Optional[Path] = None,
        callback: Optional[callable] = None
    ) -> bool:
        """Start packet capture with given filters"""
        try:
            # Build tcpdump command
            cmd = ["tcpdump", "-i", interface, "-n"]
            
            # Add filters
            if port:
                cmd.extend(["port", str(port)])
            if host:
                cmd.extend(["host", host])
            if protocol:
                cmd.append(protocol)
                
            # Add output file if specified
            if output_file:
                cmd.extend(["-w", str(output_file)])
            else:
                cmd.append("-l")  # Line-buffered output
                
            # Start capture process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Start capture thread if callback provided
            if callback and not output_file:
                self.should_capture = True
                self.capture_thread = threading.Thread(
                    target=self._capture_loop,
                    args=(callback,),
                    daemon=True
                )
                self.capture_thread.start()
            
            self.logger.info(f"Started packet capture: {' '.join(cmd)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start packet capture: {str(e)}")
            return False
            
    def stop_capture(self) -> None:
        """Stop packet capture"""
        if self.process:
            try:
                self.should_capture = False
                self.process.terminate()
                self.process.wait(timeout=5)
                if self.capture_thread:
                    self.capture_thread.join(timeout=5)
                self.logger.info("Stopped packet capture")
            except Exception as e:
                self.logger.error(f"Error stopping packet capture: {str(e)}")
            finally:
                self.process = None
                self.capture_thread = None
                
    def get_stats(self) -> Dict[str, Any]:
        """Get capture statistics"""
        if not self.process:
            return {"status": "not running"}
            
        try:
            # Get process stats
            proc = subprocess.run(
                ["ps", "-p", str(self.process.pid), "-o", "%cpu,%mem"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse stats
            stats = proc.stdout.split("\n")[1].strip().split()
            return {
                "status": "running",
                "pid": self.process.pid,
                "cpu_percent": float(stats[0]),
                "memory_percent": float(stats[1])
            }
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting process stats: {e.stderr}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            self.logger.error(f"Error getting capture stats: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def analyze_capture(
        self,
        capture_file: Path,
        filters: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """Analyze captured packets"""
        try:
            # Build tcpdump read command
            cmd = ["tcpdump", "-r", str(capture_file), "-nn", "-v"]
            
            # Add any filters
            if filters:
                for key, value in filters.items():
                    cmd.extend([key, value])
                    
            # Run analysis
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse output into structured data
            packets = []
            for line in proc.stdout.split("\n"):
                if line.strip():
                    packet = self._parse_packet_line(line)
                    if packet:
                        packets.append(packet)
                        
            return packets
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Analysis failed: {e.stderr}")
            return []
        except Exception as e:
            self.logger.error(f"Error analyzing capture: {str(e)}")
            return []
            
    def _capture_loop(self, callback: callable) -> None:
        """Background capture loop"""
        try:
            while self.should_capture and self.process:
                line = self.process.stdout.readline()
                if not line:
                    break
                packet = self._parse_packet_line(line)
                if packet:
                    callback(packet)
        except Exception as e:
            self.logger.error(f"Error in capture loop: {str(e)}")
            
    def _parse_packet_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single packet line from tcpdump output"""
        try:
            # Basic parsing - can be enhanced based on needs
            parts = line.split()
            if len(parts) < 3:
                return None
                
            return {
                "timestamp": parts[0],
                "protocol": parts[1],
                "details": " ".join(parts[2:])
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing packet line: {str(e)}")
            return None """
System services monitoring module
Handles launchctl service monitoring and management
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class ServiceMonitor:
    """Monitor and manage system services via launchctl"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def list_services(self) -> List[Dict[str, Any]]:
        """List all services"""
        try:
            # Use launchctl list for service info
            cmd = ["launchctl", "list"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_service_list(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error listing services: {str(e)}")
            return []
            
    def get_service_info(self, label: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific service"""
        try:
            # Use launchctl print for detailed info
            cmd = ["launchctl", "print", label]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_service_info(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting service info: {str(e)}")
            return None
            
    def get_service_status(self, label: str) -> Dict[str, Any]:
        """Get current status of a service"""
        try:
            # Use launchctl print for status
            cmd = ["launchctl", "print", label]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_service_status(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting service status: {str(e)}")
            return {"status": "error", "error": str(e)}
            
    def find_service_plist(self, label: str) -> Optional[Path]:
        """Find plist file for a service"""
        try:
            # Common plist locations
            locations = [
                Path("/Library/LaunchDaemons"),
                Path("/Library/LaunchAgents"),
                Path.home() / "Library/LaunchAgents",
                Path("/System/Library/LaunchDaemons"),
                Path("/System/Library/LaunchAgents")
            ]
            
            for location in locations:
                if not location.exists():
                    continue
                    
                plist = location / f"{label}.plist"
                if plist.exists():
                    return plist
                    
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding service plist: {str(e)}")
            return None
            
    def _parse_service_list(self, output: str) -> List[Dict[str, Any]]:
        """Parse launchctl list output"""
        services = []
        
        try:
            lines = output.strip().split("\n")
            
            for line in lines[1:]:  # Skip header
                if not line.strip():
                    continue
                    
                parts = line.split()
                if len(parts) >= 3:
                    service = {
                        "pid": parts[0] if parts[0] != "-" else None,
                        "status": parts[1],
                        "label": " ".join(parts[2:])
                    }
                    services.append(service)
                    
        except Exception as e:
            self.logger.error(f"Error parsing service list: {str(e)}")
            
        return services
        
    def _parse_service_info(self, output: str) -> Dict[str, Any]:
        """Parse service info output"""
        info = {
            "state": {},
            "config": {}
        }
        
        try:
            current_section = None
            
            for line in output.split("\n"):
                line = line.strip()
                if not line:
                    continue
                    
                if line.endswith(":"):
                    current_section = line[:-1].lower()
                    info[current_section] = {}
                elif "=" in line and current_section:
                    key, value = line.split("=", 1)
                    info[current_section][key.strip()] = value.strip()
                    
        except Exception as e:
            self.logger.error(f"Error parsing service info: {str(e)}")
            
        return info
        
    def _parse_service_status(self, output: str) -> Dict[str, Any]:
        """Parse service status output"""
        status = {
            "status": "unknown",
            "pid": None,
            "exit_code": None
        }
        
        try:
            for line in output.split("\n"):
                line = line.strip()
                
                if "state = running" in line.lower():
                    status["status"] = "running"
                elif "state = waiting" in line.lower():
                    status["status"] = "waiting"
                elif "state = stopped" in line.lower():
                    status["status"] = "stopped"
                    
                if "pid =" in line.lower():
                    try:
                        status["pid"] = int(line.split("=")[1].strip())
                    except (ValueError, IndexError):
                        pass
                        
                if "last exit code =" in line.lower():
                    try:
                        status["exit_code"] = int(line.split("=")[1].strip())
                    except (ValueError, IndexError):
                        pass
                        
        except Exception as e:
            self.logger.error(f"Error parsing service status: {str(e)}")
            
        return status
</rewritten_file> """
Kernel monitoring and management module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class KernelMonitor:
    """Monitor kernel parameters and system messages"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_kernel_info(self) -> Dict[str, Any]:
        """Get kernel information"""
        try:
            # Use sysctl for kernel info
            cmd = ["sysctl", "-a"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_sysctl_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting kernel info: {str(e)}")
            return {}
            
    def get_system_messages(self, lines: int = 100) -> List[Dict[str, Any]]:
        """Get recent system messages"""
        try:
            # Use dmesg for system messages
            cmd = ["dmesg"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_dmesg_output(proc.stdout, lines)
            
        except Exception as e:
            self.logger.error(f"Error getting system messages: {str(e)}")
            return []
            
    def get_kernel_extensions(self) -> List[Dict[str, Any]]:
        """Get loaded kernel extensions"""
        try:
            # Use kextstat for kernel extensions
            cmd = ["kextstat"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_kextstat_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting kernel extensions: {str(e)}")
            return []
            
    def get_boot_args(self) -> Dict[str, str]:
        """Get boot arguments"""
        try:
            # Use nvram for boot args
            cmd = ["nvram", "boot-args"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_nvram_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting boot args: {str(e)}")
            return {}
            
    def _parse_sysctl_output(self, output: str) -> Dict[str, Any]:
        """Parse sysctl command output"""
        info = {}
        
        for line in output.split("\n"):
            if ":" in line:
                try:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Try to convert numeric values
                    try:
                        if "." in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                        
                    info[key] = value
                except Exception as e:
                    self.logger.error(f"Error parsing sysctl line: {str(e)}")
                    continue
                    
        return info
        
    def _parse_dmesg_output(self, output: str, limit: int) -> List[Dict[str, Any]]:
        """Parse dmesg command output"""
        messages = []
        
        for line in output.split("\n")[-limit:]:
            if not line.strip():
                continue
                
            try:
                # Parse timestamp and message
                parts = line.split(None, 1)
                if len(parts) >= 2:
                    messages.append({
                        "timestamp": parts[0],
                        "message": parts[1]
                    })
            except Exception as e:
                self.logger.error(f"Error parsing dmesg line: {str(e)}")
                continue
                
        return messages
        
    def _parse_kextstat_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse kextstat command output"""
        extensions = []
        
        for line in output.split("\n")[1:]:  # Skip header
            if not line.strip():
                continue
                
            try:
                parts = line.split()
                if len(parts) >= 6:
                    extension = {
                        "index": int(parts[0]),
                        "refs": int(parts[1]),
                        "address": parts[2],
                        "size": parts[3],
                        "wired": parts[4],
                        "name": parts[5]
                    }
                    
                    # Add version if present
                    if len(parts) > 6:
                        extension["version"] = parts[6].strip("()")
                        
                    extensions.append(extension)
            except Exception as e:
                self.logger.error(f"Error parsing kextstat line: {str(e)}")
                continue
                
        return extensions
        
    def _parse_nvram_output(self, output: str) -> Dict[str, str]:
        """Parse nvram command output"""
        args = {}
        
        if "boot-args" in output:
            try:
                # Extract boot args
                value = output.split("boot-args", 1)[1].strip()
                
                # Parse individual arguments
                for arg in value.split():
                    if "=" in arg:
                        key, val = arg.split("=", 1)
                        args[key] = val
                    else:
                        args[arg] = ""
                        
            except Exception as e:
                self.logger.error(f"Error parsing boot args: {str(e)}")
                
        return args
``` """
System monitoring module
Provides system-level monitoring and management capabilities
"""

from .processes import ProcessMonitor
from .kernel import KernelMonitor
from .hardware import HardwareMonitor
from .services import ServiceMonitor

__all__ = [
    'ProcessMonitor',
    'KernelMonitor',
    'HardwareMonitor',
    'ServiceMonitor'
]
"""
Process monitoring and management module
"""

import logging
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

class ProcessMonitor:
    """Monitor system processes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_processes(self, user: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get running processes"""
        try:
            # Use ps for process info
            cmd = ["ps", "-ax", "-o", "pid,ppid,user,%cpu,%mem,state,lstart,command"]
            if user:
                cmd.extend(["-u", user])
                
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_ps_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting processes: {str(e)}")
            return []
            
    def get_process_info(self, pid: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific process"""
        try:
            # Get basic process info
            cmd = ["ps", "-p", str(pid), "-o", "pid,ppid,user,%cpu,%mem,state,lstart,command"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            processes = self._parse_ps_output(proc.stdout)
            if not processes:
                return None
                
            process = processes[0]
            
            # Add additional info
            process["files"] = self._get_open_files(pid)
            process["ports"] = self._get_network_ports(pid)
            process["env"] = self._get_environment(pid)
            
            return process
            
        except Exception as e:
            self.logger.error(f"Error getting process info: {str(e)}")
            return None
            
    def get_process_tree(self, pid: Optional[int] = None) -> Dict[int, Dict[str, Any]]:
        """Get process tree"""
        try:
            # Get all processes
            processes = self.get_processes()
            
            # Build tree structure
            tree = {}
            for process in processes:
                pid = process["pid"]
                ppid = process["ppid"]
                
                # Add to tree
                if pid not in tree:
                    tree[pid] = {"info": process, "children": []}
                else:
                    tree[pid]["info"] = process
                    
                # Add to parent's children
                if ppid in tree:
                    tree[ppid]["children"].append(pid)
                    
            return tree
            
        except Exception as e:
            self.logger.error(f"Error building process tree: {str(e)}")
            return {}
            
    def get_resource_usage(self, pid: int) -> Dict[str, Any]:
        """Get detailed resource usage for a process"""
        try:
            # Use ps for resource info
            cmd = ["ps", "-p", str(pid), "-o", "%cpu,%mem,rss,vsz,utime,stime"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_resource_usage(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting resource usage: {str(e)}")
            return {}
            
    def _parse_ps_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse ps command output"""
        processes = []
        lines = output.split("\n")
        
        if len(lines) < 2:  # Need at least header and one process
            return processes
            
        # Get header fields
        headers = lines[0].strip().lower().split()
        
        # Parse each process line
        for line in lines[1:]:
            if not line.strip():
                continue
                
            try:
                parts = line.strip().split(None, len(headers) - 1)
                if len(parts) >= len(headers):
                    process = {}
                    for i, header in enumerate(headers):
                        value = parts[i]
                        # Convert numeric values
                        if header in ["pid", "ppid"]:
                            process[header] = int(value)
                        elif header in ["%cpu", "%mem"]:
                            process[header] = float(value)
                        else:
                            process[header] = value
                    processes.append(process)
            except Exception as e:
                self.logger.error(f"Error parsing process line: {str(e)}")
                continue
                
        return processes
        
    def _get_open_files(self, pid: int) -> List[str]:
        """Get open files for a process"""
        try:
            cmd = ["lsof", "-p", str(pid), "-F", "n"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            files = []
            for line in proc.stdout.split("\n"):
                if line.startswith("n"):  # File name
                    files.append(line[1:])  # Remove 'n' prefix
                    
            return files
            
        except Exception as e:
            self.logger.error(f"Error getting open files: {str(e)}")
            return []
            
    def _get_network_ports(self, pid: int) -> List[Dict[str, Any]]:
        """Get network ports used by process"""
        try:
            cmd = ["lsof", "-i", "-a", "-p", str(pid), "-n", "-P"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            ports = []
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    try:
                        parts = line.split()
                        if len(parts) >= 9:
                            port = {
                                "protocol": parts[4],
                                "address": parts[8],
                                "state": parts[9] if len(parts) > 9 else None
                            }
                            ports.append(port)
                    except Exception as e:
                        self.logger.error(f"Error parsing port line: {str(e)}")
                        continue
                        
            return ports
            
        except Exception as e:
            self.logger.error(f"Error getting network ports: {str(e)}")
            return []
            
    def _get_environment(self, pid: int) -> Dict[str, str]:
        """Get environment variables for process"""
        try:
            cmd = ["ps", "eww", "-p", str(pid)]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            env = {}
            for line in proc.stdout.split("\n")[1:]:  # Skip header
                if "=" in line:
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip()
                    
            return env
            
        except Exception as e:
            self.logger.error(f"Error getting environment: {str(e)}")
            return {}
            
    def _parse_resource_usage(self, output: str) -> Dict[str, Any]:
        """Parse resource usage output"""
        usage = {}
        lines = output.split("\n")
        
        if len(lines) < 2:  # Need header and values
            return usage
            
        try:
            # Get header fields
            headers = lines[0].strip().lower().split()
            values = lines[1].strip().split()
            
            if len(headers) == len(values):
                for i, header in enumerate(headers):
                    try:
                        # Convert values to appropriate types
                        if header in ["%cpu", "%mem"]:
                            usage[header] = float(values[i])
                        elif header in ["rss", "vsz"]:
                            usage[header] = int(values[i])
                        else:
                            usage[header] = values[i]
                    except ValueError:
                        usage[header] = values[i]
                        
        except Exception as e:
            self.logger.error(f"Error parsing resource usage: {str(e)}")
            
        return usage
``` """
Hardware monitoring module
"""

import logging
import subprocess
import json
from typing import Optional, Dict, Any, List
from pathlib import Path

class HardwareMonitor:
    """Monitor system hardware"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_system_info(self) -> Dict[str, Any]:
        """Get system hardware information"""
        try:
            # Use system_profiler for hardware info
            cmd = ["system_profiler", "SPHardwareDataType", "-json"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return json.loads(proc.stdout)["SPHardwareDataType"][0]
            
        except Exception as e:
            self.logger.error(f"Error getting system info: {str(e)}")
            return {}
            
    def get_temperature(self) -> Dict[str, float]:
        """Get temperature sensors data"""
        try:
            # Use osx-cpu-temp for temperature
            cmd = ["osx-cpu-temp", "-j"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return json.loads(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting temperature: {str(e)}")
            return {}
            
    def get_power_info(self) -> Dict[str, Any]:
        """Get power and battery information"""
        try:
            # Use system_profiler for power info
            cmd = ["system_profiler", "SPPowerDataType", "-json"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return json.loads(proc.stdout)["SPPowerDataType"][0]
            
        except Exception as e:
            self.logger.error(f"Error getting power info: {str(e)}")
            return {}
            
    def get_disk_info(self) -> List[Dict[str, Any]]:
        """Get disk and storage information"""
        try:
            # Use diskutil for disk info
            cmd = ["diskutil", "list", "-plist"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            disks = []
            plist = self._parse_plist(proc.stdout)
            
            # Get detailed info for each disk
            for disk in plist.get("AllDisksAndPartitions", []):
                disk_info = self._get_disk_details(disk["DeviceIdentifier"])
                if disk_info:
                    disks.append(disk_info)
                    
            return disks
            
        except Exception as e:
            self.logger.error(f"Error getting disk info: {str(e)}")
            return []
            
    def get_memory_pressure(self) -> Dict[str, Any]:
        """Get memory pressure statistics"""
        try:
            # Use memory_pressure command
            cmd = ["memory_pressure"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_memory_pressure(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting memory pressure: {str(e)}")
            return {}
            
    def _get_disk_details(self, disk_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific disk"""
        try:
            # Use diskutil info for detailed disk info
            cmd = ["diskutil", "info", "-plist", disk_id]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_plist(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting disk details: {str(e)}")
            return None
            
    def _parse_plist(self, plist_str: str) -> Dict[str, Any]:
        """Parse property list output"""
        try:
            # Convert plist to JSON format
            cmd = ["plutil", "-convert", "json", "-o", "-", "-"]
            
            proc = subprocess.run(
                cmd,
                input=plist_str.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if proc.returncode != 0:
                return {}
                
            return json.loads(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error parsing plist: {str(e)}")
            return {}
            
    def _parse_memory_pressure(self, output: str) -> Dict[str, Any]:
        """Parse memory_pressure command output"""
        pressure = {
            "system": {},
            "levels": {}
        }
        
        current_section = None
        
        for line in output.split("\n"):
            line = line.strip()
            
            if not line:
                continue
                
            # Detect sections
            if "System-wide memory pressure:" in line:
                current_section = "system"
                continue
            elif "Memory pressure level:" in line:
                current_section = "levels"
                continue
                
            # Parse values
            if current_section and ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                
                # Try to convert percentages
                if "%" in value:
                    try:
                        value = float(value.replace("%", ""))
                    except ValueError:
                        pass
                        
                if current_section == "system":
                    pressure["system"][key] = value
                else:
                    pressure["levels"][key] = value
                    
        return pressure """
File change detection module
Handles real-time file system change monitoring
"""

import logging
import os
import time
from typing import Optional, Dict, Any, List, Set, Callable
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler, FileSystemEvent

class ChangeMonitor:
    """Monitor file system changes in real-time"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.observer = Observer()
        self.handlers = {}
        self.started = False
        
    def start_monitoring(self) -> None:
        """Start the file system monitor"""
        if not self.started:
            self.observer.start()
            self.started = True
            
    def stop_monitoring(self) -> None:
        """Stop the file system monitor"""
        if self.started:
            self.observer.stop()
            self.observer.join()
            self.started = False
            
    def watch_directory(self,
                       path: str,
                       recursive: bool = True,
                       patterns: Optional[List[str]] = None,
                       ignore_patterns: Optional[List[str]] = None,
                       callback: Optional[Callable[[FileSystemEvent], None]] = None
                       ) -> None:
        """Watch a directory for changes"""
        try:
            path_obj = Path(path)
            if not path_obj.is_dir():
                raise ValueError(f"Not a directory: {path}")
                
            # Create event handler
            handler = FileChangeHandler(
                patterns=patterns,
                ignore_patterns=ignore_patterns,
                callback=callback,
                logger=self.logger
            )
            
            # Schedule directory watching
            self.observer.schedule(
                handler,
                str(path_obj),
                recursive=recursive
            )
            
            # Store handler reference
            self.handlers[str(path_obj)] = handler
            
            if not self.started:
                self.start_monitoring()
                
        except Exception as e:
            self.logger.error(f"Error watching directory: {str(e)}")
            
    def unwatch_directory(self, path: str) -> None:
        """Stop watching a directory"""
        try:
            path_obj = Path(path)
            
            # Remove handler
            if str(path_obj) in self.handlers:
                handler = self.handlers[str(path_obj)]
                self.observer.unschedule(handler)
                del self.handlers[str(path_obj)]
                
        except Exception as e:
            self.logger.error(f"Error unwatching directory: {str(e)}")
            
    def get_recent_changes(self, path: str, minutes: int = 60) -> List[Dict[str, Any]]:
        """Get recent changes in a directory"""
        try:
            path_obj = Path(path)
            if not path_obj.is_dir():
                raise ValueError(f"Not a directory: {path}")
                
            changes = []
            cutoff_time = time.time() - (minutes * 60)
            
            # Walk directory
            for root, dirs, files in os.walk(str(path_obj)):
                for name in files + dirs:
                    try:
                        file_path = Path(root) / name
                        stat_result = file_path.stat()
                        
                        # Check if modified within time window
                        if stat_result.st_mtime >= cutoff_time:
                            changes.append({
                                "path": str(file_path),
                                "type": "directory" if file_path.is_dir() else "file",
                                "modified": datetime.fromtimestamp(stat_result.st_mtime),
                                "size": stat_result.st_size if file_path.is_file() else None
                            })
                    except Exception as e:
                        self.logger.error(f"Error processing {file_path}: {str(e)}")
                        continue
                        
            return sorted(changes, key=lambda x: x["modified"], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error getting recent changes: {str(e)}")
            return []
            
class FileChangeHandler(FileSystemEventHandler):
    """Handle file system change events"""
    
    def __init__(self,
                 patterns: Optional[List[str]] = None,
                 ignore_patterns: Optional[List[str]] = None,
                 callback: Optional[Callable[[FileSystemEvent], None]] = None,
                 logger: Optional[logging.Logger] = None):
        super().__init__()
        self.patterns = patterns
        self.ignore_patterns = ignore_patterns
        self.callback = callback
        self.logger = logger or logging.getLogger(__name__)
        
    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file/directory creation"""
        try:
            if self._should_handle_event(event):
                self.logger.info(f"Created: {event.src_path}")
                if self.callback:
                    self.callback(event)
        except Exception as e:
            self.logger.error(f"Error handling creation event: {str(e)}")
            
    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file/directory modification"""
        try:
            if self._should_handle_event(event):
                self.logger.info(f"Modified: {event.src_path}")
                if self.callback:
                    self.callback(event)
        except Exception as e:
            self.logger.error(f"Error handling modification event: {str(e)}")
            
    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file/directory deletion"""
        try:
            if self._should_handle_event(event):
                self.logger.info(f"Deleted: {event.src_path}")
                if self.callback:
                    self.callback(event)
        except Exception as e:
            self.logger.error(f"Error handling deletion event: {str(e)}")
            
    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file/directory move/rename"""
        try:
            if self._should_handle_event(event):
                self.logger.info(f"Moved/Renamed: {event.src_path} -> {event.dest_path}")
                if self.callback:
                    self.callback(event)
        except Exception as e:
            self.logger.error(f"Error handling move event: {str(e)}")
            
    def _should_handle_event(self, event: FileSystemEvent) -> bool:
        """Check if event should be handled based on patterns"""
        try:
            # Always handle directory events
            if event.is_directory:
                return True
                
            # Check ignore patterns
            if self.ignore_patterns:
                for pattern in self.ignore_patterns:
                    if Path(event.src_path).match(pattern):
                        return False
                        
            # Check include patterns
            if self.patterns:
                for pattern in self.patterns:
                    if Path(event.src_path).match(pattern):
                        return True
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking event patterns: {str(e)}")
            return False """
Files module
Provides file system monitoring and management capabilities
"""

from .integrity import IntegrityMonitor
from .permissions import PermissionsMonitor
from .changes import ChangeMonitor
from .storage import StorageMonitor

__all__ = [
    'IntegrityMonitor',
    'PermissionsMonitor',
    'ChangeMonitor',
    'StorageMonitor'
]
"""
Storage monitoring module
Handles disk and volume monitoring
"""

import logging
import subprocess
import json
from typing import Optional, Dict, Any, List
from pathlib import Path

class StorageMonitor:
    """Monitor disk and volume storage"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_volumes(self) -> List[Dict[str, Any]]:
        """Get list of mounted volumes"""
        try:
            # Use diskutil list for volume info
            cmd = ["diskutil", "list", "-plist"]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"diskutil failed: {proc.stderr}")
                
            # Parse plist output
            volumes = []
            plist = self._parse_plist(proc.stdout)
            
            # Get detailed info for each disk
            for disk in plist.get("AllDisksAndPartitions", []):
                disk_info = self._get_disk_info(disk["DeviceIdentifier"])
                if disk_info:
                    volumes.append(disk_info)
                    
            return volumes
            
        except Exception as e:
            self.logger.error(f"Error getting volumes: {str(e)}")
            return []
            
    def get_volume_info(self, volume: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a volume"""
        try:
            # Use diskutil info for volume info
            cmd = ["diskutil", "info", "-plist", volume]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"diskutil failed: {proc.stderr}")
                
            return self._parse_plist(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting volume info: {str(e)}")
            return None
            
    def get_storage_usage(self, path: str = "/") -> Dict[str, Any]:
        """Get storage usage information"""
        try:
            # Use df for storage info
            cmd = ["df", "-h", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"df failed: {proc.stderr}")
                
            return self._parse_df_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting storage usage: {str(e)}")
            return {}
            
    def get_directory_size(self, path: str) -> Dict[str, Any]:
        """Get directory size information"""
        try:
            # Use du for directory size
            cmd = ["du", "-sh", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"du failed: {proc.stderr}")
                
            return self._parse_du_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting directory size: {str(e)}")
            return {}
            
    def get_volume_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all volumes"""
        try:
            stats = {}
            
            # Get list of volumes
            volumes = self.get_volumes()
            
            # Get stats for each volume
            for volume in volumes:
                identifier = volume.get("DeviceIdentifier")
                if identifier:
                    mount_point = volume.get("MountPoint")
                    if mount_point:
                        stats[identifier] = {
                            "info": volume,
                            "usage": self.get_storage_usage(mount_point)
                        }
                        
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting volume stats: {str(e)}")
            return {}
            
    def _get_disk_info(self, disk_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed disk information"""
        try:
            cmd = ["diskutil", "info", "-plist", disk_id]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                return None
                
            return self._parse_plist(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting disk info: {str(e)}")
            return None
            
    def _parse_plist(self, plist_str: str) -> Dict[str, Any]:
        """Parse property list output"""
        try:
            # Convert plist to JSON
            cmd = ["plutil", "-convert", "json", "-o", "-", "-"]
            
            proc = subprocess.run(
                cmd,
                input=plist_str.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if proc.returncode != 0:
                raise Exception(f"plutil failed: {proc.stderr.decode()}")
                
            return json.loads(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error parsing plist: {str(e)}")
            return {}
            
    def _parse_df_output(self, output: str) -> Dict[str, Any]:
        """Parse df command output"""
        try:
            lines = output.strip().split("\n")
            if len(lines) < 2:
                return {}
                
            # Parse header
            headers = lines[0].lower().split()
            
            # Parse values
            values = lines[1].split()
            
            if len(headers) == len(values):
                return dict(zip(headers, values))
                
            return {}
            
        except Exception as e:
            self.logger.error(f"Error parsing df output: {str(e)}")
            return {}
            
    def _parse_du_output(self, output: str) -> Dict[str, Any]:
        """Parse du command output"""
        try:
            parts = output.strip().split()
            if len(parts) >= 2:
                return {
                    "size": parts[0],
                    "path": parts[1]
                }
                
            return {}
            
        except Exception as e:
            self.logger.error(f"Error parsing du output: {str(e)}")
            return {} """
File permissions monitoring module
Handles file permission monitoring and management
"""

import logging
import os
import stat
import pwd
import grp
import subprocess
from typing import Optional, Dict, Any, List, Set
from pathlib import Path

class PermissionsMonitor:
    """Monitor and manage file permissions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_permissions(self, path: str) -> Dict[str, Any]:
        """Get detailed permissions information"""
        try:
            path_obj = Path(path)
            stat_result = path_obj.stat()
            
            # Get owner and group names
            try:
                owner = pwd.getpwuid(stat_result.st_uid).pw_name
            except KeyError:
                owner = str(stat_result.st_uid)
                
            try:
                group = grp.getgrgid(stat_result.st_gid).gr_name
            except KeyError:
                group = str(stat_result.st_gid)
                
            return {
                "mode": stat_result.st_mode,
                "mode_string": stat.filemode(stat_result.st_mode),
                "owner": owner,
                "group": group,
                "owner_id": stat_result.st_uid,
                "group_id": stat_result.st_gid,
                "permissions": {
                    "user": {
                        "read": bool(stat_result.st_mode & stat.S_IRUSR),
                        "write": bool(stat_result.st_mode & stat.S_IWUSR),
                        "execute": bool(stat_result.st_mode & stat.S_IXUSR)
                    },
                    "group": {
                        "read": bool(stat_result.st_mode & stat.S_IRGRP),
                        "write": bool(stat_result.st_mode & stat.S_IWGRP),
                        "execute": bool(stat_result.st_mode & stat.S_IXGRP)
                    },
                    "other": {
                        "read": bool(stat_result.st_mode & stat.S_IROTH),
                        "write": bool(stat_result.st_mode & stat.S_IWOTH),
                        "execute": bool(stat_result.st_mode & stat.S_IXOTH)
                    }
                },
                "special": {
                    "setuid": bool(stat_result.st_mode & stat.S_ISUID),
                    "setgid": bool(stat_result.st_mode & stat.S_ISGID),
                    "sticky": bool(stat_result.st_mode & stat.S_ISVTX)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting permissions: {str(e)}")
            return {}
            
    def get_acl(self, path: str) -> List[Dict[str, Any]]:
        """Get Access Control List entries"""
        try:
            cmd = ["ls", "-le", path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if proc.returncode != 0:
                raise Exception(f"ls failed: {proc.stderr}")
                
            return self._parse_acl_output(proc.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting ACL: {str(e)}")
            return []
            
    def check_access(self, path: str, user: Optional[str] = None) -> Dict[str, bool]:
        """Check access permissions for current or specified user"""
        try:
            if user:
                # Get user info
                try:
                    user_info = pwd.getpwnam(user)
                    uid = user_info.pw_uid
                    groups = [g.gr_gid for g in grp.getgrall() if user in g.gr_mem]
                    groups.append(user_info.pw_gid)
                except KeyError:
                    raise ValueError(f"User not found: {user}")
            else:
                # Current process user
                uid = os.getuid()
                groups = os.getgroups()
                
            path_obj = Path(path)
            stat_result = path_obj.stat()
            
            # Check if user is owner
            is_owner = stat_result.st_uid == uid
            # Check if user is in group
            in_group = stat_result.st_gid in groups
            
            mode = stat_result.st_mode
            
            return {
                "exists": True,
                "read": (
                    (is_owner and bool(mode & stat.S_IRUSR)) or
                    (in_group and bool(mode & stat.S_IRGRP)) or
                    bool(mode & stat.S_IROTH)
                ),
                "write": (
                    (is_owner and bool(mode & stat.S_IWUSR)) or
                    (in_group and bool(mode & stat.S_IWGRP)) or
                    bool(mode & stat.S_IWOTH)
                ),
                "execute": (
                    (is_owner and bool(mode & stat.S_IXUSR)) or
                    (in_group and bool(mode & stat.S_IXGRP)) or
                    bool(mode & stat.S_IXOTH)
                )
            }
            
        except FileNotFoundError:
            return {"exists": False, "read": False, "write": False, "execute": False}
        except Exception as e:
            self.logger.error(f"Error checking access: {str(e)}")
            return {"exists": True, "read": False, "write": False, "execute": False}
            
    def scan_directory_permissions(self, 
                                 directory: str,
                                 recursive: bool = True,
                                 check_patterns: Optional[List[Dict[str, Any]]] = None
                                 ) -> Dict[str, Any]:
        """Scan directory for permission issues"""
        results = {
            "scanned": 0,
            "issues": [],
            "errors": []
        }
        
        try:
            path_obj = Path(directory)
            if not path_obj.is_dir():
                raise ValueError(f"Not a directory: {directory}")
                
            # Get list of files
            if recursive:
                files = path_obj.rglob("*")
            else:
                files = path_obj.glob("*")
                
            # Process each file
            for file_path in files:
                try:
                    results["scanned"] += 1
                    perms = self.get_permissions(str(file_path))
                    
                    # Check against patterns if provided
                    if check_patterns:
                        for pattern in check_patterns:
                            if self._check_permission_pattern(perms, pattern):
                                results["issues"].append({
                                    "path": str(file_path),
                                    "permissions": perms,
                                    "pattern": pattern
                                })
                                
                except Exception as e:
                    results["errors"].append({
                        "path": str(file_path),
                        "error": str(e)
                    })
                    
        except Exception as e:
            self.logger.error(f"Error scanning directory permissions: {str(e)}")
            
        return results
        
    def _parse_acl_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse ACL command output"""
        entries = []
        
        try:
            lines = output.strip().split("\n")
            for line in lines:
                if line.startswith(" "):  # ACL entry
                    parts = line.strip().split(":")
                    if len(parts) >= 3:
                        entry = {
                            "type": parts[0],
                            "name": parts[1],
                            "permissions": parts[2]
                        }
                        entries.append(entry)
                        
        except Exception as e:
            self.logger.error(f"Error parsing ACL output: {str(e)}")
            
        return entries
        
    def _check_permission_pattern(self, perms: Dict[str, Any], pattern: Dict[str, Any]) -> bool:
        """Check if permissions match a pattern"""
        try:
            # Check each condition in pattern
            for key, value in pattern.items():
                if key == "min_mode":
                    if perms["mode"] & value != value:
                        return True
                elif key == "max_mode":
                    if perms["mode"] & ~value != 0:
                        return True
                elif key == "owner":
                    if perms["owner"] == value:
                        return True
                elif key == "group":
                    if perms["group"] == value:
                        return True
                elif key == "world_writable":
                    if value and perms["permissions"]["other"]["write"]:
                        return True
                elif key == "setuid":
                    if value and perms["special"]["setuid"]:
                        return True
                elif key == "setgid":
                    if value and perms["special"]["setgid"]:
                        return True
                        
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking permission pattern: {str(e)}")
            return False """
File integrity monitoring module
Handles file integrity checking and verification
"""

import logging
import hashlib
import os
import stat
from typing import Optional, Dict, Any, List, Set
from pathlib import Path
from datetime import datetime

class IntegrityMonitor:
    """Monitor file integrity and changes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def calculate_file_hash(self, path: str, algorithm: str = "sha256") -> Optional[str]:
        """Calculate file hash using specified algorithm"""
        try:
            hash_func = getattr(hashlib, algorithm)()
            path_obj = Path(path)
            
            if not path_obj.is_file():
                raise ValueError(f"Not a file: {path}")
                
            # Read file in chunks to handle large files
            with open(path_obj, "rb") as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)
                    
            return hash_func.hexdigest()
            
        except Exception as e:
            self.logger.error(f"Error calculating file hash: {str(e)}")
            return None
            
    def get_file_metadata(self, path: str) -> Dict[str, Any]:
        """Get file metadata including permissions and timestamps"""
        try:
            path_obj = Path(path)
            stat_result = path_obj.stat()
            
            return {
                "size": stat_result.st_size,
                "mode": stat_result.st_mode,
                "uid": stat_result.st_uid,
                "gid": stat_result.st_gid,
                "atime": datetime.fromtimestamp(stat_result.st_atime),
                "mtime": datetime.fromtimestamp(stat_result.st_mtime),
                "ctime": datetime.fromtimestamp(stat_result.st_ctime),
                "permissions": stat.filemode(stat_result.st_mode),
                "type": self._get_file_type(stat_result.st_mode)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting file metadata: {str(e)}")
            return {}
            
    def verify_signature(self, path: str, signature: str) -> bool:
        """Verify file signature"""
        try:
            calculated_hash = self.calculate_file_hash(path)
            return calculated_hash == signature
            
        except Exception as e:
            self.logger.error(f"Error verifying signature: {str(e)}")
            return False
            
    def scan_directory(self, directory: str, recursive: bool = True) -> Dict[str, Dict[str, Any]]:
        """Scan directory for file integrity information"""
        results = {}
        try:
            path_obj = Path(directory)
            if not path_obj.is_dir():
                raise ValueError(f"Not a directory: {directory}")
                
            # Get list of files
            if recursive:
                files = path_obj.rglob("*")
            else:
                files = path_obj.glob("*")
                
            # Process each file
            for file_path in files:
                if file_path.is_file():
                    try:
                        relative_path = str(file_path.relative_to(path_obj))
                        results[relative_path] = {
                            "hash": self.calculate_file_hash(str(file_path)),
                            "metadata": self.get_file_metadata(str(file_path))
                        }
                    except Exception as e:
                        self.logger.error(f"Error processing file {file_path}: {str(e)}")
                        continue
                        
        except Exception as e:
            self.logger.error(f"Error scanning directory: {str(e)}")
            
        return results
        
    def compare_snapshots(self, 
                         snapshot1: Dict[str, Dict[str, Any]], 
                         snapshot2: Dict[str, Dict[str, Any]]
                         ) -> Dict[str, List[str]]:
        """Compare two snapshots and return differences"""
        changes = {
            "added": [],
            "removed": [],
            "modified": [],
            "unchanged": []
        }
        
        try:
            # Get sets of files
            files1 = set(snapshot1.keys())
            files2 = set(snapshot2.keys())
            
            # Find added and removed files
            changes["added"] = list(files2 - files1)
            changes["removed"] = list(files1 - files2)
            
            # Check for modifications in common files
            common_files = files1 & files2
            for file in common_files:
                if snapshot1[file]["hash"] != snapshot2[file]["hash"]:
                    changes["modified"].append(file)
                else:
                    changes["unchanged"].append(file)
                    
        except Exception as e:
            self.logger.error(f"Error comparing snapshots: {str(e)}")
            
        return changes
        
    def monitor_critical_files(self, paths: List[str]) -> Dict[str, Dict[str, Any]]:
        """Monitor specific critical files"""
        results = {}
        
        try:
            for path in paths:
                path_obj = Path(path)
                if path_obj.exists():
                    results[path] = {
                        "hash": self.calculate_file_hash(path),
                        "metadata": self.get_file_metadata(path),
                        "exists": True
                    }
                else:
                    results[path] = {
                        "exists": False,
                        "error": "File not found"
                    }
                    
        except Exception as e:
            self.logger.error(f"Error monitoring critical files: {str(e)}")
            
        return results
        
    def _get_file_type(self, mode: int) -> str:
        """Determine file type from mode"""
        if stat.S_ISREG(mode):
            return "regular"
        elif stat.S_ISDIR(mode):
            return "directory"
        elif stat.S_ISLNK(mode):
            return "symlink"
        elif stat.S_ISFIFO(mode):
            return "fifo"
        elif stat.S_ISSOCK(mode):
            return "socket"
        elif stat.S_ISBLK(mode):
            return "block"
        elif stat.S_ISCHR(mode):
            return "character"
        else:
            return "unknown" %                                                  joshua@JZMBP domai-app % 

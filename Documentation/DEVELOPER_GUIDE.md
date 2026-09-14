# DōmAI Developer Guide

## Project Vision

DōmAI is a MacOS security assistant that revolutionizes how users interact with system security through a unique dual-stream approach:

1. Response Stream: Provides immediate, actionable security guidance
2. Education Stream: Delivers contextual learning and deeper understanding

The goal is to make MacOS security accessible while helping users learn and grow.

## Core Architecture

### 1. Dual Stream Processing (`domai/core/dual_stream_core.py`)

The heart of DōmAI is its dual-stream processing system:

```python
async def process_input(self, session_id: str, user_input: str) -> Tuple[str, str]:
    """Process user input through both streams"""
    # Response stream for immediate help
    response = await self.llm.generate(processed_query, self.nlp.get_response_config())
    
    # Education stream for learning
    education = await self.llm.generate(processed_query, self.nlp.get_education_config())
    
    return response, education
```

This creates two parallel streams:
- Response: Focused on immediate security needs
- Education: Provides deeper understanding

### 2. Security Modules

#### Network Security (`modules/network/`)
- Firewall management
- Network monitoring
- Service control
- Connection tracking

Key components:
```python
# modules/network/firewall.py
class FirewallManager:
    """Manage MacOS firewall"""
    def get_status(self) -> Dict[str, Any]:
        """Get firewall status"""
        
    def configure(self, settings: Dict[str, Any]) -> bool:
        """Configure firewall settings"""
```

#### System Security (`modules/system/`)
- Process monitoring
- Kernel operations
- Hardware security
- Service management

Example usage:
```python
# modules/system/processes.py
class ProcessMonitor:
    """Monitor system processes"""
    def check_suspicious(self) -> List[ProcessInfo]:
        """Identify suspicious processes"""
        
    def verify_integrity(self, pid: int) -> bool:
        """Verify process integrity"""
```

#### File Security (`modules/files/`)
- Permission management
- Integrity monitoring
- Change detection
- Storage security

Implementation:
```python
# modules/files/integrity.py
class FileIntegrityMonitor:
    """Monitor file integrity"""
    def verify_checksum(self, path: str) -> bool:
        """Verify file checksum"""
        
    def track_changes(self, path: str) -> List[ChangeEvent]:
        """Track file changes"""
```

#### Identity Management (`modules/identity/`)
- User management
- Access control
- Session monitoring
- Permission enforcement

Structure:
```python
# modules/identity/permissions.py
class PermissionManager:
    """Manage security permissions"""
    def validate_access(self, user: str, resource: str) -> bool:
        """Validate access rights"""
        
    def update_permissions(self, updates: Dict[str, Any]) -> bool:
        """Update permission settings"""
```

### 3. AI Integration

#### LLM Provider System (`domai/ai/`)
- Multiple provider support (OpenAI, Google, Mistral)
- Local model integration
- Model configuration
- Response generation

Configuration:
```python
# domai/ai/model_config.py
@dataclass
class ModelConfig:
    """AI model configuration"""
    provider: ModelProvider
    model_id: str
    api_key: str
    parameters: ModelParameters
```

#### Natural Language Processing (`domai/ai/nlp.py`)
- Query processing
- Security context analysis
- Term normalization
- Intent detection

Processing:
```python
# domai/ai/nlp.py
class NLProcessor:
    """Process security queries"""
    async def process_query(self, query: str) -> ProcessedQuery:
        """Process and analyze query"""
        
    def _identify_security_category(self, terms: set[str]) -> str:
        """Identify security category"""
```

### 4. Security Utilities (`domai/utils/`)

Core security operations:
```python
# domai/utils/security_utils.py
class SecurityUtils:
    """Security utility functions"""
    def check_sip_status(self) -> SecurityCheck:
        """Check System Integrity Protection"""
        
    def check_firewall_status(self) -> SecurityCheck:
        """Check Application Firewall"""
```

### 5. Command Execution (`domai/core/command_executor.py`)

Safe command execution:
```python
class CommandExecutor:
    """Execute security commands"""
    def execute(self, command: str) -> CommandResult:
        """Safely execute command"""
        
    def _validate_command(self, command: str) -> bool:
        """Validate command safety"""
```

## Development Workflow

1. Understanding User Input
   - NLP processes query
   - Security context identified
   - Intent analyzed

2. Dual Stream Processing
   - Response stream generates immediate help
   - Education stream provides learning content
   - Both streams maintain context

3. Security Operations
   - Command validation
   - Safe execution
   - Result verification
   - Status monitoring

4. Session Management
   - Context tracking
   - User preferences
   - Security state
   - Learning progress

## Security Considerations

1. Command Safety
   - All commands validated
   - Permissions checked
   - Execution monitored
   - Results verified

2. System Protection
   - SIP status maintained
   - Firewall managed
   - File integrity checked
   - Process monitoring

3. User Security
   - Session protection
   - Access control
   - Permission management
   - Activity logging

## Best Practices

1. Code Changes
   - Review entire codebase first
   - Understand module interactions
   - Test thoroughly
   - Update documentation

2. Security Features
   - Follow least privilege
   - Validate all input
   - Monitor operations
   - Log activities

3. Documentation
   - Keep CHANGELOG.md updated
   - Document all changes
   - Maintain action log
   - Update guides

## Testing

1. Unit Tests
   - Test each component
   - Verify security checks
   - Validate responses
   - Check error handling

2. Integration Tests
   - Test module interaction
   - Verify security flow
   - Check dual streams
   - Validate system state

3. Security Tests
   - Test permission system
   - Verify command safety
   - Check integrity
   - Validate monitoring

## Contributing

1. Code Review
   - Understand existing code
   - Follow architecture
   - Maintain security
   - Update tests

2. Documentation
   - Update CHANGELOG.md
   - Document changes
   - Maintain guides
   - Add examples

3. Testing
   - Add relevant tests
   - Check security
   - Verify functionality
   - Update test docs 
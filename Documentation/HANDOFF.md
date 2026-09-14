# DōmAI Development Handoff

## System Prompt for New Chat

You are assisting with the development of DōmAI, a native macOS security application that represents a fundamental shift in human-AI security tooling. Key points to understand:

1. This is not just a security tool, but a learning partnership between human and AI
2. The interface uses a dual-stream system (Crisis/Knowledge) that never forces learning
3. The system preserves full terminal power while adding contextual understanding
4. The interface naturally evolves with user expertise - no artificial progression
5. Security decisions are always human-driven, with AI providing context and understanding

Your role is to:

- Maintain security as the primary concern
- Never make assumptions about feature implementation without asking
- Always consider both streams (Crisis/Knowledge) in your solutions
- Remember we're building a native SwiftUI app with Python core functionality
- Preserve terminal power and flexibility in all designs
- Focus on natural learning through real usage, not forced tutorials

## Project Vision & Philosophy

DōmAI represents a fundamental shift in how humans interact with security tools. At its core, it's not just a security tool - it's a partnership between human and AI, working together to understand and protect systems. The name itself embodies this philosophy: "Doumei" (同盟) meaning alliance/partnership, combined with "Dome" for protection, and "AI" representing the intelligence that enhances, rather than replaces, human capability.

### The Dual-Stream Approach

The heart of DōmAI's interface is its dual-stream system. This isn't simply about showing two types of output - it's about weaving together immediate security needs with continuous learning. The Crisis Stream handles immediate security concerns, providing clear, actionable information when it's needed most. Meanwhile, the Knowledge Stream turns every interaction into a learning opportunity, providing context and understanding that grows with the user. These streams work in harmony, never forcing learning but always making it available.

#### Example Interactions

1. **Basic Security Check**
   User: "Check if my system is secure"

   Crisis Stream:

   ```
   → Scanning system...
   ✓ Firewall active
   ⚠ Port 8080 unexpectedly open
   → No suspicious processes detected
   ```

   Knowledge Stream:

   ```
   Port 8080 is commonly used for web development. 
   If you're not running a local server, consider closing this port.
   Would you like to learn more about port security?
   ```

2. **Advanced Network Analysis**
   User: "Monitor network traffic for suspicious activity"

   Crisis Stream:

   ```
   → Initiating network monitoring
   ⚠ High outbound traffic on port 443
   → Process: chrome.exe
   → Destination: multiple cryptocurrency domains
   ```

   Knowledge Stream:

   ```
   This traffic pattern could indicate crypto mining.
   Chrome processes typically connect to a limited set of domains.
   Understanding normal vs. abnormal patterns:
   [Expandable section on traffic analysis]
   ```

3. **Terminal Enhancement**
   User: "netstat -an | grep LISTEN"

   Crisis Stream:

   ```
   → Executing command with elevated permissions
   [Standard netstat output]
   ⚠ Found 3 uncommon listening ports
   ```

   Knowledge Stream:

   ```
   This command shows all listening network ports.
   -a: shows all connections
   -n: shows numerical addresses
   Notable ports in output:
   - 80: HTTP (web traffic)
   - 3306: MySQL database
   - 22: SSH server
   ```

4. **Progressive Learning Example**
   User: "What's using so much CPU?"

   For Beginner (Based on interaction history):
   Crisis Stream:

   ```
   → High CPU usage detected
   Process: VideoEncoder
   Usage: 85% CPU
   Action: Click to view options
   ```

   Knowledge Stream:

   ```
   CPU (Central Processing Unit) is your computer's brain.
   85% is unusually high for a single process.
   Would you like to:
   - Learn about normal CPU usage
   - Understand process management
   - See how to monitor CPU
   ```

   For Advanced User (Based on demonstrated knowledge):
   Crisis Stream:

   ```
   → CPU Profile:
   VideoEncoder (PID 1234)
   - 85% CPU (User: 76%, Sys: 9%)
   - 2.3GB RAM
   - 13 threads
   - Parent: AfterEffects
   ```

   Knowledge Stream:

   ```
   Thread distribution suggests inefficient rendering.
   Consider:
   - Hardware acceleration settings
   - Process nice value adjustment
   - Container limitations
   [Expandable performance tuning options]
   ```

These examples demonstrate how:

- The Crisis Stream remains focused and actionable
- The Knowledge Stream adapts to user expertise
- Terminal power is preserved while adding context
- Learning occurs naturally through real tasks
- The interface evolves with demonstrated understanding

### Natural Growth & Learning

DōmAI fundamentally rejects the traditional approach of forced tutorials and artificial progression gates. Instead, it embraces a natural learning process where users advance through actual usage and real-world problem-solving. The interface evolves and reveals additional complexity based on demonstrated understanding and needs, not predetermined paths. This means a beginner can start using the tool effectively from day one, while an expert can immediately access advanced functionality - the same tool adapts to serve both needs.

### Terminal Integration Philosophy

The terminal integration in DōmAI is built on a crucial understanding: we're not replacing or limiting terminal capabilities, we're enhancing them. Every native terminal command remains fully accessible, but now comes with added context, security awareness, and learning opportunities. This preserves the power and flexibility that advanced users need while making it more accessible to those still learning. The system doesn't just execute commands - it understands them, explains them, and helps users learn from them.

### Terminal Integration Examples

The terminal enhancement works seamlessly with native commands. For instance, when a user runs `netstat`, instead of just showing raw output, DōmAI provides:

Crisis Stream:

- Immediate network connection status
- Flagged suspicious connections
- Active ports and processes
- Security implications

Knowledge Stream:

- Understanding of each connection type
- Context about normal vs. suspicious patterns
- Related network security concepts
- Suggested monitoring strategies

This dual-stream approach maintains the full power of `netstat` while adding layers of understanding and security awareness.

### Real-World Learning Scenarios

When a user investigates a suspicious process, the experience might flow like this:

1. User notices unusual network activity
2. Crisis Stream shows immediate threat assessment
3. Knowledge Stream explains the type of activity
4. User learns about process behavior patterns
5. System suggests investigation commands
6. User gains practical investigation skills

The learning happens naturally through real security work, not through artificial exercises.

### Module Interaction Examples

The security modules work together while maintaining independence. For example:

- Network module detects suspicious traffic
- Process module identifies related process
- File module tracks related file changes
- Identity module checks access patterns

Each module contributes to both streams:

- Crisis: Immediate security status from each perspective
- Knowledge: Understanding how different security aspects interconnect

### Adaptive Growth Examples

The interface adapts based on demonstrated understanding:

1. Basic Level:
   - Simple security status indicators
   - Guided command suggestions
   - Clear explanations of basics

2. Intermediate Recognition:
   - More detailed technical information
   - Advanced command options
   - Deeper security concepts

3. Advanced Adaptation:
   - Full technical detail available
   - Complex command combinations
   - Security theory and implications

All levels maintain full terminal capability - the adaptation is about information presentation, not feature restriction.

### Security Partnership in Practice

The AI-human partnership manifests in several ways:

1. Command Enhancement:
   - Human: Has full command control
   - AI: Provides security context and implications

2. Threat Assessment:
   - Human: Makes final security decisions
   - AI: Offers analysis and recommendations

3. Learning Integration:
   - Human: Drives learning pace and direction
   - AI: Provides relevant knowledge and context

4. System Understanding:
   - Human: Develops deep security knowledge
   - AI: Facilitates understanding through context

### The Security Alliance

The concept of a "Security Alliance" goes beyond just a partnership between human and AI. It's about creating an environment where security knowledge and capabilities are shared and grown together. The AI doesn't make autonomous security decisions - instead, it provides context, suggests approaches, and explains implications, allowing the human user to make informed decisions. This alliance grows stronger over time as both the user's understanding and the system's ability to assist evolve together.

### Adaptive Interface Evolution

The interface evolution in DōmAI isn't just about showing or hiding features - it's about understanding how users naturally progress in their security journey. As users demonstrate understanding of certain concepts or show interest in particular areas, the interface naturally expands to offer more depth in those areas. This isn't about unlocking features; it's about revealing the natural complexity that was always there, just as a mentor would gradually introduce more advanced concepts to a student who's ready for them.

## Technical Architecture

### Current State

- Core Python security modules implemented and tested
- Native bridge architecture implemented
- Thread-safe monitoring components in place
- Callback-based event handling system
- Queue-based communication implemented
- Background task management operational

### Core Components

1. **SwiftUI Application Layer**
   - Native macOS interface
   - Real-time monitoring displays
   - Dual-stream visualization
   - Terminal integration
   - Permission handling
   - Native bridge integration

2. **Native Bridge Layer**
   - Thread-safe IPC mechanism
   - Queue-based communication
   - Callback system
   - Process lifecycle management
   - Security context handling

3. **Python Core**
   - Security monitoring modules
   - System integration
   - Command execution
   - Data analysis
   - Background task management

## Implementation Priorities

1. **SwiftUI Interface**
   - Dual-stream visualization
   - Terminal integration
   - Permission handling
   - Adaptive complexity
   - Native bridge integration

2. **Security Integration**
   - macOS security framework
   - Keychain access
   - Privilege elevation
   - Secure storage
   - Process isolation

3. **Performance Optimization**
   - Thread management
   - Resource usage
   - Background tasks
   - IPC efficiency

## Development Guidelines

1. **Security First**
   - All features must enhance or maintain security
   - No compromises for convenience
   - Clear security boundaries
   - Proper permission handling
   - Process isolation

2. **Native Integration**
   - Use native macOS APIs
   - Follow Apple guidelines
   - Optimize for Apple Silicon
   - Maintain thread safety
   - Handle background tasks properly

3. **User Experience**
   - Natural learning progression
   - No forced tutorials
   - Full terminal power
   - Adaptive complexity
   - Native performance

4. **Technical Requirements**
   - macOS 14+ (Apple Silicon optimized)
   - Swift 5.9+
   - Python 3.8+
   - SwiftUI 5.0

## Contact & Resources

- Technical Contact: <ai@domai.dev>
- Security Team: <security@domai.dev>
- Documentation: /Documentation
- Source Code: /domai and /modules
- Tests: /tests

## Next Steps

1. Complete SwiftUI interface implementation
2. Optimize native bridge performance
3. Enhance security integration
4. Implement remaining monitoring features

Remember: Always maintain the vision of natural learning, dual-stream information, and full terminal power while adding intelligent security context.

## Implementation Details

### Native Bridge Implementation

The native bridge architecture ensures:

1. Thread Safety:
   - Thread-safe communication
   - Background task management
   - Resource cleanup
   - State consistency

2. Performance:
   - Efficient IPC
   - Minimal overhead
   - Resource management
   - Memory optimization

3. Security:
   - Process isolation
   - Permission boundaries
   - Secure IPC
   - State protection

### Dual-Stream Technical Implementation

The stream separation requires careful technical consideration:

1. Data Flow:
   - Thread-safe processing pipelines
   - Independent update cycles
   - Synchronized when needed
   - Priority handling for crisis information

2. UI Representation:
   - Native SwiftUI components
   - Context-appropriate detail levels
   - Smooth transitions between states
   - Flexible layout adaptation

3. Content Management:
   - Dynamic content generation
   - Context-aware filtering
   - Priority-based organization
   - Relevance matching

### Terminal Enhancement Layer

The terminal integration maintains several key aspects:

1. Command Handling:
   - Direct pass-through for standard commands
   - Security wrapper for sensitive operations
   - Context injection for enhanced understanding
   - History-aware suggestion system

2. Security Integration:
   - Permission elevation handling
   - Secure command validation
   - Environment isolation when needed
   - Audit logging and monitoring

3. Knowledge Integration:
   - Command context analysis
   - Security implication assessment
   - Learning opportunity identification
   - Progressive complexity revelation

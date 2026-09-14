> **Archived (September 2026).** This repository is a sanitized copy of the 2024 Python-era DōmAI prototype (`domai-app`), kept read-only as design history. It is not runnable as-is and is not developed further.
>
> **Active development is in [joshzdev/domai](https://github.com/joshzdev/domai)**, the native Swift/SwiftUI macOS app. Start with its [Product Specification](https://github.com/joshzdev/domai/blob/main/Documentation/PRODUCT_SPEC.md).

# DōmAI - MacOS Security Assistant

DōmAI is an AI-powered security assistant for MacOS that provides interactive guidance and education about system security. It helps users understand and manage their MacOS security settings through natural language interaction.

## Vision

DōmAI combines three powerful elements:

- **Doumei (同盟)**: Alliance
- **Dome**: Protective shield for your system's security
- **AI**: AI security assistance

Our mission is to unify and simplify Mac security & maintenance through natural language interaction and adaptive learning.

The best part? The app grows with the user, adapting based on lessons learnt.

[Read our complete vision →](Documentation/VISION.md)

## Features

- **Interactive Security Guidance**: Get clear, actionable advice about MacOS security in plain language
- **Educational Content**: Learn about security concepts and best practices while solving problems
- **Security Assessment**: Check the status of key security features like SIP, Firewall, FileVault, and Gatekeeper
- **Safe Command Execution**: Execute security-related commands with validation and safety checks
- **Multiple AI Providers**: Support for OpenAI, Google (Gemini), and Mistral AI models
- **Flexible Configuration**: Customize technical level and notification preferences

## Installation

### Prerequisites

- MacOS 10.15 (Catalina) or later
- Python 3.8 or later
- pip (Python package installer)

### Install from PyPI

```bash
pip install domai
```

### Install from Source

```bash
git clone https://github.com/joshua/domai-app.git
cd domai-app
pip install -e .
```

## Configuration

1. Create a configuration file at `~/.domai/config.json`:

```json
{
    "api_keys": {
        "openai": "your-openai-key",
        "google": "your-google-key",
        "mistral": "your-mistral-key"
    }
}
```

Or set environment variables:

```bash
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_API_KEY="your-google-key"
export MISTRAL_API_KEY="your-mistral-key"
```

## Usage

### Interactive Mode

Start an interactive session:

```bash
domai interactive
```

Options:
- `--config, -c`: Path to configuration file
- `--technical-level, -t`: Set technical level (beginner/intermediate/advanced)

### Execute Security Commands

Execute specific security commands:

```bash
domai execute "command"
```

Options:
- `--no-confirm`: Execute without confirmation
- `--config, -c`: Path to configuration file

### Security Assessment

Perform a security assessment:

```bash
domai assessment
```

## Security Features

DōmAI can help you manage:

- System Integrity Protection (SIP)
- Application Firewall
- FileVault Disk Encryption
- Gatekeeper and App Security
- File Permissions
- Security Recommendations

## Example Interactions

```
> How do I check if SIP is enabled?
Response: I'll check the System Integrity Protection status for you.
Command: csrutil status

> Is my firewall configured properly?
Response: Let me check your firewall configuration and provide recommendations.
[Displays firewall status and suggestions]

> Help me understand FileVault encryption
Response: Here's your current FileVault status.
Learn More: [Educational content about disk encryption]
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/joshua/domai-app.git
cd domai-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/MacOS
venv\Scripts\activate     # On Windows

# Install development dependencies
pip install -e "[dev]"
```

### Running Tests

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for GPT models
- Google for Gemini AI
- Mistral AI for their models
- The MacOS security community

## Support

For support, please:
1. Check the [Documentation](docs/)
2. Search [existing issues](https://github.com/joshua/domai-app/issues)
3. Create a new issue if needed

## Security

For security concerns, please email security@domai.ai or see our [Security Policy](SECURITY.md).

## Project Overview
- Name: DōmAI (Dōmei + Dome + AI)
- Website: domai.dev
- Support: humans@domai.dev
- Technical: ai@domai.dev
- Purpose: Unifying and simplifying Mac security & maintenance

## Current Mac Security Landscape

### Existing Tools & Fragmentation
1. System Information & Diagnostics
   - EtreCheck: System report generation
   - OnyX: System maintenance & configuration
   - Pareto Security: Basic security checks
   - KnockKnock: Launch item checker
   - BlockBlock: Installation monitor
   - XProCheck: Malware definitions
   - LockRattler: Security system checks
   - Silent Knight: Security update checks
   - DHS: Dylib vulnerabilities/hijack search
   - Signet: Signature verification
   - Taccy: Privacy permission checks
   - Murus: Packet firewall management
   - Apparency: File integrity
   - Lynis: System security audit
   - Zap (OWASP ZAP): vulnerabilities in webapps
   - Wireshark/TCPdump: Packet Sniffing
   - Rkhunter: Rootkit detector
   - Little Snitch: Network connections
   - Virustotal: Check IPs

2. Problems with Current Approach
   - Tools don't communicate with each other
   - Inconsistent interfaces
   - Overlapping functionality
   - Varying levels of maintenance
   - Different learning curves
   - No unified data view
   - CLI power hidden behind complexity
   - Time wasted on learning curve
   - Copying and Pasting between tools

### What CLI Can Actually Do
- Network monitoring (tcpdump, lsof, netstat)
- Process monitoring (ps, top, htop)
- System configuration (defaults, nvram)
- Security settings (spctl, csrutil)
- File system monitoring (fs_usage, opensnoop)
- Hardware diagnostics (system_profiler)
- Application management (codesign, xattr)

## DōmAI Solution

### Core Philosophy
- "One dome to protect it all. One AI to find them. One alliance to bring them and in quarantine, bind them."
- Unified interface for all security/maintenance tasks
- Progressive learning through use
- Power of CLI with accessibility of GUI
- Adaptive to user skill level

## Real Talk Section - Extended

### Why Everything's So Fragmented
1. Historical reasons:
   - Tools developed independently
   - Different developers solving specific problems
   - No standardization
   - Apple's changing security model

2. Technical reasons:
   - Different subsystems
   - Varying permission requirements
   - Complex integration needs
   - System update challenges

3. Market reasons:
   - Niche solutions
   - Different target users
   - Varying business models
   - Support limitations

### How We're Fixing This
1. Technical Integration:
   - Unified command framework
   - Consistent permission model
   - Centralized monitoring
   - Standardized data presentation

2. User Experience:
   - Single learning curve
   - Progressive feature revelation
   - Consistent interface
   - Contextual help

3. Security Approach:
   - Comprehensive protection
   - Intelligent monitoring
   - Proactive maintenance
   - Educational components

## Additional Technical Considerations

### CLI Integration
- Wrapper for complex commands
- Visual command builder
- Result interpretation
- Command learning system

### Permission Management
- Unified permission requests
- Clear purpose explanation
- Permission tracking
- Security impact awareness

### System Integration
- Kernel extension management
- System extension handling
- Network filter integration
- File system monitoring

## Final Thoughts
The Mac security/maintenance landscape is a mess of fragmented tools. Each one is powerful in its niche, but users shouldn't need 12 different apps to keep their system secure and maintained. DōmAI isn't just another tool - it's the unification and simplification of Mac system management.

Remember: The power of the command line with the accessibility of a modern interface, growing with the user's needs and abilities.

---
*Note: This document combines technical specifications, market analysis, and opinionated views on the current state of Mac security tools and our solution to their fragmentation.*

## Practicability Analysis

### Why Language Precision Matters
When building security tools, the difference between "practical" and "practicable" isn't just semantic - it's the difference between "yeah, we could do that" and "yes, this will actually work in the real world."

### Real-World Implementability Assessment

#### What's Actually Practicable Now
1. User Interface & Education
   - Adaptive learning ✓
   - Multi-level documentation ✓
   - Achievement system ✓
   WHY: Direct user interaction, no deep system access needed

2. Basic Security Features
   - System monitoring ✓
   - Basic firewall management ✓
   - Update checking ✓
   WHY: Uses existing APIs, proven implementation paths

3. CLI Wrapping
   - Basic command simplification ✓
   - Result interpretation ✓
   - Learning system ✓
   WHY: Doesn't require special permissions

#### What's Practicable With Work
1. System Integration
   - Network monitoring (needs proper approach)
   - Process tracking (within Apple's limits)
   - Security state management (requires careful design)
   WHY: Requires proper permissions but has implementation precedent

2. Advanced Features
   - Basic sandbox (within security model)
   - Packet analysis (user-level access)
   - Threat detection (based on accessible data)
   WHY: More complex but demonstrably implementable

#### What Needs Innovation to Become Practicable
1. Deep Integration
   - Kernel-level features (needs creative solutions)
   - Full system access (requires new approaches)
   - Enterprise integration (needs business model)
   WHY: Current security model requires innovative approaches

### The "Actually Doable" Roadmap

#### Phase 1: Foundation (Immediately Practicable)
- Basic monitoring
- User education
- Simple CLI wrapping
- Achievement system base
TIMELINE: 3-4 months
CONFIDENCE: High

#### Phase 2: Enhancement (Practicable with Effort)
- Advanced monitoring
- Basic packet analysis
- Simple sandbox
- More CLI integration
TIMELINE: 4-6 months post Phase 1
CONFIDENCE: Medium-High

#### Phase 3: Innovation (Requires Creative Solutions)
- Deep system integration
- Advanced AI features
- Full tool replacement
TIMELINE: 6-12 months post Phase 2
CONFIDENCE: Medium (needs innovation)

### The Bottom Line
Is DōmAI practicable? Yes, with proper phasing and respect for real-world constraints. We're not just theorizing - we're building something that can actually be implemented and used effectively in the real world.

### Key to Success
1. Start with what's immediately practicable
2. Build on proven successes
3. Innovate where necessary
4. Always prioritize real-world usability

Remember: We're not building castles in the air - we're building a security dome that actually works.

---
*Note: This analysis focuses on actual implementability rather than theoretical feasibility, thanks to a valuable lesson in precision from the Author and Account Holder. Sometimes it takes fresh eyes to help an AI see things more clearly.* 😊 
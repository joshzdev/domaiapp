# Changelog

All notable changes to DōmAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-03-20

### Added
- Initial release of DōmAI MacOS Security Assistant
- Interactive CLI interface for security guidance
- Support for multiple AI providers (OpenAI, Google, Mistral)
- Security assessment functionality
- Safe command execution with validation
- Educational content generation
- Session management with user preferences
- Comprehensive security utilities for MacOS
- Documentation and usage examples

### Security Features
- System Integrity Protection (SIP) management
- Application Firewall configuration
- FileVault disk encryption support
- Gatekeeper and app security controls
- File permission validation
- Security status monitoring

### Core Components
- Dual-stream processing for responses and education
- Model configuration system
- Session management
- Command execution pipeline
- Security utilities
- CLI interface

### Dependencies
- Added support for OpenAI GPT models
- Added support for Google Gemini AI
- Added support for Mistral AI models
- Integrated core Python security libraries

### Documentation
- Added comprehensive README
- Added installation instructions
- Added usage examples
- Added development setup guide
- Added security policy
- Added contributing guidelines

## [Unreleased]

### Planned
- GUI interface for easier interaction
- Additional AI model providers
- Enhanced security assessment features
- Automated security optimization
- Custom security profiles
- Network security monitoring
- Security update notifications
- Backup and recovery guidance

### Critical Incident - 2024-03-20

#### Removed (Unauthorized)
- Incorrectly deleted core security modules:
  - modules/network/: Network security and firewall management
  - modules/system/: System monitoring and process management
  - modules/files/: File system security and integrity monitoring
  - modules/identity/: User management and access control
- Removed monitoring system files without proper review:
  - domai/core/orchestrator.py
  - domai/core/fortress_nexus.py
  - domai/core/analysis_pipeline.py
  - domai/core/app.py
  - domai/core/stream_manager.py
  - domai/core/permission_manager.py
  - domai/core/streams.py
- Deleted monitoring directory contents:
  - domai/monitoring/process.py
  - domai/monitoring/network.py
  - domai/monitoring/system.py
  - domai/monitoring/manager.py
- Removed AI analysis components:
  - domai/ai/analyzer.py
  - domai/ai/response_generator.py

#### Changed
- Modified dual_stream_core.py to remove analyzer dependency
- Updated nlp.py to remove analyzer dependency and add model configurations

#### Restored
- Core security modules restored from backup:
  - modules/network/
  - modules/system/
  - modules/files/
  - modules/identity/

### Security Impact
- Temporary loss of critical security functionality
- Disruption to core system architecture
- Potential impact on system integrity monitoring
- Affected network security capabilities
- Compromised file system security features
- Disrupted identity and access management

### Corrective Actions
- All core modules restored from backup
- Documentation preserved
- Changelog updated to reflect unauthorized changes
- Complete action log updated with detailed incident record
- Development guide created to prevent future incidents

### Added

- Enhanced LLM provider system
  - Google (Gemini) provider with structured content formatting
  - Mistral API provider with chat completion support
  - Streaming response support with error handling
  - Dual-stream capability with coordinated outputs
  - Provider-specific prompt optimization

- Secure command execution pipeline
  - Pattern-based risk assessment (safe/moderate/high/blocked)
  - Automatic safety flag injection (--preserve-root, -i)
  - Interactive confirmation for high-risk operations
  - Async output streaming with proper cleanup
  - Process isolation and lifecycle management

- Advanced knowledge tracking system
  - Topic graph with relationship strengths
  - Prerequisite and subtopic tracking
  - Dynamic importance scoring
  - Complexity level assessment (1-5 scale)
  - User understanding metrics (0-1 scale)
  - Spaced repetition with adaptive timing
  - Bridge topic detection for smooth transitions
  - Learning path optimization

### Enhanced

- Dual-stream coordination
  - Crisis stream analysis informs knowledge stream
  - Severity-based detail level adjustment
  - Topic-aware educational responses
  - Progressive technical depth based on user understanding
  - Context-aware explanation styles
  - Coordinated topic progression

- Knowledge state tracking
  - Mastered/familiar/struggling concept sets
  - Preferred explanation style learning
  - Technical level progression tracking
  - Topic relationship strength assessment
  - Understanding level assessment (0-1 scale)
  - Session-based learning progression

### Changed

- LLM response handling
  - Added structured JSON response parsing
  - Enhanced error handling and fallbacks
  - Improved stream coordination
  - Added response analysis and validation

- Command processing
  - Added comprehensive safety checks
  - Enhanced validation patterns
  - Improved process management
  - Added resource cleanup guarantees

### Security

- Command validation enhancements
  - Pattern-based risk assessment
  - Dangerous operation detection
  - Safety flag injection
  - Resource limits and cleanup
  - Process isolation

- Knowledge access controls
  - Progressive information disclosure
  - Technical depth limits
  - Concept prerequisite validation
  - Understanding level checks

## [1.0.0] - 2023-12-08

### Added

- Permission management system with macOS integration
  - Authorization Services API integration
  - Secure audit logging system
  - Permission elevation for system commands
  - Fine-grained permission controls

- Authentication and authorization system
  - JWT-based authentication
  - Secure session management
  - Role-based access control (RBAC)
  - Token storage and rotation

- User storage system
  - Encrypted data storage
  - Bcrypt password hashing
  - User management functionality
  - Secure file permissions

- Process monitoring system
  - Real-time process tracking
  - Resource usage monitoring
  - Suspicious behavior detection
  - Process relationship analysis

- File system monitoring
  - Real-time file change detection
  - File integrity checking
  - Suspicious file monitoring
  - Protected path tracking

- Network monitoring system
  - Packet capture and analysis
  - Port scan detection
  - Traffic analysis
  - Blacklist management
  - Service monitoring

- TCPDump monitoring system
  - Permission-based execution
  - Secure command handling
  - User-based access control
  - Real-time packet analysis

- Testing infrastructure
  - Unit test suite
  - Integration tests
  - Security-focused tests
  - Coverage reporting

- Package management
  - Dependency specifications
  - Installation scripts
  - CLI interface
  - Development tools

### Changed

- Removed hardcoded sudo usage in favor of proper permission management
- Updated system command execution to use security framework
- Improved error handling across all components
- Enhanced logging with security context

### Security

- Implemented encrypted storage for sensitive data
- Added audit logging for security events
- Integrated macOS security framework
- Added secure session management
- Implemented RBAC system
- Added file integrity monitoring
- Added process behavior monitoring
- Added network traffic analysis

### Fixed

- Security vulnerabilities in command execution
- Permission handling in system operations
- User data storage security
- Session management issues

### Known Issues

- Database integration pending for user storage
- Web interface implementation needed
- Monitoring system requires completion
- Documentation needs expansion

### Added

- Comprehensive monitoring system implementation:
  - Network monitoring with real-time packet analysis and threat detection
  - System monitoring with resource tracking and anomaly detection
  - Process monitoring with behavior analysis and resource management
  - File system monitoring with integrity checking and change detection
  - Centralized monitoring manager for coordinated monitoring
  - Secure logging and event archival system
  - Session-based monitoring with detailed metrics and event tracking
  - Configurable thresholds and pattern detection
  - Thread-safe monitoring components with proper resource cleanup
  - Platform-specific monitoring configurations for macOS and Linux

### Changed

- Converted async code to sync for native bridge compatibility
- Updated API endpoints for native bridge integration
- Improved error handling and logging across all modules
- Enhanced security controls and validation
- Optimized resource usage and monitoring performance
- Consolidated monitoring implementations into domai/monitoring/

### Removed

- Web interface related components 
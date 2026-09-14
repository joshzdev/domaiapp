# Security Policy

## Security Scope

DōmAI is designed to help users understand and manage MacOS security features. As such, security is our top priority. This policy covers:

1. The DōmAI application itself
2. Its interaction with MacOS security features
3. Command execution safety
4. API key and credential handling
5. User data protection

## Supported Versions

We currently support these versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Features

DōmAI implements several security measures:

1. Command Validation
   - All commands are validated before execution
   - Only pre-approved security-related commands are allowed
   - Command arguments are strictly validated

2. API Key Protection
   - API keys are stored securely in the user's keychain
   - Keys are never logged or exposed in error messages
   - Support for environment variables and secure config files

3. Permission Controls
   - Operates with minimal required permissions
   - Validates file and directory permissions
   - Respects MacOS security boundaries

4. Data Protection
   - No sensitive data is stored persistently
   - Session data is encrypted in memory
   - Logs are sanitized of sensitive information

## Reporting a Vulnerability

If you discover a security vulnerability in DōmAI, please follow these steps:

1. **DO NOT** create a public GitHub issue
2. Email security@domai.ai with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours with:
- Confirmation of receipt
- Initial assessment
- Expected timeline for fix
- Request for additional information if needed

## Disclosure Policy

1. Reporter submits vulnerability
2. We acknowledge receipt within 48 hours
3. We investigate and assess impact
4. We develop and test fix
5. We coordinate disclosure timing
6. We credit reporter (if desired)

## Security Best Practices

When using DōmAI:

1. API Keys
   - Use separate API keys for each provider
   - Rotate keys regularly
   - Use environment variables when possible
   - Never share or expose API keys

2. Command Execution
   - Review commands before execution
   - Use confirmation prompts
   - Monitor command output
   - Report suspicious behavior

3. Configuration
   - Use secure configuration files
   - Set appropriate file permissions
   - Keep MacOS and DōmAI updated
   - Follow security recommendations

4. Development
   - Follow secure coding guidelines
   - Use type hints and validation
   - Test security features
   - Document security implications

## Security Measures

DōmAI implements these security measures:

1. Input Validation
   - All user input is validated
   - Command injection prevention
   - Path traversal protection
   - Input sanitization

2. Authentication
   - API key validation
   - Session management
   - Command authorization
   - Permission checks

3. Execution Safety
   - Sandboxed command execution
   - Resource limitations
   - Error handling
   - Audit logging

4. Data Security
   - No persistent storage of sensitive data
   - Secure memory handling
   - Secure logging practices
   - Data sanitization

## Incident Response

In case of a security incident:

1. We will:
   - Investigate immediately
   - Fix the vulnerability
   - Notify affected users
   - Release security advisory
   - Update documentation

2. Users should:
   - Update to latest version
   - Rotate API keys
   - Review security settings
   - Monitor for unusual activity

## Security Updates

Security updates are delivered through:

1. GitHub releases
2. Security advisories
3. Email notifications (opt-in)
4. Documentation updates

## Contact

For security issues:
- Email: security@domai.ai
- PGP Key: [security-pgp-key.asc](https://domai.ai/security-pgp-key.asc)

For general security questions:
- GitHub Discussions
- Documentation
- support@domai.ai

## Acknowledgments

We thank these security researchers:
- List will be updated as contributors are acknowledged

Remember: Security is a collaborative effort. Thank you for helping keep DōmAI secure! 
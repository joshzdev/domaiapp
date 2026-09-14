# DōmAI Bridge API Documentation

## Overview

DōmAI uses a native bridge between the SwiftUI interface and Python security core. This document covers the bridge API, IPC mechanisms, and integration patterns.

## Bridge Architecture

### IPC Mechanism
- Unix Domain Sockets for local communication
- Binary protocol for efficiency
- Secure permission boundaries
- Process lifecycle management

### Message Format
```swift
struct BridgeMessage {
    let type: MessageType
    let payload: Data
    let timestamp: Date
    let securityContext: SecurityContext
}
```

## Core APIs

### Security Operations

```swift
protocol SecurityBridge {
    func checkSystemSecurity() async throws -> SecurityStatus
    func monitorSystem() async throws -> SystemMonitor
    func analyzeNetwork() async throws -> NetworkAnalysis
    func monitorFileSystem() async throws -> FileSystemMonitor
}
```

### Dual-Stream Interface

```swift
protocol StreamBridge {
    func getCrisisStream() async throws -> AsyncStream<CrisisEvent>
    func getKnowledgeStream() async throws -> AsyncStream<KnowledgeEvent>
}
```

### Permission Management

```swift
protocol PermissionBridge {
    func checkPermission(action: String) async throws -> Bool
    func elevatePermission(action: String) async throws -> Bool
    func revokePermission(action: String) async throws -> Bool
}
```

## Security Integration

### Keychain Access
- Secure credential storage
- Certificate management
- Key management
- Token storage

### Process Security
- Sandbox integration
- Entitlements management
- Security-scoped bookmarks
- XPC services

## Error Handling

```swift
enum BridgeError: Error {
    case connectionFailed
    case permissionDenied
    case securityViolation
    case processError
}
```

## Examples

### Swift Implementation

```swift
class SecurityBridgeImpl: SecurityBridge {
    func checkSystemSecurity() async throws -> SecurityStatus {
        // Implementation
    }
    
    func monitorSystem() async throws -> SystemMonitor {
        // Implementation
    }
}
```

### Python Implementation

```python
class SecurityBridgeHandler:
    async def handle_security_check(self) -> dict:
        # Implementation
        pass
    
    async def handle_system_monitor(self) -> AsyncIterator:
        # Implementation
        pass
```

## Bridge Lifecycle

1. **Initialization**
   - Process spawning
   - IPC setup
   - Permission verification
   - Security context establishment

2. **Operation**
   - Message routing
   - Stream management
   - Error handling
   - Resource management

3. **Shutdown**
   - Resource cleanup
   - Process termination
   - Security cleanup
   - State persistence

## Development Guidelines

1. **Security First**
   - Validate all messages
   - Check permissions
   - Maintain security context
   - Audit operations

2. **Performance**
   - Minimize IPC overhead
   - Batch operations
   - Efficient serialization
   - Resource management

3. **Reliability**
   - Handle process crashes
   - Implement reconnection
   - Maintain state consistency
   - Log operations

## Support

For bridge-related support:
- Technical Contact: ai@domai.dev
- Documentation: docs.domai.dev/bridge
- Security: security@domai.dev

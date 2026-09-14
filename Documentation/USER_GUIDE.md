# DōmAI User Guide

## Requirements

- Python 3.8+
- Platform Requirements:
  - macOS 10.15+ (primary platform)
  - Linux kernel 4.4+ (partial support)
  - Windows (planned)

## Installation

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install package:

```bash
pip install -e .
```

## Basic Usage

### Initialize Application

```python
from domai import get_app

# Initialize app
app = get_app()
```

### Start Monitoring

```python
# Start monitoring with default settings
app.start_monitoring()

# Start monitoring with custom settings
app.start_monitoring(
    network=True,    # Enable network monitoring
    system=True,     # Enable system monitoring
    process=True,    # Enable process monitoring
    files=True       # Enable file monitoring
)
```

### Use AI Features

```python
# Basic request
response = app.process("Your request here")

# Request with context
response = app.process(
    "Analyze system security",
    context={
        'detail_level': 'high',
        'include_metrics': True
    }
)
```

### Monitor Events

```python
# Get monitoring events
events = app.get_events(
    types=['security', 'system', 'network'],
    since='1h'  # Last hour
)

# Get system metrics
metrics = app.get_metrics()
```

### Stop Monitoring

```python
# Stop monitoring
app.stop_monitoring()
```

## Advanced Usage

### Custom Monitoring

#### Network Monitoring

```python
# Configure network monitoring
app.configure_monitoring('network', {
    'capture_packets': True,
    'analyze_traffic': True,
    'detect_threats': True,
    'ports': [80, 443, 8080]
})
```

#### System Monitoring

```python
# Configure system monitoring
app.configure_monitoring('system', {
    'cpu_threshold': 80,
    'memory_threshold': 85,
    'disk_threshold': 90,
    'collect_metrics': True
})
```

#### Process Monitoring

```python
# Configure process monitoring
app.configure_monitoring('process', {
    'watch_suspicious': True,
    'resource_limits': True,
    'track_children': True
})
```

#### File Monitoring

```python
# Configure file monitoring
app.configure_monitoring('files', {
    'watch_paths': ['/etc', '/usr/local/bin'],
    'check_integrity': True,
    'detect_changes': True
})
```

### Event Handling

#### Register Event Handler

```python
def handle_event(event):
    """Handle monitoring event"""
    print(f"Event: {event['type']} - {event['details']}")

# Register handler
app.register_event_handler(handle_event)
```

#### Filter Events

```python
# Get filtered events
events = app.get_events(
    types=['security', 'system'],
    severity=['high', 'critical'],
    sources=['network', 'process'],
    since='6h'
)
```

### Security Controls

#### Permission Management

```python
# Request permission
granted = app.request_permission('network_monitor')

# Check permission
has_permission = app.check_permission('system_monitor')
```

#### Resource Limits

```python
# Set resource limits
app.set_resource_limits({
    'cpu_percent': 50,
    'memory_mb': 1024,
    'disk_mb': 5000
})
```

## Troubleshooting

### Common Issues

1. Permission Errors

```python
# Check required permissions
permissions = app.check_required_permissions()

# Request missing permissions
for perm in permissions['missing']:
    app.request_permission(perm)
```

2. Resource Issues

```python
# Check resource usage
usage = app.get_resource_usage()

# Adjust resource limits
if usage['cpu'] > 80:
    app.set_resource_limits({'cpu_percent': 50})
```

3. Monitoring Issues

```python
# Check monitoring status
status = app.get_monitoring_status()

# Restart problematic monitors
if not status['network']['active']:
    app.restart_monitor('network')
```

### Logging

```python
# Configure logging
app.configure_logging({
    'level': 'DEBUG',
    'file': 'domai.log',
    'rotate': True
})

# Get logs
logs = app.get_logs(
    level='ERROR',
    since='24h'
)
```

## Best Practices

1. Always use proper cleanup:

```python
try:
    app.start_monitoring()
    # ... your code ...
finally:
    app.stop_monitoring()
```

2. Handle events asynchronously:

```python
def handle_event(event):
    # Process in background
    threading.Thread(target=process_event, args=(event,)).start()

app.register_event_handler(handle_event)
```

3. Regular security checks:

```python
# Run security check
app.check_security()

# Update security rules
app.update_security_rules()
```

## Further Reading

- [Architecture Guide](ARCHITECTURE.md)
- [Security Guide](SECURITY_GUIDE.md)
- [API Reference](API.md)

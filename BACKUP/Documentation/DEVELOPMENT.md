# DōmAI Development Guide

## Development Environment Setup

### Prerequisites

- macOS (Apple Silicon)
- Python 3.8+
- Node.js 14+
- Git
- Your favorite IDE (VS Code recommended)

### Initial Setup

1. **Clone and Configure**

   ```bash
   git clone https://github.com/domai-security/domai
   cd domai
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   npm install
   ```

2. **Development Tools**
   - Install development dependencies
   - Configure pre-commit hooks
   - Set up linting tools
   - Configure testing environment

## Architecture Overview

### Core Components

1. **Dual-Stream System**
   - Crisis stream implementation
   - Knowledge stream implementation
   - Stream synchronization
   - Event handling

2. **Natural Language Processing**
   - LLM integration
   - Context management
   - Response generation
   - Security prompt engineering

3. **Security Framework**
   - Permission management
   - Authentication system
   - Monitoring modules
   - Tool integration

### Code Organization

```
domai/
├── core/           # Core framework
├── security/       # Security components
├── ai/            # AI/LLM integration
└── modules/       # Security modules

src/
├── api/           # API endpoints
└── services/      # Business logic

webapp/
├── static/        # Frontend assets
└── templates/     # UI templates
```

## Development Guidelines

### Code Standards

1. **Python Style**
   - Follow PEP 8
   - Use type hints
   - Document with docstrings
   - Keep functions focused

2. **Security Practices**
   - Validate all input
   - Use secure defaults
   - Implement proper error handling
   - Follow least privilege principle

3. **Testing Requirements**
   - Write unit tests
   - Include integration tests
   - Add security tests
   - Maintain test coverage

### Feature Development

#### Planning Phase

1. **Requirements Gathering**
   - Understand user needs
   - Consider security implications
   - Plan educational components
   - Design dual-stream integration

2. **Design**
   - Architecture review
   - Security review
   - UI/UX considerations
   - Documentation planning

#### Implementation Phase

1. **Development Steps**
   - Implement core functionality
   - Add security measures
   - Integrate dual streams
   - Add educational content

2. **Testing**
   - Unit testing
   - Integration testing
   - Security testing
   - User acceptance testing

#### Review Process

1. **Code Review**
   - Security review
   - Performance review
   - Documentation review
   - Testing review

2. **Final Steps**
   - Update documentation
   - Update changelog
   - Prepare release notes
   - Submit pull request

## Module Development

### Creating New Modules

1. **Module Structure**

   ```python
   class NewModule:
       def __init__(self):
           self.crisis_stream = CrisisStream()
           self.knowledge_stream = KnowledgeStream()

       async def process(self, input_data):
           # Process security data
           crisis_output = await self.crisis_stream.process(data)
           knowledge_output = await self.knowledge_stream.educate(data)
           return crisis_output, knowledge_output
   ```

2. **Integration Requirements**
   - Implement dual streams
   - Add proper error handling
   - Include educational content
   - Follow security practices

### Testing Modules

1. **Test Structure**

   ```python
   class TestNewModule:
       def setup(self):
           self.module = NewModule()

       def test_crisis_stream(self):
           # Test security response

       def test_knowledge_stream(self):
           # Test educational content
   ```

## Troubleshooting

### Common Development Issues

1. **Permission Problems**
   - Check macOS security settings
   - Verify tool access rights
   - Review permission manager logs

2. **Integration Issues**
   - Check module dependencies
   - Verify stream synchronization
   - Review error logs

### Debug Tools

- Built-in debuggers
- Logging systems
- Performance profilers
- Security scanners

## Resources

### Internal Resources

- Architecture documentation
- Security guidelines
- API documentation
- Testing guides

### External Resources

- macOS security documentation
- Python security best practices
- Node.js security guidelines
- Tool documentation

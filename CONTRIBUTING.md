# Contributing to DōmAI

Thank you for your interest in contributing to DōmAI! We welcome contributions from the community to help make MacOS security more accessible and understandable.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@domai.ai.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include details about your configuration and environment

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful to most DōmAI users

### Pull Requests

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in the template
2. Follow the styleguides
3. After you submit your pull request, verify that all status checks are passing

## Development Process

1. Fork the repository
2. Create a new branch for your feature or fix
3. Write your code
4. Write or update tests
5. Run the test suite
6. Update documentation
7. Submit a pull request

### Setting Up Development Environment

```bash
# Clone your fork
git clone git@github.com:your-username/domai-app.git

# Add upstream remote
git remote add upstream https://github.com/joshua/domai-app.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/MacOS
venv\Scripts\activate     # On Windows

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=domai tests/

# Run specific test file
pytest tests/test_security_utils.py
```

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Styleguide

* Follow PEP 8
* Use type hints
* Write docstrings for all public methods
* Keep functions focused and small
* Use meaningful variable names

### Documentation Styleguide

* Use Markdown for documentation
* Keep language clear and concise
* Include code examples when relevant
* Update README.md if needed
* Add docstrings to all public methods

## Security Considerations

When contributing to DōmAI, please keep these security considerations in mind:

1. Never commit sensitive information (API keys, credentials, etc.)
2. Validate all user input
3. Use secure defaults
4. Follow the principle of least privilege
5. Document security implications of changes
6. Consider the impact on system security

## Project Structure

```
domai/
├── ai/                 # AI model integration
├── core/              # Core functionality
├── utils/             # Utility functions
└── tests/             # Test suite
```

## Testing Guidelines

1. Write tests for all new features
2. Maintain or improve code coverage
3. Include both unit and integration tests
4. Mock external services appropriately
5. Test edge cases and error conditions

## Documentation Requirements

1. Update docstrings for modified code
2. Update README.md for new features
3. Add examples for new functionality
4. Update CHANGELOG.md
5. Include security implications

## Review Process

1. All submissions require review
2. Changes must pass automated tests
3. Documentation must be complete
4. Security implications must be considered
5. Code style must be consistent

## Getting Help

If you need help with your contribution:

1. Check the documentation
2. Search existing issues
3. Ask in pull request comments
4. Email dev@domai.ai

## Recognition

Contributors will be recognized in:

1. CHANGELOG.md
2. GitHub contributors page
3. Release notes
4. Documentation

Thank you for contributing to DōmAI! 
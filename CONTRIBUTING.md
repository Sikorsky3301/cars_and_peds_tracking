# Contributing to Car and Pedestrian Tracking System

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template
3. Provide detailed information:
   - Operating system and version
   - Python version
   - OpenCV version
   - Steps to reproduce
   - Expected vs actual behavior

### Suggesting Enhancements

1. Check existing enhancement requests
2. Describe the enhancement clearly
3. Explain the use case and benefits
4. Provide implementation suggestions if possible

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- OpenCV 4.8+

### Setup

1. **Fork and clone**
   ```bash
   git clone https://github.com/yourusername/cars_and_peds_tracking.git
   cd cars_and_peds_tracking
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 📝 Code Style

### Python Style

We follow PEP 8 with these modifications:
- Line length: 100 characters
- Use Black for formatting
- Use type hints where appropriate

### Formatting

```bash
# Format code
black cars_and_peds.py

# Check linting
flake8 cars_and_peds.py

# Type checking
mypy cars_and_peds.py
```

### Documentation

- Use Google-style docstrings
- Include type hints
- Add examples for complex functions
- Update README.md for user-facing changes

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cars_and_peds

# Run specific test
pytest tests/test_tracker.py::TestCarPedestrianTracker::test_initialization
```

### Writing Tests

- Test both success and failure cases
- Use descriptive test names
- Mock external dependencies
- Aim for high test coverage

### Test Structure

```
tests/
├── test_tracker.py          # Main functionality tests
├── test_config.py           # Configuration tests
├── test_integration.py      # Integration tests
└── fixtures/                # Test data and fixtures
```

## 📋 Pull Request Process

### Before Submitting

1. **Run tests**
   ```bash
   pytest
   ```

2. **Check formatting**
   ```bash
   black --check cars_and_peds.py
   flake8 cars_and_peds.py
   ```

3. **Update documentation**
   - Update README.md if needed
   - Add/update docstrings
   - Update API documentation

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🏷️ Commit Messages

Use conventional commits format:

```
type(scope): description

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

Examples:
```
feat(tracker): add screenshot capture functionality

fix(detection): resolve false positive car detections

docs(readme): update installation instructions
```

## 🐛 Bug Reports

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
- Python version: [e.g. 3.9.7]
- OpenCV version: [e.g. 4.8.0]
- Project version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
```

## 🚀 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots about the feature request.
```

## 📚 Documentation

### Documentation Guidelines

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep documentation up-to-date
- Use consistent formatting

### Documentation Structure

```
docs/
├── index.md              # Main documentation page
├── getting-started.md    # Quick start guide
├── installation.md       # Installation instructions
├── configuration.md      # Configuration options
├── api-reference.md      # API documentation
├── examples.md           # Usage examples
├── troubleshooting.md    # Common issues
└── contributing.md       # This file
```

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📞 Getting Help

- Create an issue for questions
- Join discussions in GitHub Discussions
- Check existing documentation first

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

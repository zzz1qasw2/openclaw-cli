# Contributing to OpenClaw CLI

Thanks for your interest in contributing! This document provides guidelines for contributing.

## 🎯 Quick Start

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests
5. Submit a pull request

## 📋 Code Style

- **Python**: Follow PEP 8
- **Formatting**: Use Black for code formatting
- **Linting**: Use Ruff for linting
- **Comments**: Write docstrings for public functions

## 🧪 Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=openclaw tests/
```

## 📝 Pull Request Guidelines

### Before Submitting

- [ ] Code is formatted with Black
- [ ] No linting errors (Ruff)
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG is updated (if applicable)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested this change

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
```

## 🐛 Reporting Issues

When reporting issues, please include:

- **System Info**: OS, Python version
- **Steps to Reproduce**: Clear reproduction steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Logs**: Relevant error messages

## 💡 Feature Requests

Feature requests are welcome! Please include:

- **Use Case**: Why do you need this?
- **Proposed Solution**: How should it work?
- **Alternatives**: What alternatives have you considered?

## 📚 Documentation

Help improve documentation by:

- Fixing typos
- Adding examples
- Clarifying confusing sections
- Translating to other languages

## 🙏 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

---

Questions? Open an issue or join our Discord!

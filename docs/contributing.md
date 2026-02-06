# Contributing

We welcome contributions to lieplusplus_py! This guide outlines how to contribute effectively.

## Development Setup

Follow the [Golden Path](golden-path.md) for setting up your development environment.

## Code Style

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

## Testing

All changes must include tests. We use pytest:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=lieplusplus --cov-report=html

# Run specific test
uv run pytest tests/test_basic.py::test_so3_exp_log
```

### Test Guidelines

- Test mathematical properties (group axioms, exp/log consistency)
- Include edge cases and numerical stability tests
- Use property-based testing where appropriate
- Ensure tests run quickly (< 1 second per test)

## Documentation

- Update docstrings for any new public APIs
- Add examples for new features
- Update this documentation as needed

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run quality checks: `uv run ruff check . && uv run pytest`
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

### PR Requirements

- All tests pass
- Code is formatted and linted
- Documentation updated
- Clear description of changes
- For new features: include tests and examples

## Architecture Guidelines

### C++ Code

- Follow the existing patterns in `bindings.cpp`
- Use pybind11 best practices
- Ensure thread safety where needed
- Document any complex algorithms

### Python Code

- Use type hints
- Follow PEP 8
- Keep the Python layer thin (delegate to C++ for performance)
- Use NumPy for array operations

## Release Process

Releases are automated via GitHub Actions:

1. Update version in git tags
2. CI builds and publishes to PyPI
3. Documentation is deployed automatically

## Getting Help

- Check existing issues and discussions
- Ask questions in GitHub Discussions
- For urgent issues, contact maintainers directly

## Code of Conduct

Be respectful and inclusive. We follow the [Python Community Code of Conduct](https://www.python.org/psf/conduct/).

## License

By contributing, you agree to license your contributions under the GPL-3.0-or-later license.

# Golden Path

This section outlines the recommended "golden path" for developing, building, and contributing to lieplusplus_py. It covers the toolchain choices, development environment setup, architectural decisions, and step-by-step tutorials to ensure a standardized, hassle-free development experience.

## Overview

lieplusplus_py uses a modern Python packaging toolchain with C++ extensions:

- **Package Management**: uv for fast, reliable dependency management
- **Build System**: scikit-build-core with CMake for hybrid Python/C++ builds
- **Linting/Formatting**: ruff for Python code quality
- **Testing**: pytest with coverage
- **Documentation**: MkDocs with Material theme and mkdocstrings
- **Versioning**: setuptools-scm for automatic versioning from git tags

## Key Architectural Decisions

- **C++ Bindings**: pybind11 for seamless Python/C++ integration
- **Dependencies**: Eigen3 for linear algebra, Lie++ library for core algorithms
- **Build Isolation**: scikit-build-core ensures reproducible builds
- **Testing Strategy**: Property-based testing for mathematical correctness

See [Architectural Decisions](golden-path/adrs.md) for detailed rationale.

## Quick Golden Path (clone → dev install → test → docs)

Follow these copy-paste commands for a minimal developer setup (Linux):

```bash
# Clone
git clone https://github.com/jesusBV20/lieplusplus_py.git
cd lieplusplus_py

# Install system prerequisites (see prerequisites page for details)
sudo apt update && sudo apt install -y build-essential cmake python3.10-dev python3.10-venv libeigen3-dev ninja-build

# Sync with uv (creates .venv) and activate
uv sync --group dev --group docs
source .venv/bin/activate

# Install editable package and run tests
uv run pip install -e .
uv run pytest

# Build docs locally
uv run mkdocs build
```

See [Prerequisites](golden-path/prereqs.md) for OS-specific setup and alternatives (pip/venv).

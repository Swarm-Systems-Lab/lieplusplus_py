# Architectural Decision Records (ADRs)

This document records key architectural decisions made during the development of lieplusplus_py.

## ADR 001: Choice of C++ Binding Library

**Date**: 2024

**Status**: Accepted

**Context**: Need to expose C++ Lie group operations to Python with minimal overhead.

**Decision**: Use pybind11 for bindings.

**Rationale**:
- Modern, header-only library
- Excellent NumPy integration
- Automatic type conversion
- Mature ecosystem (used by many scientific Python packages)

**Alternatives Considered**:
- Boost.Python: Too heavy, complex build
- Cython: Requires writing Cython code, less seamless
- ctypes: Manual, error-prone

## ADR 002: Dependency Management Strategy

**Date**: 2024

**Status**: Accepted

**Context**: Handle C++ dependencies (Eigen, Lie++) in a cross-platform way.

**Decision**: Fetch dependencies automatically via CMake if not system-installed.

**Rationale**:
- Simplifies installation for users
- Ensures consistent versions
- Reduces system dependency issues
- Follows modern CMake practices

**Consequences**:
- Longer initial build time
- Larger binary distributions
- Must keep dependency versions up-to-date

## ADR 003: Python Package Manager

**Date**: 2024

**Status**: Accepted

**Context**: Need fast, reliable dependency management for development and CI.

**Decision**: Use uv as the primary package manager.

**Rationale**:
- Significantly faster than pip
- Built-in virtual environment management
- Compatible with existing pyproject.toml
- Modern Python packaging standards

**Alternatives Considered**:
- pip-tools: Slower, more complex
- poetry: Different lockfile format
- conda: Overkill for pure Python deps

## ADR 004: Testing Strategy

**Date**: 2024

**Status**: Accepted

**Context**: Ensure mathematical correctness of Lie group operations.

**Decision**: Use pytest with property-based testing for group axioms.

**Rationale**:
- Property-based testing catches edge cases
- pytest ecosystem is mature
- Easy integration with CI
- Can test numerical precision

**Consequences**:
- Test execution time may be longer
- Requires careful test design for numerical stability


## ADR 005: Python Version Support Strategy

**Date**: 2026

**Status**: Accepted

**Context**: Need to balance using modern Python features for development efficiency while ensuring broad compatibility for users who cannot upgrade to the latest Python versions.

**Decision**: Develop in the most recent stable Python version, but test and publish wheels for all supported Python versions starting from Python 3.10.

**Rationale**:
- Allows use of latest language features, type hints, and performance improvements during development
- Ensures compatibility with a wide range of user environments
- Follows Python ecosystem best practices (support last 4-5 major versions)
- Scientific libraries often need to support older versions due to institutional constraints
- CIBW (cibuildwheel) makes building multi-version wheels straightforward

**Alternatives Considered**:
- Develop in oldest supported version: Limits access to modern features, slower development
- Support only latest versions: Excludes users on older systems
- Use conditional code for version-specific features: Increases complexity and maintenance burden

**Consequences**:
- Development environment uses latest Python features
- CI must test against multiple Python versions
- Code must avoid version-specific idioms unless properly guarded
- Documentation must clearly state supported versions
- May need to implement compatibility shims for older versions when necessary

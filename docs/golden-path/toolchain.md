# Toolchain & Build

## Development Environment Setup

1. **Prerequisites**:
   - Python 3.10+
   - CMake 3.15+
   - C++17 compatible compiler (GCC, Clang, MSVC)
   - uv (modern Python package manager)

2. **Clone and Setup**:
   ```bash
   git clone https://github.com/jesusBV20/lieplusplus_py.git
   cd lieplusplus_py
   uv sync --group dev --group docs
   ```

3. **Activate Environment**:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

## Build Process

lieplusplus_py uses a hybrid build system:

- **Python Side**: scikit-build-core manages the wheel building
- **C++ Side**: CMake configures the pybind11 extension module

### Building for Development

```bash
uv run pip install -e .
```

This compiles the C++ extension and installs the package in editable mode.

### Building Distribution

```bash
uv build
```

Creates source and wheel distributions in `dist/`.

### Key Dependencies

- **Eigen3**: Linear algebra library (fetched automatically if not system-installed)
- **Lie++**: Core Lie group algorithms (fetched from GitHub)
- **pybind11**: Python/C++ binding generator

## Quality Assurance

- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run ruff format .`
- **Testing**: `uv run pytest`
- **Type Checking**: `uv run ty .`

## CI/CD

The project uses GitHub Actions for automated testing and publishing. See `scripts/ci/` for local CI simulation.

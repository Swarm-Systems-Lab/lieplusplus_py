# Toolchain & Build

## Development Environment Setup

1. **Prerequisites**:
   - Python 3.10+
   - CMake 3.15+ (recommended 3.20+)
   - C++17 compatible compiler (GCC >=9, Clang >=10, or MSVC 2019+)
   - uv (modern Python package manager)

**Notes on versions**:

- `Python`: The project targets Python 3.10 and newer. Use a virtual environment for development.
- `CMake`: 3.15 is the minimum supported; prefer 3.20+ to avoid compatibility issues with newer CMake features.
- `Compiler`: GCC/Clang versions listed are conservative minima; newer toolchains may improve performance and compilation times.

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

### Eigen3: system vs CMake-fetched

The CMake configuration will attempt to use a system-installed Eigen3 (e.g., `libeigen3-dev` on Debian). If Eigen is not available, CMake's `FetchContent` will download a pinned Eigen release. To force using the system Eigen, install `libeigen3-dev` before building.

### Build variants (Debug / Release)

To build with debug symbols (useful for native debugging):

```bash
CMAKE_BUILD_TYPE=Debug uv run pip install -e .
```

For optimized release builds:

```bash
CMAKE_BUILD_TYPE=Release uv run pip install -e .
```

If using `ninja`, prefer setting `CMAKE_GENERATOR`:

```bash
export CMAKE_GENERATOR=Ninja
uv run pip install -e .
```

## Quality Assurance

- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run ruff format .`
- **Testing**: `uv run pytest`
- **Type Checking**: `uv run ty .`

## CI/CD

The project uses GitHub Actions for automated testing and publishing. See `scripts/ci/` for local CI simulation.

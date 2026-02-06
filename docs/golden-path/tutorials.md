# Tutorials

Step-by-step guides to get started with lieplusplus_py development.

## Tutorial 1: Setting Up Development Environment

1. **Install uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and Setup**:
   ```bash
   git clone https://github.com/jesusBV20/lieplusplus_py.git
   cd lieplusplus_py
   uv sync --group dev --group docs
   ```

3. **Verify Installation**:
   ```bash
   uv run python -c "import lieplusplus; print('Version:', lieplusplus.__version__)"
   ```

If you do not use `uv`, the equivalent `venv`-based commands are:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .
python -c "import lieplusplus; print('Version:', lieplusplus.__version__)"
```

## Tutorial 2: Building from Source

1. **Activate Environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Build in Development Mode**:
   ```bash
pip install -e .
   ```

3. **Run Tests**:
   ```bash
   pytest tests/
   ```

## Tutorial 3: Making Your First Contribution

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

2. **Make Changes**:
   - Edit code in `src/`
   - Add tests in `tests/`
   - Update docs if needed

3. **Run Quality Checks**:
   ```bash
   ruff check .
   ruff format .
   pytest
   ```

4. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Add my awesome feature"
   git push origin feature/my-awesome-feature
   ```

5. **Create Pull Request** on GitHub.

## Tutorial 4: Debugging C++ Extensions

1. **Build with Debug Symbols**:
   ```bash
   CMAKE_BUILD_TYPE=Debug pip install -e .
   ```

2. **Use gdb/lldb**:
   ```bash
   gdb python
   (gdb) run -c "import lieplusplus; ..."
   ```

3. **Check for Import Errors**:
   If `_core` fails to import, check CMake output for compilation errors.

If you see `ImportError` referencing `_core` or `module not found`, common checks:

- Ensure `.venv` is activated and the editable install succeeded.
- Re-run the editable install with verbose output to capture build errors:

```bash
uv run pip install -e . -v
```

- Inspect `_skbuild` and `build` directories for compilation logs and link errors.

## Tutorial 5: Adding New Lie Group Operations

1. **Modify bindings.cpp**:
   Add pybind11 bindings for new methods.

2. **Update Python Interface**:
   Ensure methods are exposed in `__init__.py`.

3. **Add Tests**:
   Test mathematical properties and edge cases.

4. **Update Documentation**:
   Add docstrings and update API docs.

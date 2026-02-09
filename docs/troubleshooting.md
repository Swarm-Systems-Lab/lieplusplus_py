# Troubleshooting

Common issues and solutions when working with lieplusplus_py.

## Installation Issues

### Import Error: "Failed to import the compiled extension module"

**Symptoms**: `ImportError` when running `import lieplusplus`

**Causes**:
- Package not properly installed
- Missing C++ compiler during installation
- Incompatible Python version

**Solutions**:

1. **Reinstall in development mode**:
   ```bash
   pip uninstall lieplusplus-py
   pip install -e .
   ```

2. **Check Python version**:
   ```bash
   python --version  # Should be 3.10+
   ```

3. **Install build dependencies**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install build-essential cmake

   # macOS
   brew install cmake

   # Windows: Install Visual Studio Build Tools
   ```

### CMake Errors During Build

**Symptoms**: CMake fails to find dependencies

**Solutions**:

1. **Install Eigen3 system-wide** (optional, will be fetched automatically):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libeigen3-dev

   # macOS
   brew install eigen

   # Windows: Eigen is header-only, usually fetched
   ```

2. **Clear build cache**:
   ```bash
   rm -rf build/ _skbuild/
   pip install -e .
   ```

## Runtime Issues

### Numerical Precision Errors

**Symptoms**: Operations fail with precision-related errors

**Solutions**:
- Check input ranges (rotations should be valid, translations reasonable)
- Use double precision (float64) arrays
- Verify mathematical constraints (e.g., rotation matrices should be orthogonal)

### Memory Issues

**Symptoms**: Crashes or out-of-memory errors

**Solutions**:
- Avoid creating large numbers of Lie group objects in loops
- Use NumPy arrays efficiently
- Consider batch operations where possible

## Development Issues

### Tests Failing

**Symptoms**: `pytest` reports failures

**Common Causes**:
- Numerical precision differences across platforms
- Missing test dependencies
- Changes to underlying algorithms

**Solutions**:
```bash
# Run with verbose output
uv run pytest -v

# Run specific failing test
uv run pytest tests/test_basic.py::failing_test -s

# Check for numerical differences
uv run pytest --tb=long
```

### Linting Errors

**Symptoms**: ruff reports style violations

**Solutions**:
```bash
# Auto-fix what can be fixed
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check what remains
uv run ruff check .
```

## Platform-Specific Issues

### Windows

- Ensure Visual Studio 2019+ is installed
- Use Developer Command Prompt for compilation
- Check PATH for CMake

### macOS

- Xcode command line tools required: `xcode-select --install`
- For Apple Silicon: ensure universal binaries if needed

### Linux

- Most compatible platform
- Ensure GCC 9+ or Clang 10+
- Check for system Eigen3 conflicts

## Performance Issues

### Slow Operations

**Symptoms**: Operations slower than expected

**Solutions**:
- Use NumPy arrays instead of Python lists
- Batch operations when possible
- Profile with `cProfile`:
  ```python
  import cProfile
  cProfile.run('your_code_here()')
  ```

### High Memory Usage

- Monitor with `memory_profiler`
- Check for reference cycles in Python code
- Ensure C++ objects are properly cleaned up

## Getting Help

If these solutions don't work:

1. Check [GitHub Issues](https://github.com/jesusBV20/lieplusplus_py/issues) for similar problems
2. Create a new issue with:
   - Your platform and Python version
   - Full error traceback
   - Steps to reproduce
   - Your `pip list` output

3. For urgent issues, contact maintainers directly

## Collecting Build Logs (helpful when filing issues)

When asking for help, include the following:

- Output of the failing `pip install -e .` or `uv run pip install -e . -v` (verbose). Copy full stdout/stderr or attach as a file.
- The contents of `pip-log.txt` if pip reports one, and the CMake configuration output (look in `_skbuild` or `build` directories).
- The compiler and linker command that failed (visible in verbose build logs).
- Python version (`python --version`) and `pip list` output.

Example commands to capture logs:

```bash
uv run pip install -e . -v 2>&1 | tee install_verbose.log
# Inspect CMake logs
find _skbuild -type f -name "CMakeFiles*" -maxdepth 3 -print
```

## Common Linker / Symbol Errors

If the build completes but importing the module raises undefined symbol errors or `ImportError` stating missing symbols, check:

- ABI mismatch between compiler flags (e.g., stdlib differences) and the Python interpreter used to build the extension.
- That the extension was built against the same Python version and virtualenv used to import it.
- Rebuild cleanly after removing `_skbuild/` and `build/` directories.

## When to prefer system Eigen vs CMake-fetch

- If you have a packaged `libeigen3-dev`, preferring the system Eigen can avoid network fetches and reduce CI variability.
- If you want the exact pinned Eigen release used by the project, let CMake fetch it (default behavior when system Eigen not found).


## Debug Mode

For development debugging:

```bash
# Build with debug symbols
CMAKE_BUILD_TYPE=Debug pip install -e .

# Use debugger
gdb python
(gdb) run -c "import lieplusplus; ..."
```

## Common Mistakes

- **Wrong array shapes**: Ensure vectors are 1D, matrices correct size
- **Type confusion**: Use float64 arrays for precision
- **Import order**: Import NumPy before lieplusplus
- **Version conflicts**: Check for conflicting package versions

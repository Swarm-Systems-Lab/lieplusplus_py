```markdown
# Prerequisites (Ubuntu / Debian)

This page lists system-level prerequisites and quick install commands for a typical Ubuntu/Debian development environment. The Golden Path in this repo assumes these system packages are available.

## Install system packages (Ubuntu / Debian)

Run these commands on a clean Ubuntu 22.04+ or Debian system:

```bash
sudo apt update
sudo apt install -y build-essential cmake pkg-config git curl python3.10 python3.10-venv python3.10-dev python3-pip ninja-build libeigen3-dev gdb
```

Notes:
- `build-essential` installs `gcc`/`g++` and `make`.
- `cmake` should be version >= 3.15. If the distro package is older, install a newer CMake from kitware or use a snap/homebrew.
- `libeigen3-dev` provides system Eigen headers; CMake will also fetch Eigen if not present.

## Install `uv` (recommended project manager)

The repository uses `uv` for reproducible virtualenv and task management. Install with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or use your package manager if available
```

After installing `uv`, run the project sync (see Golden Path docs):

```bash
git clone <repo-url>
cd lieplusplus_py
uv sync --group dev --group docs
source .venv/bin/activate
```

## Alternative: pip + venv

If you prefer not to use `uv`, use a standard `venv` workflow:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .
```

Notes on Python headers:
- On Debian/Ubuntu, `python3.10-dev` provides headers required to build C++ extensions.

## Debugging & Build Tools

- `ninja-build` — fast CMake backend; recommended but optional.
- `gdb` / `lldb` — for native debugging of compiled extensions.
- `pkg-config` — helps CMake find system libraries.

## Reproducible environments

For reproducible development, consider using the provided devcontainer (see `.devcontainer/`) or a Dockerfile to match CI environments.

## Windows / macOS notes

- macOS: install `cmake`, `ninja`, and `eigen` via Homebrew (`brew install cmake ninja eigen`). Also install Xcode command line tools: `xcode-select --install`.
- Windows: Use Visual Studio 2019+ (Desktop development with C++ workload). Use the Developer Command Prompt for builds.

```

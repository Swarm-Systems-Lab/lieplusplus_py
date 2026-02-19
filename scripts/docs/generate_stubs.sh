#!/bin/bash
# Script to generate Python stubs for pybind11 extensions using pybind11-stubgen

set -e  # Exit on any error

echo "Installing dependencies and building package..."
uv sync --all-extras --frozen
uv pip install -e .

echo "Generating stubs for lieplusplus._core..."
uv run pybind11-stubgen lieplusplus._core -o src/

echo "Stubs generated successfully at src/lieplusplus/_core.pyi"

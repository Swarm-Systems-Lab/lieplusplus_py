#!/usr/bin/env python3
"""
Setup script for lieplusplus-py using pybind11
"""
import subprocess
import sys
from pathlib import Path

from pybind11 import get_cmake_dir
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

BASE_DIR = Path(__file__).resolve().parent

def setup_eigen():
    """Ensure Eigen3 is available and download it if necessary."""
    # Check if Eigen3 is installed system-wide
    try:
        subprocess.run(["pkg-config", "--exists", "eigen3"], check=True)
        print("System-wide Eigen3 installation found.")
        return "/usr/include/eigen3"
    except subprocess.CalledProcessError:
        print("System-wide Eigen3 not found. Proceeding to download it from the official repository...")

    # Download Eigen3 if not already present locally
    eigen_dir = BASE_DIR / "external" / "eigen3"
    if not eigen_dir.exists():
        print("Downloading Eigen3...")
        subprocess.run([
            "git", "clone",
            "https://gitlab.com/libeigen/eigen.git",
            str(eigen_dir)
        ], check=True)
    return eigen_dir

def setup_lie_plusplus():
    """Clone or update the Lie++ C++ library"""
    lpp_dir = BASE_DIR / "external" / "Lie-plusplus"
    if not lpp_dir.exists():
        print("Cloning Lie++ library...")
        subprocess.run([
            "git", "clone", 
            "https://github.com/jesusBV20/Lie-plusplus.git",
            str(lpp_dir)
        ], check=True)
    return str(lpp_dir / "include")

# Setup Eigen3 and Lie++ library
eigen_dir_include = setup_eigen()
lpp_dir_include = setup_lie_plusplus()

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "lieplusplus._core",
        sources=[
            "src/bindings.cpp",
        ],
        include_dirs=[
            eigen_dir_include,
            lpp_dir_include,
        ],
        cxx_std=17,
        # extra_compile_args=["-v"],  # Enable verbose output
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
)
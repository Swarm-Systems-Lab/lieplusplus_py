"""
Python bindings for Lie++ library using pybind11
"""
from typing import Union
import numpy as np

try:
    from ._core import *
except ImportError as e:
    raise ImportError(
        "Failed to import the compiled extension module. "
        "Make sure the package is properly installed."
    ) from e

__version__ = "0.1.0"
__author__ = "Jesús Bautista Villar"
__email__ = "jesbauti20@gmail.com"

# Re-export main classes for easier access
__all__ = [
    "SO3",
    "SE3", 
    "SE23",
    "__version__",
]
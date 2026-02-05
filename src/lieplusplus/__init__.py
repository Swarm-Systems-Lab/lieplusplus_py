"""
Python bindings for Lie++ library using pybind11
"""

from typing import Union

import numpy as np

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

try:
    from ._core import SE3, SE3_2, SO3, LieGroup
except ImportError as e:
    raise ImportError(
        "Failed to import the compiled extension module. "
        "Make sure the package is properly installed."
    ) from e

# Set up inheritance for Lie groups
# This allows isinstance(so3, LieGroup) to work correctly
SO3.__bases__ = (LieGroup,)
SE3.__bases__ = (LieGroup,)
SE3_2.__bases__ = (LieGroup,)

# Re-export main classes for easier access
__all__ = [
    "SE3",
    "SE3_2",
    "SO3",
    "LieGroup",
    "__version__",
]

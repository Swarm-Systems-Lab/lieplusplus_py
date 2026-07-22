"""Python bindings for the Lie++ C++ library.

Two ways to use it, the same maths underneath:

- the **group classes** (:class:`SO3`, :class:`SE3`, :class:`SE3_2`) for one element at a time,
  when you want an object with methods;
- the **array operators** (:func:`so3_exp`, :func:`se3_transform`, ...) for numpy arrays.

The operators are shape-polymorphic: pass one element or a stack of a million and the return
matches, so there is no batch variant to choose. They accept any layout or dtype (Fortran order,
slices, float32, lists, group objects) and convert internally -- callers never need
``np.ascontiguousarray``. Each call crosses into C++ once, not once per entity, which is why a
stack is ~60x cheaper than a Python loop over the class API.

    >>> lpp.so3_exp([0.0, 0.0, 0.1]).shape      # one element
    (3, 3)
    >>> lpp.so3_exp(np.zeros((100, 3))).shape   # a stack, same function
    (100, 3, 3)

Operators also take ``out=`` to write into an array you already own, which keeps hot loops
allocation-free.
"""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

try:
    from ._core import (
        SE3,
        SE3_2,
        SO3,
        LieGroup,
        se3_compose,
        se3_exp,
        se3_inv,
        se3_log,
        se3_retract,
        se3_transform,
        so3_compose,
        so3_exp,
        so3_inv,
        so3_inv_right_jacobian,
        so3_log,
        so3_retract,
        so3_right_jacobian,
        so3_rotate,
    )
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

__all__ = [
    "SE3",
    "SE3_2",
    "SO3",
    "LieGroup",
    "__version__",
    # array operators -- SE(3)
    "se3_compose",
    "se3_exp",
    "se3_inv",
    "se3_log",
    "se3_retract",
    "se3_transform",
    # array operators -- SO(3)
    "so3_compose",
    "so3_exp",
    "so3_inv",
    "so3_inv_right_jacobian",
    "so3_log",
    "so3_retract",
    "so3_right_jacobian",
    "so3_rotate",
]

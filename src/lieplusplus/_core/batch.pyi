"""
Vectorized Lie-group operators.

Every function takes C-contiguous float64 arrays shaped (N, *element) and returns
(N, *element). The maths is identical to the scalar API; only the number of
Python->C++ crossings differs (one per array, not one per entity).
"""
from __future__ import annotations
import numpy
import numpy.typing
import typing
__all__: list[str] = ['se3_compose', 'se3_exp', 'se3_inv', 'se3_log', 'se3_retract', 'se3_transform', 'so3_compose', 'so3_exp', 'so3_inv', 'so3_inv_right_jacobian', 'so3_log', 'so3_retract', 'so3_right_jacobian', 'so3_rotate']
def se3_compose(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Group composition A*B, (N,4,4) x (N,4,4) -> (N,4,4).
    
    Shapes: (4, 4) or (N, 4, 4) x (4, 4) or (N, 4, 4) -> (4, 4) or (N, 4, 4)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def se3_exp(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Exponential map, (N,6) -> (N,4,4).
    
    Shapes: (6) or (N, 6) -> (4, 4) or (N, 4, 4)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def se3_inv(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Inverse pose, (N,4,4) -> (N,4,4).
    
    Shapes: (4, 4) or (N, 4, 4) -> (4, 4) or (N, 4, 4)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def se3_log(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Logarithmic map, (N,4,4) -> (N,6).
    
    Shapes: (4, 4) or (N, 4, 4) -> (6) or (N, 6)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def se3_retract(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Right retraction T*exp(u), (N,4,4) x (N,6) -> (N,4,4).
    
    Shapes: (4, 4) or (N, 4, 4) x (6) or (N, 6) -> (4, 4) or (N, 4, 4)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def se3_transform(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Apply a pose to points, (N,4,4) x (N,3) -> (N,3). The frame-change primitive.
    
    Shapes: (4, 4) or (N, 4, 4) x (3) or (N, 3) -> (3) or (N, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def so3_compose(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Group composition A*B, (N,3,3) x (N,3,3) -> (N,3,3).
    
    Shapes: (3, 3) or (N, 3, 3) x (3, 3) or (N, 3, 3) -> (3, 3) or (N, 3, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def so3_exp(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Exponential map, (N,3) -> (N,3,3).
    
    Shapes: (3) or (N, 3) -> (3, 3) or (N, 3, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def so3_inv(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Inverse, (N,3,3) -> (N,3,3).
    
    Shapes: (3, 3) or (N, 3, 3) -> (3, 3) or (N, 3, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def so3_inv_right_jacobian(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Inverse right Jacobian, (N,3) -> (N,3,3).
    
    Shapes: (3) or (N, 3) -> (3, 3) or (N, 3, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def so3_log(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Logarithmic map, (N,3,3) -> (N,3).
    
    Shapes: (3, 3) or (N, 3, 3) -> (3) or (N, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def so3_retract(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Right retraction R*exp(u), (N,3,3) x (N,3) -> (N,3,3). The integration primitive.
    
    Shapes: (3, 3) or (N, 3, 3) x (3) or (N, 3) -> (3, 3) or (N, 3, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def so3_right_jacobian(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Right Jacobian, (N,3) -> (N,3,3).
    
    Shapes: (3) or (N, 3) -> (3, 3) or (N, 3, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """
def so3_rotate(x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], y: typing.Annotated[numpy.typing.ArrayLike, numpy.float64], out: typing.Any = None) -> numpy.ndarray:
    """
    Rotate vectors, (N,3,3) x (N,3) -> (N,3).
    
    Shapes: (3, 3) or (N, 3, 3) x (3) or (N, 3) -> (3) or (N, 3)
    Pass one element or a stack; the result matches. `out=` writes in place.
    """

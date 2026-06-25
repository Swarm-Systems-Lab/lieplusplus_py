"""
Python bindings for Lie++ library
"""
from __future__ import annotations
import collections.abc
import numpy
import numpy.typing
import typing
__all__: list[str] = ['LieGroup', 'SE3', 'SE3_2', 'SO3']
class LieGroup:
    """
    
                LieGroup - Abstract base class for all Lie groups
    
                All Lie groups should implement the following methods:
                - exp(): Exponential map from Lie algebra to Lie group
                - log(): Logarithmic map from Lie group to Lie algebra
                - wedge(): Wedge operator from R^n to Lie algebra
                - vee(): Vee operator from Lie algebra to R^n
                - adjoint(): Adjoint operator
                - random(): Generate a random group element
                - tangent_zero(): Zero element of the Lie algebra
                - __mul__(): Group composition
                - __call__(): Convert to matrix representation
            
    """
class SE3(LieGroup):
    @staticmethod
    def exp(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[6, 1]"]) -> SE3:
        """
        Exponential map: se(3) -> SE(3)
        """
    @staticmethod
    def log(T: SE3) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 1]"]:
        """
        Logarithmic map: SE(3) -> se(3)
        """
    @staticmethod
    def random() -> SE3:
        """
        Generate a random SE3 pose (rotation + translation)
        """
    @staticmethod
    def tangent_zero() -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 1]"]:
        """
        Zero element of se(3).
        """
    @staticmethod
    def vee(U: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[4, 4]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 1]"]:
        """
        Vee operator: se(3) -> R6
        """
    @staticmethod
    def wedge(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[6, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[4, 4]"]:
        """
        Wedge operator: R6 -> se(3)
        """
    def Adjoint(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 6]"]:
        """
        Return Adjoint matrix
        """
    def R(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Return rotation part
        """
    def __call__(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[4, 4]"]:
        """
        Call operator to get the pose matrix (4x4).
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor (identity pose)
        """
    @typing.overload
    def __init__(self, R: SO3, t: typing.Annotated[collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], "FixedSize(1)"]) -> None:
        """
        Constructor from rotation and translation array
        """
    @typing.overload
    def __init__(self, T: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[4, 4]"]) -> None:
        """
        Constructor from 4x4 transformation matrix
        """
    @typing.overload
    def __init__(self, R: SO3, t: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> None:
        """
        Constructor from rotation and translation vector
        """
    @typing.overload
    def __init__(self, R: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 3]"], t: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> None:
        """
        Constructor from rotation matrix and translation vector
        """
    @typing.overload
    def __init__(self, R: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], t: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> None:
        """
        Constructor from rotation vector (exponential map) and translation vector
        """
    @typing.overload
    def __mul__(self, other: SE3) -> SE3:
        """
        Compose poses
        """
    @typing.overload
    def __mul__(self, point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        Transform point
        """
    def __repr__(self) -> str:
        ...
    def asMatrix(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[4, 4]"]:
        """
        Return 4x4 transformation matrix
        """
    def inv(self) -> SE3:
        """
        Return inverse pose
        """
    def q(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[4, 1]"]:
        """
        Return rotation quaternion as [w, x, y, z]
        """
    def t(self) -> typing.Annotated[list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]], "FixedSize(1)"]:
        """
        Return translation array
        """
    def translation(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        Return translation vector
        """
class SE3_2(LieGroup):
    @staticmethod
    def exp(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[9, 1]"]) -> SE3_2:
        """
        Exponential map: se_2(3) -> SE_2(3)
        """
    @staticmethod
    def log(T: SE3_2) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[9, 1]"]:
        """
        Logarithmic map: SE_2(3) -> se_2(3)
        """
    @staticmethod
    def random() -> SE3_2:
        """
        Generate a random SE3_2 pose (rotation + velocity + position)
        """
    @staticmethod
    def tangent_zero() -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[9, 1]"]:
        """
        Zero element of se_2(3).
        """
    @staticmethod
    def vee(U: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[5, 5]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[9, 1]"]:
        """
        Vee operator: se_2(3) -> R9
        """
    @staticmethod
    def wedge(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[9, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[5, 5]"]:
        """
        Wedge operator: R9 -> se_2(3)
        """
    def Adjoint(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[9, 9]"]:
        """
        Return Adjoint matrix
        """
    def R(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Return rotation part
        """
    def __call__(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[5, 5]"]:
        """
        Call operator to get the extended pose matrix (5x5).
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor (identity extended pose)
        """
    @typing.overload
    def __init__(self, R: SO3, t: typing.Annotated[collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], "FixedSize(2)"]) -> None:
        """
        Constructor from rotation and translation array [velocity, position]
        """
    @typing.overload
    def __init__(self, R: SO3, translations: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        """
        Constructor from rotation and translation vectors [velocity, position]
        """
    def __mul__(self, other: SE3_2) -> SE3_2:
        """
        Compose extended poses
        """
    def __repr__(self) -> str:
        ...
    def asMatrix(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[5, 5]"]:
        """
        Return 5x5 extended pose matrix
        """
    def inv(self) -> SE3_2:
        """
        Return inverse extended pose
        """
    def p(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        Return position vector
        """
    def q(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[4, 1]"]:
        """
        Return rotation quaternion as [w, x, y, z]
        """
    def t(self) -> typing.Annotated[list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]], "FixedSize(2)"]:
        """
        Return translation array
        """
    def v(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        Return velocity vector
        """
class SO3(LieGroup):
    @staticmethod
    def Gamma2(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Gamma2 matrix for SO(3).
        """
    @staticmethod
    def adjoint(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Adjoint operator for so(3). Returns a 3x3 matrix.
        """
    @staticmethod
    def exp(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> SO3:
        """
        Exponential map R^3 -> SO(3).
        """
    @staticmethod
    def invLeftJacobian(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Inverse Left Jacobian of SO(3). Returns a 3x3 matrix.
        """
    @staticmethod
    def invRightJacobian(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Inverse Right Jacobian. Returns a 3x3 matrix.
        """
    @staticmethod
    def leftJacobian(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Left Jacobian of SO(3). Returns a 3x3 matrix.
        """
    @staticmethod
    def log(X: SO3) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        Logarithmic map SO(3) -> R^3.
        """
    @staticmethod
    def random() -> SO3:
        """
        Generate a random SO(3) rotation.
        """
    @staticmethod
    def rightJacobian(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Right Jacobian (leftJacobian(-u)). Returns a 3x3 matrix.
        """
    @staticmethod
    def tangent_zero() -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        Zero element of so(3).
        """
    @staticmethod
    def vee(U: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 3]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        Vee operator so(3) -> R^3. Returns a 3-vector.
        """
    @staticmethod
    def wedge(u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Wedge operator R^3 -> so(3). Returns a 3x3 matrix.
        """
    def Adjoint(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Return the Adjoint matrix (3x3).
        """
    def R(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Return the rotation matrix (3x3).
        """
    def __call__(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Call operator to get the rotation matrix (3x3).
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor (identity rotation)
        """
    @typing.overload
    def __init__(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[4, 1]"]) -> None:
        """
        Constructor from quaternion [w, x, y, z].
        """
    @typing.overload
    def __init__(self, R: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 3]"]) -> None:
        """
        Constructor from rotation matrix
        """
    @typing.overload
    def __init__(self, u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> None:
        """
        Constructor from rotation vector (exponential map)
        """
    @typing.overload
    def __init__(self, u: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], v: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> None:
        """
        Constructor from two vectors u, v such that R * u = v
        """
    @typing.overload
    def __mul__(self, other: SO3) -> SO3:
        """
        Compose with another SO3.
        """
    @typing.overload
    def __mul__(self, matrix: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 3]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Apply rotation to a 3x3 matrix.
        """
    @typing.overload
    def __mul__(self, vector: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        Rotate a 3-vector.
        """
    @typing.overload
    def __mul__(self, vectors: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, n]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, n]"]:
        """
        Apply rotation to an array of 3-vectors (3xN matrix).
        """
    def __repr__(self) -> str:
        ...
    def asMatrix(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Return the rotation as a 3x3 matrix.
        """
    def fromR(self, R: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 3]"]) -> None:
        """
        Set this rotation from a rotation matrix.
        """
    def fromq(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[4, 1]"]) -> None:
        """
        Set this rotation from a (normalized) quaternion [w, x, y, z].
        """
    def inv(self) -> SO3:
        """
        Return the inverse rotation (SO(3)).
        """
    def invAdjoint(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        """
        Return the inverse Adjoint matrix (3x3).
        """
    def multiplyLeft(self, other: SO3) -> SO3:
        """
        In-place multiplication: self = other * self. Returns self.
        """
    def multiplyRight(self, other: SO3) -> SO3:
        """
        In-place multiplication: self = self * other. Returns self.
        """
    def q(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[4, 1]"]:
        """
        Return quaternion as [w, x, y, z].
        """
__version__: str = '0.5.2'

#!/usr/bin/env python3
"""
Basic usage example for lieplusplus-py
"""

import numpy as np

import lieplusplus as lpp


def so3_example():
    """Example usage of SO(3) rotations"""

    # Create identity rotation
    lpp.SO3()

    # Create rotation from axis-angle
    axis_angle = np.array([0.1, 0.2, 0.3])
    R = lpp.SO3.exp(axis_angle)

    # Compose rotations
    R_random = lpp.SO3.random()
    R * R_random

    # Rotate a vector
    v = np.array([1.0, 0.0, 0.0])
    R * v

    # Test inverse
    R_inv = R.inv()
    R * R_inv


def se3_example():
    """Example usage of SE(3) poses"""

    # Create identity pose
    lpp.SE3()

    # Create pose from rotation and translation
    R = lpp.SO3.exp(np.array([0.1, 0.0, 0.1]))
    t = np.array([1.0, 2.0, 3.0])
    T = lpp.SE3(R, t)

    # Compose poses
    T_random = lpp.SE3.random()
    T * T_random

    # Transform a point
    p = np.array([1.0, 0.0, 0.0])
    T * p


def se23_example():
    """Example usage of SE_2(3) extended poses"""

    # Create identity extended pose
    lpp.SE3_2()

    # Create extended pose with velocity and position
    R = lpp.SO3()  # identity rotation
    v = np.array([0.1, 0.1, 0.3])  # velocity
    p = np.array([1.0, 2.0, 3.0])  # position
    X = lpp.SE3_2(R, [v, p])


    # Random extended pose via exponential map
    xi = np.random.randn(9)  # 9-dimensional tangent space
    X_random = lpp.SE3_2.exp(xi)

    # Compose extended poses
    X * X_random

    # Test exp/log consistency
    lpp.SE3_2.log(X_random)


def adjoint_example():
    """Example of Adjoint matrices"""

    # SO(3) Adjoint
    R = lpp.SO3.exp(np.array([0.1, 0.2, 0.3]))
    R.Adjoint()

    # SE(3) Adjoint
    T = lpp.SE3.random()
    T.Adjoint()

    # SE_2(3) Adjoint
    X = lpp.SE3_2.random()
    X.Adjoint()


if __name__ == "__main__":

    so3_example()
    se3_example()
    se23_example()
    adjoint_example()


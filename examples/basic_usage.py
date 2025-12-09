#!/usr/bin/env python3
"""
Basic usage example for lieplusplus-py
"""
import numpy as np
import lieplusplus as lpp


def so3_example():
    """Example usage of SO(3) rotations"""
    print("=== SO(3) Rotation Group Example ===")
    
    # Create identity rotation
    R_identity = lpp.SO3()
    print(f"Identity rotation matrix:\n{R_identity.asMatrix()}")
    
    # Create rotation from axis-angle
    axis_angle = np.array([0.1, 0.2, 0.3])
    R = lpp.SO3.exp(axis_angle)
    print(f"\nRotation from axis-angle {axis_angle}:")
    print(f"Rotation matrix:\n{R.asMatrix()}")
    print(f"Quaternion: {R.q()}")
    
    # Compose rotations
    R_random = lpp.SO3.random()
    R_composed = R * R_random
    print(f"\nComposed rotation matrix:\n{R_composed.asMatrix()}")
    
    # Rotate a vector
    v = np.array([1.0, 0.0, 0.0])
    v_rotated = R * v
    print(f"\nOriginal vector: {v}")
    print(f"Rotated vector: {v_rotated}")
    
    # Test inverse
    R_inv = R.inv()
    should_be_identity = R * R_inv
    print(f"\nR * R^-1 (should be identity):\n{should_be_identity.asMatrix()}")


def se3_example():
    """Example usage of SE(3) poses"""
    print("\n\n=== SE(3) Pose Group Example ===")
    
    # Create identity pose
    T_identity = lpp.SE3()
    print(f"Identity pose matrix:\n{T_identity.asMatrix()}")
    
    # Create pose from rotation and translation
    R = lpp.SO3.exp(np.array([0.1, 0.0, 0.1]))
    t = np.array([1.0, 2.0, 3.0])
    T = lpp.SE3(R, t)
    print(f"\nPose from R and t:")
    print(f"Transformation matrix:\n{T.asMatrix()}")
    print(f"Rotation part:\n{T.R()}")
    print(f"Translation part: {T.translation()}")
    
    # Compose poses
    T_random = lpp.SE3.random()
    T_composed = T * T_random
    print(f"\nComposed pose matrix:\n{T_composed.asMatrix()}")
    
    # Transform a point
    p = np.array([1.0, 0.0, 0.0])
    p_transformed = T * p
    print(f"\nOriginal point: {p}")
    print(f"Transformed point: {p_transformed}")


def se23_example():
    """Example usage of SE_2(3) extended poses"""
    print("\n\n=== SE_2(3) Extended Pose Group Example ===")
    
    # Create identity extended pose
    X_identity = lpp.SE3_2()
    print(f"Identity extended pose matrix:\n{X_identity.asMatrix()}")
    
    # Create extended pose with velocity and position
    R = lpp.SO3()  # identity rotation
    v = np.array([0.1, 0.1, 0.3])  # velocity
    p = np.array([1.0, 2.0, 3.0])  # position
    X = lpp.SE3_2(R, [v, p])
    
    print(f"\nExtended pose from R, v, p:")
    print(f"Extended pose matrix:\n{X.asMatrix()}")
    print(f"Rotation (quaternion): {X.q()}")
    print(f"Velocity: {X.v()}")
    print(f"Position: {X.p()}")
    
    # Random extended pose via exponential map
    xi = np.random.randn(9)  # 9-dimensional tangent space
    X_random = lpp.SE3_2.exp(xi)
    print(f"\nRandom extended pose from exp(xi):")
    print(f"xi: {xi}")
    print(f"X matrix:\n{X_random.asMatrix()}")
    
    # Compose extended poses
    X_composed = X * X_random
    print(f"\nComposed extended pose matrix:\n{X_composed.asMatrix()}")
    
    # Test exp/log consistency
    xi_recovered = lpp.SE3_2.log(X_random)
    print(f"\nOriginal xi: {xi}")
    print(f"Recovered xi: {xi_recovered}")
    print(f"Difference: {np.linalg.norm(xi - xi_recovered)}")


def adjoint_example():
    """Example of Adjoint matrices"""
    print("\n\n=== Adjoint Matrices Example ===")
    
    # SO(3) Adjoint
    R = lpp.SO3.exp(np.array([0.1, 0.2, 0.3]))
    Ad_R = R.Adjoint()
    print(f"SO(3) Adjoint matrix:\n{Ad_R}")
    
    # SE(3) Adjoint  
    T = lpp.SE3.random()
    Ad_T = T.Adjoint()
    print(f"\nSE(3) Adjoint matrix:\n{Ad_T}")
    
    # SE_2(3) Adjoint
    X = lpp.SE3_2.random()
    Ad_X = X.Adjoint()
    print(f"\nSE_2(3) Adjoint matrix:\n{Ad_X}")


if __name__ == "__main__":
    print("Lie++ Python Bindings Example")
    print("=" * 50)
    
    so3_example()
    se3_example() 
    SE3_2_example()
    adjoint_example()
    
    print("\n\nExample completed successfully!")
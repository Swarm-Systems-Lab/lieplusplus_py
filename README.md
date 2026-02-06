# Lie++ Python Bindings

Python bindings for the [Lie++ C++ library](https://github.com/jesusBV20/Lie-plusplus), providing efficient operations on Lie groups commonly used in robotics and computer vision.

> **Warning — AI-generated content:** This README was largely generated with the
> help of an AI assistant. While we strive for accuracy, please verify critical
> details (installation steps, API contract, and examples) before relying on them
> in production.

## Features

- **SO(3)**: 3D rotation group
- **SE(3)**: Special Euclidean group (pose: rotation + translation)
- **SE_2(3)**: Extended Special Euclidean group (pose + velocity)
- NumPy integration for seamless array operations
- High-performance C++ implementation with Python convenience
- Comprehensive test suite and examples

## Requirements

- Python 3.10+

## Quick Start

```bash
pip install lieplusplus-py
```

```python
import numpy as np
from lieplusplus import SO3, SE3

# Create a 3D rotation from axis-angle (exponential map)
R = SO3.exp(np.array([0.1, 0.2, 0.3]))
print(R.asMatrix())

# Create a 3D pose from a 6D twist
T = SE3.exp(np.array([0.1, 0.2, 0.3, 1.0, 2.0, 3.0]))
print(T.asMatrix())
```

## Architecture (short)

- Python layer: user-facing API with type hints and convenience helpers.
- C++ bindings: pybind11 exposes Lie++ classes efficiently to Python.
- Core: the Lie++ C++ library provides mathematical implementations; Eigen3 is
   used for linear algebra.

## Use Cases

- Robotics: kinematics, motion planning, state estimation.
- Computer vision: SLAM and structure-from-motion.
- Research and optimization on manifolds.

## Lie++ Python API Documentation

### SO(3) - 3D Rotations

```python
import numpy as np
from lieplusplus import SO3

# --- Constructors ---
R = SO3()                               # Identity rotation
R = SO3([1, 0, 0, 0])                   # Quaternion [w, x, y, z]
R = SO3(np.eye(3))                      # Rotation matrix (3×3)
R = SO3([0.1, 0.2, 0.3])                # Rotation vector (exp map)
R = SO3([1, 0, 0], [0, 1, 0])           # Rotation sending u → v
R = SO3.random()                        # Random rotation

# --- Group operations ---
R3 = R1 * R2         # Compose rotations
v_rot = R * v        # Rotate a 3-vector
M_rot = R * M        # Rotate a 3×3 matrix

# --- Lie-theoretic operations (static) ---
u  = SO3.log(R)          # R^3 log-coordinate
R2 = SO3.exp(u)          # Exponential map
U  = SO3.wedge(u)        # 3×3 skew-symmetric matrix
u2 = SO3.vee(U)          # Vector from skew matrix
u0 = SO3.tangent_zero()  # Zero element of so(3)

# --- Jacobians ---
J    = SO3.leftJacobian(u)
Jinv = SO3.invLeftJacobian(u)

# --- Accessors ---
R.asMatrix()      # 3×3 rotation matrix
R.Adjoint()       # 3×3 Adjoint matrix
R.inv()           # Inverse rotation
R.q()             # Quaternion [w, x, y, z]
```

### SE(3) - Poses

```python
import numpy as np
from lieplusplus import SE3, SO3

# --- Constructors ---
T = SE3()                                 # Identity pose
T = SE3(R, t)                             # SO(3) + translation vector
T = SE3(np.eye(4))                        # Full 4×4 pose matrix
T = SE3([0.1, 0.2, 0.3], [1, 2, 3])       # Rotation vector + translation
T = SE3.random()                          # Random pose

# --- Group operations ---
T3 = T1 * T2       # Compose poses
p_world = T * p    # Transform a 3D point

# --- Lie-theoretic operations (static) ---
u  = SE3.log(T)        # R^6 tangent vector
T2 = SE3.exp(u)
U  = SE3.wedge(u)
u2 = SE3.vee(U)
u0 = SE3.tangent_zero()

# --- Accessors ---
T.asMatrix()       # 4×4 transformation matrix
T.Adjoint()        # 6×6 Adjoint matrix
T.inv()            # Inverse pose
T.R()              # Rotation (SO3)
T.q()              # Quaternion
T.translation()    # 3D translation vector

```

### SE_2(3) - Extended Poses

```python
import numpy as np
from lieplusplus import SE3_2, SO3

# --- Constructors ---
X = SE3_2()                               # Identity extended pose
X = SE3_2(R, [v, p])                      # Rotation + [velocity, position]
X = SE3_2(R, [np.zeros(3), np.ones(3)])   # Example
X = SE3_2.random()                        # Random extended pose

# --- Group operations ---
X3 = X1 * X2

# --- Lie-theoretic operations (static) ---
u  = SE3_2.log(X)       # R^9 tangent vector
X2 = SE3_2.exp(u)
U  = SE3_2.wedge(u)
u2 = SE3_2.vee(U)
u0 = SE3_2.tangent_zero()

# --- Accessors ---
X.asMatrix()    # 5×5 extended matrix
X.Adjoint()     # 9×9 Adjoint matrix
X.inv()         # Inverse extended pose
X.R()           # Rotation (SO3)
X.v()           # Velocity vector
X.p()           # Position vector
```

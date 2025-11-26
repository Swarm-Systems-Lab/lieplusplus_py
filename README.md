# Lie++ Python Bindings

Python bindings for the [Lie++ C++ library](https://github.com/jesusBV20/Lie-plusplus), providing efficient operations on Lie groups commonly used in robotics and computer vision.

## Features

- **SO(3)**: 3D rotation group
- **SE(3)**: Special Euclidean group (pose: rotation + translation)  
- **SE_2(3)**: Extended Special Euclidean group (pose + velocity)
- NumPy integration for seamless array operations
- High-performance C++ implementation with Python convenience
- Comprehensive test suite and examples

## Installation

### From Source

   ```bash
   git clone https://github.com/Swarm-Systems-Lab/lieplusplus_py.git
   cd lieplusplus_py
   pip install -e .
   ```
   Alternatively, for a development installation (includes testing and formatting tools):
   ```bash
   pip install -e .[dev]
   ```

### Requirements

- Python 3.8+
- NumPy
- pybind11
- C++17 compatible compiler
- Eigen3 (automatically downloaded during the build)

## API Reference

### SO(3) - 3D Rotations

```python
# Constructors
R = lpp.SO3()                    # Identity
R = lpp.SO3.exp(axis_angle)      # From axis-angle vector
R = lpp.SO3.random()             # Random rotation

# Operations
R1 * R2                          # Composition
R.inverse()                      # Inverse rotation
R * vector                       # Rotate vector
R.asMatrix()                     # Get 3x3 matrix
R.q()                            # Get quaternion
R.Adjoint()                      # Adjoint matrix
```

### SE(3) - Poses

```python
# Constructors  
T = lpp.SE3()                    # Identity pose
T = lpp.SE3(R, t)                # From rotation and translation
T = lpp.SE3.exp(xi)              # From se(3) vector (6D)
T = lpp.SE3.random()             # Random pose

# Operations
T1 * T2                          # Pose composition
T.inverse()                      # Inverse pose
T * point                        # Transform point
T.asMatrix()                     # Get 4x4 matrix
T.R()                            # Get SO(3) rotation part as a 3x3 matrix
T.translation()                  # Get translation vector
T.Adjoint()                      # 6x6 Adjoint matrix
```

### SE_2(3) - Extended Poses

```python
# Constructors
X = lpp.SE23()                   # Identity extended pose  
X = lpp.SE23(R, [v, p])          # From rotation, velocity, position
X = lpp.SE23.exp(xi)             # From se_2(3) vector (9D)
X = lpp.SE23.random()            # Random extended pose

# Operations
X1 * X2                          # Extended pose composition
X.inverse()                      # Inverse
X.asMatrix()                     # Get 5x5 matrix
X.R()                            # Get SO(3) part as a 3x3 matrix
X.v()                            # Get velocity vector
X.p()                            # Get position vector  
X.Adjoint()                      # 9x9 Adjoint matrix
```
# Usage Guide

This guide provides an overview of how to use lieplusplus_py for common tasks.

## Installation

```bash
pip install lieplusplus-py
```

## Basic Concepts

lieplusplus_py provides three main Lie groups:

- **SO(3)**: Rotations in 3D space
- **SE(3)**: Rigid body transformations (rotation + translation)
- **SE₂(3)**: Extended transformations (rotation + translation + velocity)

All classes inherit from `LieGroup` and support common operations.

## Core Operations

### Creating Transformations

```python
import lieplusplus as lie
import numpy as np

# Identity elements
R = lie.SO3()  # Identity rotation
T = lie.SE3()  # Identity pose

# From exponential map
omega = np.array([0.1, 0.2, 0.3])  # Rotation vector
R = lie.SO3.exp(omega)

xi = np.array([0.1, 0.2, 0.3, 1.0, 2.0, 3.0])  # 6D twist
T = lie.SE3.exp(xi)
```

### Composition and Inversion

```python
# Compose transformations
T1 = lie.SE3.exp(np.array([0, 0, 0, 1, 0, 0]))  # Translation
T2 = lie.SE3.exp(np.array([0.1, 0, 0, 0, 0, 0]))  # Rotation
T_composed = T1 * T2

# Inverse
T_inv = T.inv()
```

### Applying Transformations

```python
# Transform points
point = np.array([1.0, 2.0, 3.0])
transformed = T * point

# Transform other transformations
T_relative = T1 * T2.inv()
```

## Advanced Features

### Jacobians and Derivatives

```python
# Left Jacobian of SO(3)
J = lie.SO3.left_jacobian(omega)

# Right Jacobian
J_right = lie.SO3.right_jacobian(omega)
```

### Adjoint Matrices

```python
# For computing derivatives through composition
adj = T.Adjoint()
```

## Integration Patterns

### With NumPy

```python
# Vectorized operations
omegas = np.random.randn(10, 3)
rotations = [lie.SO3.exp(omega) for omega in omegas]

# Batch processing
points = np.random.randn(100, 3)
transformed_points = np.array([T * p for p in points])
```

### With Optimization Libraries

```python
import scipy.optimize

def cost_function(xi):
    T = lie.SE3.exp(xi)
    # Compute cost based on T
    return cost

# Optimize in tangent space
result = scipy.optimize.minimize(cost_function, np.zeros(6))
optimal_T = lie.SE3.exp(result.x)
```

## Best Practices

1. **Use exponential/logarithm**: Work in tangent space for optimization
2. **Batch operations**: Process multiple transformations together
3. **Type consistency**: Use consistent NumPy dtypes (float64 recommended)
4. **Validation**: Check mathematical properties in tests

## Common Patterns

- **Kinematics**: Chain transformations for forward kinematics
- **SLAM**: Compose poses for trajectory estimation
- **Calibration**: Optimize transformations between coordinate frames
- **Motion planning**: Interpolate in tangent space

See [Examples](examples.md) for detailed code samples.

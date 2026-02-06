# Examples

This page provides practical examples of using lieplusplus_py for common Lie group operations. All examples assume you have installed the package and imported it:

```python
import numpy as np
import lieplusplus as lie
```

## SO(3) Rotations

SO(3) represents 3D rotations. Here's how to work with rotations:

```python
# Create identity rotation
R_id = lie.SO3()

# Create rotation from axis-angle (exponential map)
axis_angle = np.array([0.1, 0.2, 0.3])
R = lie.SO3.exp(axis_angle)

# Create random rotation
R_rand = lie.SO3.random()

# Compose rotations
R_composed = R * R_rand

# Rotate a vector
v = np.array([1.0, 0.0, 0.0])
v_rotated = R * v

# Get rotation matrix
matrix = R.matrix()

# Compute inverse
R_inv = R.inv()

# Verify inverse property
identity = R * R_inv  # Should be close to identity
```

## SE(3) Poses

SE(3) represents 3D rigid body transformations (rotation + translation):

```python
# Create identity pose
T_id = lie.SE3()

# Create pose from rotation and translation
R = lie.SO3.exp(np.array([0.1, 0.0, 0.1]))
t = np.array([1.0, 2.0, 3.0])
T = lie.SE3(R, t)

# Create random pose
T_rand = lie.SE3.random()

# Compose poses
T_composed = T * T_rand

# Transform a point
p = np.array([1.0, 0.0, 0.0])
p_transformed = T * p

# Get transformation matrix (4x4)
matrix = T.matrix()

# Access rotation and translation components
rotation = T.rotation()
translation = T.translation()
```

## SE₂(3) Extended Poses

SE₂(3) extends SE(3) with velocity information:

```python
# Create identity extended pose
X_id = lie.SE3_2()

# Create extended pose with rotation, velocity, and position
R = lie.SO3()
v = np.array([0.1, 0.1, 0.3])  # velocity
p = np.array([1.0, 2.0, 3.0])  # position
X = lie.SE3_2(R, [v, p])

# Create from exponential map (9D tangent vector)
xi = np.random.randn(9)
X_exp = lie.SE3_2.exp(xi)

# Compose extended poses
X_rand = lie.SE3_2.random()
X_composed = X * X_rand

# Get logarithm (tangent space)
xi_back = lie.SE3_2.log(X_exp)
```

## Adjoint Matrices

Adjoint matrices are useful for computing Jacobians in optimization:

```python
# SO(3) adjoint (3x3 matrix)
R = lie.SO3.exp(np.array([0.1, 0.2, 0.3]))
adj_so3 = R.Adjoint()

# SE(3) adjoint (6x6 matrix)
T = lie.SE3.random()
adj_se3 = T.Adjoint()

# SE₂(3) adjoint (9x9 matrix)
X = lie.SE3_2.random()
adj_se23 = X.Adjoint()
```

## Advanced Usage

Advanced examples can be found in the `examples/` directory of the repository.

### Numerical Stability

All operations are numerically stable and include proper handling of edge cases like near-singular matrices.

### Performance Tips

- Use NumPy arrays for vectorized operations
- Compose transformations rather than applying sequentially when possible
- The C++ backend ensures high performance for computationally intensive tasks

### Integration with Other Libraries

lieplusplus_py works seamlessly with other scientific Python libraries:

```python
import matplotlib.pyplot as plt

# Visualize rotation matrices
R = lie.SO3.exp(np.array([1.0, 0.0, 0.0]))
plt.imshow(R.matrix())
plt.show()
```

## Running the packaged examples

The examples in `examples/` are small smoke tests demonstrating basic usage. To run the `basic_usage.py` example (no output expected on success):

```bash
uv run python examples/basic_usage.py
# or, if using venv:
source .venv/bin/activate
python examples/basic_usage.py
```

Expected: The script runs without uncaught exceptions and exits with status 0. If you see import errors, follow the Troubleshooting page to collect build logs.

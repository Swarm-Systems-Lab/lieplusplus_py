# lieplusplus_py

Swarm Systems Lab Python lieplusplus library

⚠️ **Warning:** This project is a work in progress.

## Installation

```bash
pip install lieplusplus_py
```

## Python Lie++ API Documentation

### SO(3) - 3D Rotations

```python
import numpy as np
from lieplusplus import SO3

# --- Constructors ---
R = SO3()                               # Identity rotation
R = SO3([1, 0, 0, 0])                   # Quaternion [w, x, y, z]
R = SO3(np.eye(3))                      # Rotation matrix (3×3)
R = SO3([0.1, 0.2, 0.3])                # Rotation vector (exp map)
R = SO3([1, 0, 0], [0, 1, 0])           # Rotation sending u -> v
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

## Array operators

The group classes above are **object-oriented and single-element by design**: the algebra of one
robot rarely needs vectorization. Calling them from Python in a loop is dominated not by the
arithmetic (tens of nanoseconds) but by the pybind boundary crossing (~1-1.5 us per call), which a
loop over `N` entities pays `N` times.

So the same maths is also exposed as **plain functions on numpy arrays**, crossing into C++ once
per *call*:

```python
import numpy as np
import lieplusplus as lpp

xi = np.random.normal(size=(1000, 3)) * 0.01
R = lpp.so3_exp(xi)                 # (1000, 3, 3)
R = lpp.so3_retract(R, xi)          # R * exp(xi), the integration primitive
```

Measured on SO(3) retraction: **~3 us/entity for a Python loop vs ~0.04 us/entity** (~68x at
N=1000), and faster than an equivalent vectorized NumPy implementation, since the C++ loop
materializes no temporaries.

### One function, any input

There is **no separate batch API to choose**. Each operator is shape-polymorphic, and takes
whatever array you happen to have:

```python
lpp.so3_exp(v)                          # (3,)     -> (3, 3)      one element
lpp.so3_exp(v_stack)                    # (N, 3)   -> (N, 3, 3)   or a stack

lpp.so3_retract(one_R, tangents)        # (3,3) x (N,3) -> (N,3,3)   leading axis broadcasts N vs 1
lpp.so3_retract(R, tangents, out=R)     # writes in place, allocating nothing

lpp.so3_exp(fortran_or_float32_or_list) # any layout/dtype converts - no ascontiguousarray needed
lpp.so3_log(SO3.random())               # group objects work too (via __array__)
```

`out=` accepts **any writable array of the right shape**. A C-contiguous float64 buffer is written
directly (zero copy - the fast path an integrator wants); anything else (an F-ordered array, a
slice, a float32 buffer) goes through a temporary and is copied back, so the result always lands
in your array. It is never silently discarded.

Shape errors name the operator and the argument:

```
so3_exp: argument 'x' must have shape (3) or (N, 3), got (4, 5)
so3_retract: leading dimensions do not broadcast, got 4 and 3
```

### Available operators

| SO(3) | shapes (one element, or `N` of them) |
|---|---|
| `so3_exp` / `so3_log` | `(3,) -> (3,3)` / `(3,3) -> (3,)` |
| `so3_inv` | `(3,3) -> (3,3)` |
| `so3_compose` | `(3,3) x (3,3) -> (3,3)` |
| `so3_retract` | `(3,3) x (3,) -> (3,3)` |
| `so3_rotate` | `(3,3) x (3,) -> (3,)` |
| `so3_right_jacobian` / `so3_inv_right_jacobian` | `(3,) -> (3,3)` |

| SE(3) | shapes (one element, or `N` of them) |
|---|---|
| `se3_exp` / `se3_log` | `(6,) -> (4,4)` / `(4,4) -> (6,)` |
| `se3_inv` | `(4,4) -> (4,4)` |
| `se3_compose` | `(4,4) x (4,4) -> (4,4)` |
| `se3_retract` | `(4,4) x (6,) -> (4,4)` |
| `se3_transform` | `(4,4) x (3,) -> (3,)` |

### Adding an operator

The machinery lives in `src/pybind_batch.hpp` and is **library-agnostic** - it only assumes
fixed-size Eigen types in and out, so it can be dropped into any pybind11 project. Adding an
operator is one line; shape checking, broadcasting, `out=`, layout conversion and error messages
come for free:

```cpp
namespace pb = pybind_batch;

pb::def_unary<Vec3d, Matrix3d>(m, "so3_exp",
    [](const Vec3d& u) { return SO3d::exp(u).asMatrix(); }, "Exponential map.");

pb::def_binary<Matrix3d, Vec3d, Matrix3d>(m, "so3_retract",
    [](const Matrix3d& R, const Vec3d& u) { return (SO3d(R) * SO3d::exp(u)).asMatrix(); },
    "Right retraction R*exp(u).");
```

The element types determine the array shapes: `Vec3d` means `(3,)` or `(N, 3)`, `Matrix4d` means
`(4, 4)` or `(N, 4, 4)`.

> **Note.** The array operators are free functions (`lpp.so3_exp`) rather than methods on the
> classes (`SO3.exp`) because the two have different contracts. `SO3.exp` accepts a `(3,)` vector
> *and* a `(3,1)` column - convenient for one element, but `(3,1)` would be ambiguous with a stack
> of 3 under batching. The free functions are strict about rank instead, which is what lets a
> single name serve one element and a million.


## License

MIT

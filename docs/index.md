# lieplusplus_py

> **Warning — AI-generated content:** This documentation page was largely
> generated with the assistance of an AI. Please verify examples and
> installation instructions before relying on them in critical workflows.

High-performance Python bindings for the Lie++ C++ library, providing efficient operations on Lie groups commonly used in robotics, computer vision, and geometric computing.

## What is lieplusplus_py?

lieplusplus_py brings the power of C++ Lie group mathematics to Python with zero-copy NumPy integration. It supports:

- **SO(3)**: 3D rotations
- **SE(3)**: 3D rigid body transformations (rotation + translation)
- **SE₂(3)**: Extended rigid body transformations (rotation + translation + velocity)

Built on top of the [Lie++](https://github.com/jesusBV20/Lie-plusplus) library, it offers:

- 🚀 **Performance**: C++ speed with Python convenience
- 🔢 **NumPy Integration**: Seamless array operations
- 🧮 **Mathematical Rigor**: Verified group properties and Jacobians
- 🛠️ **Easy Installation**: Automatic dependency management

## Quick Start

```python
import numpy as np
import lieplusplus as lie

# Create a 3D rotation
R = lie.SO3.exp(np.array([0.1, 0.2, 0.3]))
print("Rotation matrix:")
print(R.matrix())

# Create a 3D pose
T = lie.SE3.exp(np.array([0.1, 0.2, 0.3, 1.0, 2.0, 3.0]))
print("Transformation matrix:")
print(T.matrix())

# Compose transformations
T2 = lie.SE3.exp(np.array([0.0, 0.0, 0.0, 0.5, 0.0, 0.0]))
result = T * T2
print("Composed transformation:")
print(result.matrix())
```

## Installation

```bash
pip install lieplusplus-py
```

For development:
```bash
git clone https://github.com/jesusBV20/lieplusplus_py.git
cd lieplusplus_py
uv sync --group dev
pip install -e .
```

## Architecture

lieplusplus_py is built as a hybrid Python/C++ package:

- **Python Layer**: Pure Python interface with type hints and documentation
- **C++ Bindings**: pybind11 generates efficient bindings to Lie++ classes
- **Core Library**: Lie++ provides the mathematical implementations
- **Dependencies**: Eigen3 for linear algebra, automatic fetching if needed

The package uses scikit-build-core for reproducible builds and setuptools-scm for versioning.

## Key Features

- **Group Operations**: Exponentiation, logarithm, composition, inversion
- **Jacobians**: Analytical derivatives for optimization
- **NumPy Compatibility**: All operations work with NumPy arrays
- **Type Safety**: Full type hints and runtime checks
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Use Cases

- **Robotics**: Forward/inverse kinematics, motion planning
- **Computer Vision**: Structure from motion, SLAM
- **Geometric Computing**: Optimization on manifolds
- **Research**: Prototyping geometric algorithms

## Contributing

We welcome contributions! See the [Golden Path](golden-path.md) for development setup and [Contributing](contributing.md) for guidelines.

## License

GPL-3.0-or-later

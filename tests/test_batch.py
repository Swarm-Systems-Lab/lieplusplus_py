"""The generic vectorization layer (pybind_batch.hpp) exposed as lieplusplus batch ops."""

import numpy as np
import pytest

import lieplusplus as lpp
from lieplusplus._core import batch as B


@pytest.fixture
def rng():
    return np.random.default_rng(0)


def _rots(rng, n):
    return B.so3_exp(rng.normal(size=(n, 3)) * 0.3)


# --------------------------------------------------------------------------- correctness
def test_batch_matches_the_scalar_api_elementwise(rng):
    xi = rng.normal(size=(6, 3)) * 0.3
    rot = _rots(rng, 6)
    tan = rng.normal(size=(6, 3)) * 0.1

    assert np.allclose(B.so3_exp(xi), [lpp.SO3.exp(v).asMatrix() for v in xi])
    assert np.allclose(B.so3_log(rot), [np.ravel(lpp.SO3.log(lpp.SO3(r))) for r in rot])
    assert np.allclose(B.so3_inv(rot), [lpp.SO3(r).inv().asMatrix() for r in rot])
    assert np.allclose(
        B.so3_retract(rot, tan),
        [(lpp.SO3(r) * lpp.SO3.exp(t)).asMatrix() for r, t in zip(rot, tan, strict=True)],
    )


def test_se3_operations(rng):
    poses = B.se3_exp(rng.normal(size=(5, 6)) * 0.3)
    points = rng.normal(size=(5, 3))

    assert np.allclose(B.se3_compose(B.se3_inv(poses), poses), np.stack([np.eye(4)] * 5))
    expected = np.einsum("nij,nj->ni", poses[:, :3, :3], points) + poses[:, :3, 3]
    assert np.allclose(B.se3_transform(poses, points), expected)


# --------------------------------------------------------------------------- ergonomics
def test_shape_polymorphism_single_and_batched(rng):
    """One element in, one element out; a stack in, a stack out."""
    v = rng.normal(size=3) * 0.3
    assert B.so3_exp(v).shape == (3, 3)
    assert np.allclose(B.so3_exp(v), lpp.SO3.exp(v).asMatrix())

    assert B.so3_exp(rng.normal(size=(4, 3))).shape == (4, 3, 3)
    assert B.so3_log(B.so3_exp(v)).shape == (3,)


def test_leading_axis_broadcasting(rng):
    """N against 1 pairs a shared element with a stack - no tiling by the caller."""
    rot, tan = _rots(rng, 4), rng.normal(size=(4, 3)) * 0.1

    shared_rot = B.so3_retract(rot[0], tan)
    assert shared_rot.shape == (4, 3, 3)
    assert np.allclose(shared_rot, [(lpp.SO3(rot[0]) * lpp.SO3.exp(t)).asMatrix() for t in tan])

    shared_tan = B.so3_retract(rot, tan[0])
    assert shared_tan.shape == (4, 3, 3)
    assert np.allclose(shared_tan, [(lpp.SO3(r) * lpp.SO3.exp(tan[0])).asMatrix() for r in rot])


def test_out_writes_into_the_given_buffer(rng):
    rot, tan = _rots(rng, 4), rng.normal(size=(4, 3)) * 0.1
    dst = np.zeros((4, 3, 3))

    result = B.so3_retract(rot, tan, out=dst)
    assert np.shares_memory(result, dst)
    assert np.allclose(dst, B.so3_retract(rot, tan))


def test_out_shape_is_validated(rng):
    rot, tan = _rots(rng, 4), rng.normal(size=(4, 3)) * 0.1
    with pytest.raises(ValueError, match="wrong shape"):
        B.so3_retract(rot, tan, out=np.zeros((3, 3, 3)))
    with pytest.raises(ValueError, match="wrong rank"):
        B.so3_retract(rot, tan, out=np.zeros((4, 9)))


def test_any_layout_or_dtype_is_accepted(rng):
    """c_style|forcecast converts on the way in - callers never need ascontiguousarray."""
    xi = rng.normal(size=(4, 3)) * 0.2
    reference = B.so3_exp(xi)

    non_contiguous = rng.normal(size=(4, 10))[:, 2:5]
    assert not non_contiguous.flags["C_CONTIGUOUS"]
    assert B.so3_exp(non_contiguous).shape == (4, 3, 3)  # accepted, not an error

    assert np.allclose(B.so3_exp(np.asfortranarray(xi)), reference)
    assert np.allclose(B.so3_exp(xi.astype(np.float32)), reference, atol=1e-6)
    assert np.allclose(B.so3_exp(xi.tolist()), reference)


# --------------------------------------------------------------------------- errors
def test_shape_errors_name_the_operator_and_argument():
    with pytest.raises(ValueError, match=r"so3_exp: argument 'x' must have shape"):
        B.so3_exp(np.zeros((4, 5)))
    with pytest.raises(ValueError, match=r"se3_transform: argument 'x' must have shape"):
        B.se3_transform(np.zeros((4, 3)), np.zeros((4, 3)))


def test_non_broadcastable_leading_dims_are_rejected(rng):
    with pytest.raises(ValueError, match="do not broadcast"):
        B.so3_retract(_rots(rng, 4), rng.normal(size=(3, 3)))


def test_docstrings_document_the_shapes():
    assert "Shapes:" in B.so3_retract.__doc__
    assert "out=" in B.so3_retract.__doc__

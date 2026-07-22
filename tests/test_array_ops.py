"""The array operators: one function per operation, whatever the shape, layout or dtype."""

import numpy as np
import pytest

import lieplusplus as lpp


@pytest.fixture
def rng():
    return np.random.default_rng(0)


def _rots(rng, n):
    return lpp.so3_exp(rng.normal(size=(n, 3)) * 0.3)


# --------------------------------------------------------------------------- correctness
def test_array_ops_match_the_class_api_elementwise(rng):
    xi = rng.normal(size=(6, 3)) * 0.3
    rot = _rots(rng, 6)
    tan = rng.normal(size=(6, 3)) * 0.1

    assert np.allclose(lpp.so3_exp(xi), [lpp.SO3.exp(v).asMatrix() for v in xi])
    assert np.allclose(lpp.so3_log(rot), [np.ravel(lpp.SO3.log(lpp.SO3(r))) for r in rot])
    assert np.allclose(lpp.so3_inv(rot), [lpp.SO3(r).inv().asMatrix() for r in rot])
    assert np.allclose(
        lpp.so3_retract(rot, tan),
        [(lpp.SO3(r) * lpp.SO3.exp(t)).asMatrix() for r, t in zip(rot, tan, strict=True)],
    )


def test_se3_operations(rng):
    poses = lpp.se3_exp(rng.normal(size=(5, 6)) * 0.3)
    points = rng.normal(size=(5, 3))

    assert np.allclose(lpp.se3_compose(lpp.se3_inv(poses), poses), np.stack([np.eye(4)] * 5))
    expected = np.einsum("nij,nj->ni", poses[:, :3, :3], points) + poses[:, :3, 3]
    assert np.allclose(lpp.se3_transform(poses, points), expected)


# --------------------------------------------------------------------------- ergonomics
def test_shape_polymorphism_single_and_batched(rng):
    """One element in, one element out; a stack in, a stack out - the same function."""
    v = rng.normal(size=3) * 0.3
    assert lpp.so3_exp(v).shape == (3, 3)
    assert np.allclose(lpp.so3_exp(v), lpp.SO3.exp(v).asMatrix())

    assert lpp.so3_exp(rng.normal(size=(4, 3))).shape == (4, 3, 3)
    assert lpp.so3_log(lpp.so3_exp(v)).shape == (3,)


def test_leading_axis_broadcasting(rng):
    """N against 1 pairs a shared element with a stack - no tiling by the caller."""
    rot, tan = _rots(rng, 4), rng.normal(size=(4, 3)) * 0.1

    shared_rot = lpp.so3_retract(rot[0], tan)
    assert shared_rot.shape == (4, 3, 3)
    assert np.allclose(shared_rot, [(lpp.SO3(rot[0]) * lpp.SO3.exp(t)).asMatrix() for t in tan])

    shared_tan = lpp.so3_retract(rot, tan[0])
    assert shared_tan.shape == (4, 3, 3)
    assert np.allclose(shared_tan, [(lpp.SO3(r) * lpp.SO3.exp(tan[0])).asMatrix() for r in rot])


def test_any_layout_or_dtype_is_accepted(rng):
    """Inputs convert on the way in - callers never need ascontiguousarray."""
    xi = rng.normal(size=(4, 3)) * 0.2
    reference = lpp.so3_exp(xi)

    non_contiguous = rng.normal(size=(4, 10))[:, 2:5]
    assert not non_contiguous.flags["C_CONTIGUOUS"]
    assert lpp.so3_exp(non_contiguous).shape == (4, 3, 3)  # accepted, not an error

    assert np.allclose(lpp.so3_exp(np.asfortranarray(xi)), reference)
    assert np.allclose(lpp.so3_exp(xi.astype(np.float32)), reference, atol=1e-6)
    assert np.allclose(lpp.so3_exp(xi.tolist()), reference)


def test_group_objects_are_accepted_as_arrays():
    """__array__ makes the class API and the array API interoperable."""
    rot = lpp.SO3.exp([0.0, 0.0, 0.25])

    assert np.asarray(rot).shape == (3, 3)
    assert np.allclose(np.asarray(rot), rot.asMatrix())
    assert np.allclose(lpp.so3_log(rot), [0.0, 0.0, 0.25])  # object straight into an operator
    assert np.allclose(lpp.so3_compose(rot, rot), lpp.so3_exp([0.0, 0.0, 0.5]))
    assert np.asarray(lpp.SE3.random()).shape == (4, 4)


# --------------------------------------------------------------------------- out=
def test_out_writes_into_the_given_buffer(rng):
    rot, tan = _rots(rng, 4), rng.normal(size=(4, 3)) * 0.1
    dst = np.zeros((4, 3, 3))

    result = lpp.so3_retract(rot, tan, out=dst)
    assert np.shares_memory(result, dst)  # the fast path allocates nothing
    assert np.allclose(dst, lpp.so3_retract(rot, tan))


def test_out_honours_awkward_buffers_instead_of_silently_dropping_the_result(rng):
    """The trap this guards: pybind's caster would CONVERT (copy) a buffer whose layout or dtype
    does not match, the kernel would fill the copy, and the caller's array would never change.
    Every writable buffer is honoured - through a temporary when it must be."""
    rot, tan = _rots(rng, 4), rng.normal(size=(4, 3)) * 0.1
    expected = lpp.so3_retract(rot, tan)

    fortran = np.asfortranarray(np.zeros((4, 3, 3)))
    result = lpp.so3_retract(rot, tan, out=fortran)
    assert np.allclose(fortran, expected)  # the caller's array really was written
    assert np.shares_memory(result, fortran)  # and is what came back

    strided = np.zeros((4, 3, 6))[:, :, :3]
    assert not strided.flags["C_CONTIGUOUS"]
    lpp.so3_retract(rot, tan, out=strided)
    assert np.allclose(strided, expected)

    lower_precision = np.zeros((4, 3, 3), dtype=np.float32)
    lpp.so3_retract(rot, tan, out=lower_precision)
    assert np.allclose(lower_precision, expected, atol=1e-6)


def test_out_in_place_retraction_is_the_integration_primitive(rng):
    """R <- R * exp(u) with no allocation: what a manifold integrator does every tick."""
    rot = _rots(rng, 8)
    tan = rng.normal(size=(8, 3)) * 0.05
    expected = lpp.so3_retract(rot, tan)

    lpp.so3_retract(rot, tan, out=rot)
    assert np.allclose(rot, expected)


def test_out_shape_is_validated(rng):
    rot, tan = _rots(rng, 4), rng.normal(size=(4, 3)) * 0.1
    with pytest.raises(ValueError, match="wrong shape"):
        lpp.so3_retract(rot, tan, out=np.zeros((3, 3, 3)))
    with pytest.raises(ValueError, match="wrong rank"):
        lpp.so3_retract(rot, tan, out=np.zeros((4, 9)))


def test_out_refuses_what_it_cannot_write(rng):
    rot, tan = _rots(rng, 4), rng.normal(size=(4, 3)) * 0.1

    read_only = np.zeros((4, 3, 3))
    read_only.setflags(write=False)
    with pytest.raises(ValueError, match="read-only"):
        lpp.so3_retract(rot, tan, out=read_only)

    with pytest.raises(ValueError, match="numpy array"):
        lpp.so3_retract(rot, tan, out=[[[0.0] * 3] * 3] * 4)


# --------------------------------------------------------------------------- errors
def test_shape_errors_name_the_operator_and_argument():
    with pytest.raises(ValueError, match=r"so3_exp: argument 'x' must have shape"):
        lpp.so3_exp(np.zeros((4, 5)))
    with pytest.raises(ValueError, match=r"se3_transform: argument 'x' must have shape"):
        lpp.se3_transform(np.zeros((4, 3)), np.zeros((4, 3)))


def test_non_broadcastable_leading_dims_are_rejected(rng):
    with pytest.raises(ValueError, match="do not broadcast"):
        lpp.so3_retract(_rots(rng, 4), rng.normal(size=(3, 3)))


def test_docstrings_document_the_shapes():
    assert "Shapes:" in lpp.so3_retract.__doc__
    assert "out=" in lpp.so3_retract.__doc__

import numpy as np
import pytest

import lieplusplus as lpp


class TestSO3:
    """Test cases for SO(3) rotation group"""

    def test_identity(self):
        """Test identity rotation"""
        R = lpp.SO3()
        matrix = R.asMatrix()
        expected = np.eye(3)
        np.testing.assert_allclose(matrix, expected, rtol=1e-10, atol=1e-10)

    def test_random_rotation(self):
        """Test random rotation properties"""
        R = lpp.SO3.random()
        matrix = R.asMatrix()

        # Check orthogonality: R @ R.T = I
        np.testing.assert_allclose(matrix @ matrix.T, np.eye(3), rtol=1e-10, atol=1e-10)

        # Check determinant = 1
        np.testing.assert_allclose(np.linalg.det(matrix), 1.0, rtol=1e-10)

    def test_exp_log_consistency(self):
        """Test exp(log(R)) = R"""
        R = lpp.SO3.random()
        u = lpp.SO3.log(R)
        R_recovered = lpp.SO3.exp(u)

        np.testing.assert_allclose(R.asMatrix(), R_recovered.asMatrix(), rtol=1e-10, atol=1e-10)

    def test_jacobian_consistency(self):
        """Test Jacobian consistency for exp and log"""
        R = lpp.SO3.random()
        u = lpp.SO3.log(R)

        R_Jr = lpp.SO3.rightJacobian(u)
        R_Jr_inv = lpp.SO3.invRightJacobian(u)

        np.testing.assert_allclose(R_Jr @ R_Jr_inv, np.eye(3), rtol=1e-10, atol=1e-10)

    def test_group_operations(self):
        """Test group operations"""
        R1 = lpp.SO3.random()
        R2 = lpp.SO3.random()

        # Test composition
        R12 = R1 * R2
        expected = R1.asMatrix() @ R2.asMatrix()
        np.testing.assert_allclose(R12.asMatrix(), expected, rtol=1e-10, atol=1e-10)

        # Test inv
        R_inv = R1.inv()
        identity = R1 * R_inv
        np.testing.assert_allclose(identity.asMatrix(), np.eye(3), rtol=1e-10, atol=1e-10)


class TestSE3:
    """Test cases for SE(3) pose group"""

    def test_identity(self):
        """Test identity pose"""
        T = lpp.SE3()
        matrix = T.asMatrix()
        expected = np.eye(4)
        np.testing.assert_allclose(matrix, expected, rtol=1e-10, atol=1e-10)

    def test_constructor(self):
        """Test construction from rotation and translation"""
        R = lpp.SO3.random()
        t = np.random.randn(3)
        T = lpp.SE3(R, t)

        matrix = T.asMatrix()
        np.testing.assert_allclose(matrix[:3, :3], R.asMatrix(), rtol=1e-10, atol=1e-10)
        np.testing.assert_allclose(matrix[:3, 3], t, rtol=1e-10, atol=1e-10)
        np.testing.assert_allclose(matrix[3, :], [0, 0, 0, 1], rtol=1e-10, atol=1e-10)

    def test_exp_log_consistency(self):
        """Test exp(log(T)) = T"""
        T = lpp.SE3.random()
        xi = lpp.SE3.log(T)
        T_recovered = lpp.SE3.exp(xi)

        np.testing.assert_allclose(T.asMatrix(), T_recovered.asMatrix(), rtol=1e-10, atol=1e-10)

    def test_group_operations(self):
        """Test group operations"""
        T1 = lpp.SE3.random()
        T2 = lpp.SE3.random()

        # Test composition
        T12 = T1 * T2
        expected = T1.asMatrix() @ T2.asMatrix()
        np.testing.assert_allclose(T12.asMatrix(), expected, rtol=1e-10, atol=1e-10)

        # Test inv
        T_inv = T1.inv()
        identity = T1 * T_inv
        np.testing.assert_allclose(identity.asMatrix(), np.eye(4), rtol=1e-10, atol=1e-10)


class TestSE3_2:
    """Test cases for SE_2(3) extended pose group"""

    def test_identity(self):
        """Test identity extended pose"""
        X = lpp.SE3_2()
        matrix = X.asMatrix()
        expected = np.eye(5)
        np.testing.assert_allclose(matrix, expected, rtol=1e-10, atol=1e-10)

    def test_constructor(self):
        """Test construction from rotation, velocity and position"""
        R = lpp.SO3.random()
        v = np.random.randn(3)
        p = np.random.randn(3)
        X = lpp.SE3_2(R, [v, p])

        # Check rotation part
        np.testing.assert_allclose(X.R(), R.asMatrix(), rtol=1e-10, atol=1e-10)

        # Check velocity and position
        np.testing.assert_allclose(X.v(), v, rtol=1e-10, atol=1e-10)
        np.testing.assert_allclose(X.p(), p, rtol=1e-10, atol=1e-10)

    def test_exp_log_consistency(self):
        """Test exp(log(X)) = X"""
        X = lpp.SE3_2.random()
        xi = lpp.SE3_2.log(X)
        X_recovered = lpp.SE3_2.exp(xi)

        np.testing.assert_allclose(X.asMatrix(), X_recovered.asMatrix(), rtol=1e-10, atol=1e-10)

    def test_group_operations(self):
        """Test group operations"""
        X1 = lpp.SE3_2.random()
        X2 = lpp.SE3_2.random()

        # Test composition
        X12 = X1 * X2
        expected = X1.asMatrix() @ X2.asMatrix()
        np.testing.assert_allclose(X12.asMatrix(), expected, rtol=1e-10, atol=1e-10)

        # Test inv
        X_inv = X1.inv()
        identity = X1 * X_inv
        np.testing.assert_allclose(identity.asMatrix(), np.eye(5), rtol=1e-10, atol=1e-10)


if __name__ == "__main__":
    pytest.main([__file__])

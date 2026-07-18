#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <sstream>
#include <iomanip>

// Include Lie++ headers
#include <groups/SO3.hpp>
#include <groups/SEn3.hpp>

// Generic vectorization layer (library-agnostic; see the header)
#include "pybind_batch.hpp"

namespace py = pybind11;

// Abstract base class for all Lie groups
class LieGroup {
public:
    virtual ~LieGroup() = default;
};

PYBIND11_MODULE(_core, m) {
    m.doc() = "Python bindings for Lie++ library";
    m.attr("__version__") = VERSION;

    // Eigen double types alias
    using Eigen::Matrix3d;
    using Eigen::Matrix4d;
    using Eigen::Quaterniond;
    using Vec3d = Eigen::Matrix<double, 3, 1>;
    using Vec4d = Eigen::Matrix<double, 4, 1>;
    using Vec6d = Eigen::Matrix<double, 6, 1>;
    using Vec9d = Eigen::Matrix<double, 9, 1>;

    using namespace group;
    using SO3d = SO3<double>;       // double precision SO(3)
    using SE3d = SEn3<double, 1>;   // double precision SE(3) with 1 translation
    using SE3d_2 = SEn3<double, 2>; // double precision SE_2(3) with 2 translations

    // ---------------------------------------------------------------------------
    // LieGroup base class (for documentation purposes)
    py::class_<LieGroup>(m, "LieGroup")
        .doc() = R"(
            LieGroup - Abstract base class for all Lie groups

            All Lie groups should implement the following methods:
            - exp(): Exponential map from Lie algebra to Lie group
            - log(): Logarithmic map from Lie group to Lie algebra
            - wedge(): Wedge operator from R^n to Lie algebra
            - vee(): Vee operator from Lie algebra to R^n
            - adjoint(): Adjoint operator
            - random(): Generate a random group element
            - tangent_zero(): Zero element of the Lie algebra
            - __mul__(): Group composition
            - __call__(): Convert to matrix representation
        )";

    // ---------------------------------------------------------------------------
    // SO(3) - 3D Rotation Group
    py::class_<SO3d>(m, "SO3")

        // ---------------------------------------------------------------------
        // Constructors
        // ---------------------------------------------------------------------
        .def(py::init<>(), "Default constructor (identity rotation)")
        .def(py::init([](const Vec4d& q) {
            return SO3d(Quaterniond(q(0), q(1), q(2), q(3)));
        }), "Constructor from quaternion [w, x, y, z].", py::arg("q"))
        .def(py::init<const Matrix3d&>(), "Constructor from rotation matrix", py::arg("R"))
        .def(py::init([](const Vec3d& u) {
            return SO3d::exp(u);
        }), "Constructor from rotation vector (exponential map)", py::arg("u"))
        .def(py::init<const Vec3d&, const Vec3d&>(),
            "Constructor from two vectors u, v such that R * u = v",
            py::arg("u"), py::arg("v"))

        // ---------------------------------------------------------------------
        // Static methods
        // ---------------------------------------------------------------------
        .def_static("exp", &SO3d::exp, "Exponential map R^3 -> SO(3).", py::arg("u"))
        .def_static("log", &SO3d::log, "Logarithmic map SO(3) -> R^3.", py::arg("X"))
        .def_static("wedge", &SO3d::wedge, "Wedge operator R^3 -> so(3). Returns a 3x3 matrix.", py::arg("u"))
        .def_static("vee", &SO3d::vee, "Vee operator so(3) -> R^3. Returns a 3-vector.", py::arg("U"))
        .def_static("adjoint", &SO3d::adjoint, "Adjoint operator for so(3). Returns a 3x3 matrix.", py::arg("u"))

        .def_static("random", []() {
                return SO3d(Quaterniond::UnitRandom());
            },
            "Generate a random SO(3) rotation.")

        .def_static("tangent_zero", []() {
                return Vec3d::Zero();
            }, "Zero element of so(3).",
            py::return_value_policy::copy)

        .def_static("leftJacobian", &SO3d::leftJacobian,
                    "Left Jacobian of SO(3). Returns a 3x3 matrix.",
                    py::arg("u"))
        .def_static("invLeftJacobian", &SO3d::invLeftJacobian,
                    "Inverse Left Jacobian of SO(3). Returns a 3x3 matrix.",
                    py::arg("u"))
        .def_static("rightJacobian", &SO3d::rightJacobian,
                    "Right Jacobian (leftJacobian(-u)). Returns a 3x3 matrix.",
                    py::arg("u"))
        .def_static("invRightJacobian", &SO3d::invRightJacobian,
                    "Inverse Right Jacobian. Returns a 3x3 matrix.",
                    py::arg("u"))
        .def_static("Gamma2", &SO3d::Gamma2,
                    "Gamma2 matrix for SO(3).",
                    py::arg("u"))

        // ---------------------------------------------------------------------
        // Instance accessors (return copies)
        // ---------------------------------------------------------------------
        .def("asMatrix", &SO3d::asMatrix,
             "Return the rotation as a 3x3 matrix.",
             py::return_value_policy::copy)

        .def("R", &SO3d::R,
             "Return the rotation matrix (3x3).",
             py::return_value_policy::copy)

        .def("q",
            [](const SO3d& self) {
                const auto& q = self.q();
                return Vec4d{q.w(), q.x(), q.y(), q.z()};
            },
            "Return quaternion as [w, x, y, z].")

        .def("inv", &SO3d::inv,
             "Return the inverse rotation (SO(3)).",
             py::return_value_policy::copy)

        .def("Adjoint", &SO3d::Adjoint,
             "Return the Adjoint matrix (3x3).",
             py::return_value_policy::copy)

        .def("invAdjoint", &SO3d::invAdjoint,
             "Return the inverse Adjoint matrix (3x3).",
             py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // Mutating methods (operate in-place)
        // ---------------------------------------------------------------------
        .def("multiplyRight", &SO3d::multiplyRight,
             "In-place multiplication: self = self * other. Returns self.",
             py::arg("other"),
             py::return_value_policy::reference_internal)

        .def("multiplyLeft", &SO3d::multiplyLeft,
             "In-place multiplication: self = other * self. Returns self.",
             py::arg("other"),
             py::return_value_policy::reference_internal)

        .def("fromq",
             [](SO3d& self, const Vec4d& q) {
                 self.fromq(Quaterniond(q(0), q(1), q(2), q(3)));
             },
             "Set this rotation from a (normalized) quaternion [w, x, y, z].",
             py::arg("q"),
             py::return_value_policy::reference_internal)

        .def("fromR", &SO3d::fromR,
             "Set this rotation from a rotation matrix.",
             py::arg("R"),
             py::return_value_policy::reference_internal)

        // ---------------------------------------------------------------------
        // Operator overloads
        // ---------------------------------------------------------------------
        .def("__mul__",
            [](const SO3d& a, const SO3d& b) {
                return a * b;
            },
            "Compose with another SO3.",
            py::arg("other"))

        .def("__mul__",
            [](const SO3d& a, const Matrix3d& M) {
                return a * M;
            },
            "Apply rotation to a 3x3 matrix.",
            py::arg("matrix"))

        .def("__mul__",
            [](const SO3d& a, const Vec3d& v) {
                return a * v;
            },
            "Rotate a 3-vector.",
            py::arg("vector"),
            py::return_value_policy::copy)

        .def("__mul__",
            [](const SO3d& a, const Eigen::Matrix<double, 3, Eigen::Dynamic>& vectors) {
                Eigen::Matrix<double, 3, Eigen::Dynamic> result(3, vectors.cols());
                for (int i = 0; i < vectors.cols(); ++i) {
                    result.col(i) = a * vectors.col(i).eval();
                }
                return result;
            },
            "Apply rotation to an array of 3-vectors (3xN matrix).",
            py::arg("vectors"),
            py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // __call__ -> asMatrix
        // ---------------------------------------------------------------------
        .def("__call__", &SO3d::asMatrix,
             "Call operator to get the rotation matrix (3x3).",
             py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // __repr__
        // ---------------------------------------------------------------------
        .def("__repr__", [](const SO3d& self) {
            Eigen::IOFormat fmt(6, 0, ", ", "\n", "  ", "");
            std::ostringstream oss;
            const auto q = self.q();
            const auto R = self.R();
            const auto log_map = self.log(R);
            oss << "<SO3 R=[\n"
                << R.format(fmt)
                << "\n]" << ", R_log=["<< log_map.transpose() << "]" << ", trace=" << R.trace() << ">";
            return oss.str();
            }
        );

    // ---------------------------------------------------------------------------
    // SE(3) - Special Euclidean Group (pose: rotation + translation)
    py::class_<SE3d>(m, "SE3")

        // ---------------------------------------------------------------------
        // Constructors
        // ---------------------------------------------------------------------
        .def(py::init<>(), "Default constructor (identity pose)")
        .def(py::init<const SO3d&, const std::array<Vec3d, 1>&>(),
            "Constructor from rotation and translation array", py::arg("R"), py::arg("t"))
        .def(py::init<const Matrix4d&>(), "Constructor from 4x4 transformation matrix", py::arg("T"))
        // Convenience constructor from single translation vector
        .def(py::init([](const SO3d& R, const Vec3d& t) {
            std::array<Vec3d, 1> t_array = {t};
            return SE3d(R, t_array);
        }), "Constructor from rotation and translation vector", py::arg("R"), py::arg("t"))
        .def(py::init([](const Matrix3d& R, const Vec3d& t) {
            SO3d rot(R);
            std::array<Vec3d, 1> t_array = {t};
            return SE3d(rot, t_array);
        }), "Constructor from rotation matrix and translation vector", py::arg("R"), py::arg("t"))
        .def(py::init([](const Vec3d& u, const Vec3d& t) {
            SO3d rot = SO3d::exp(u); // build rotation from rotation vector
            std::array<Vec3d, 1> t_array = {t};
            return SE3d(rot, t_array);
        }), "Constructor from rotation vector (exponential map) and translation vector", py::arg("R"), py::arg("t"))

        // ---------------------------------------------------------------------
        // Static methods
        // ---------------------------------------------------------------------
        .def_static("exp", &SE3d::exp, "Exponential map: se(3) -> SE(3)", py::arg("u"))
        .def_static("log", &SE3d::log, "Logarithmic map: SE(3) -> se(3)", py::arg("T"))
        .def_static("wedge", &SE3d::wedge, "Wedge operator: R6 -> se(3)", py::arg("u"))
        .def_static("vee", &SE3d::vee, "Vee operator: se(3) -> R6", py::arg("U"))

        .def_static("random", []() {
            Quaterniond q = Quaterniond::UnitRandom();
            SO3d R(q);                      // random rotation
            Vec3d t = Vec3d::Random();       // random translation
            std::array<Vec3d, 1> t_array = {t};
            return SE3d(R, t_array);
        }, "Generate a random SE3 pose (rotation + translation)")

        .def_static("tangent_zero", []() {
                return Vec6d::Zero();
            }, "Zero element of se(3).",
            py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // Instance accessors (return copies)
        // ---------------------------------------------------------------------
        .def("asMatrix", &SE3d::asMatrix, "Return 4x4 transformation matrix", py::return_value_policy::copy)
        .def("R", &SE3d::R, "Return rotation part", py::return_value_policy::copy)
        .def("q", [](const SE3d& self) {
            const auto& q = self.q();
            Vec4d v; v << q.w(), q.x(), q.y(), q.z(); return v;
        }, "Return rotation quaternion as [w, x, y, z]")
        .def("t", &SE3d::t, "Return translation array", py::return_value_policy::copy)
        .def("translation", [](const SE3d& self){ return self.t()[0]; }, "Return translation vector")
        .def("inv", &SE3d::inv, "Return inverse pose", py::return_value_policy::copy)
        .def("Adjoint", &SE3d::Adjoint, "Return Adjoint matrix", py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // Operator overloads
        // ---------------------------------------------------------------------
        .def("__mul__",
            [](const SE3d& a, const SE3d& b){
                return a * b;
            },
            "Compose poses", py::arg("other"))
        .def("__mul__",
            [](const SE3d& a, const Vec3d& p){
                return a * p;
            },
            "Transform point", py::arg("point"), py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // __call__ -> asMatrix
        // ---------------------------------------------------------------------
        .def("__call__", &SE3d::asMatrix,
             "Call operator to get the pose matrix (4x4).",
             py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // __repr__
        // ---------------------------------------------------------------------
        .def("__repr__", [](const SE3d& self){
            return "<SE3 pose>"; // TODO: improve representation
        }
    );


    // ---------------------------------------------------------------------------
    // SE_2(3) - Extended Special Euclidean Group (pose + velocity)
    py::class_<SE3d_2>(m, "SE3_2")

        // ---------------------------------------------------------------------
        // Constructors
        // ---------------------------------------------------------------------
        .def(py::init<>(), "Default constructor (identity extended pose)")
        .def(py::init<const SO3d&, const std::array<Vec3d, 2>&>(),
            "Constructor from rotation and translation array [velocity, position]", py::arg("R"), py::arg("t"))
        // Convenience constructor from std::vector<Vec3d>
        .def(py::init([](const SO3d& R, const std::vector<Vec3d>& translations){
            if(translations.size() != 2) throw std::invalid_argument("Expected exactly 2 translation vectors [velocity, position]");
            std::array<Vec3d,2> t_array = {translations[0], translations[1]};
            return SE3d_2(R, t_array);
        }), "Constructor from rotation and translation vectors [velocity, position]", py::arg("R"), py::arg("translations"))

        // ---------------------------------------------------------------------
        // Static methods
        // ---------------------------------------------------------------------
        .def_static("exp", &SE3d_2::exp, "Exponential map: se_2(3) -> SE_2(3)", py::arg("u"))
        .def_static("log", &SE3d_2::log, "Logarithmic map: SE_2(3) -> se_2(3)", py::arg("T"))
        .def_static("wedge", &SE3d_2::wedge, "Wedge operator: R9 -> se_2(3)", py::arg("u"))
        .def_static("vee", &SE3d_2::vee, "Vee operator: se_2(3) -> R9", py::arg("U"))

        .def_static("random", []() {
            Quaterniond q = Quaterniond::UnitRandom();
            SO3d R(q);                // random rotation
            Vec3d v = Vec3d::Random(); // random velocity
            Vec3d p = Vec3d::Random(); // random position
            std::array<Vec3d, 2> t_array = {v, p};
            return SE3d_2(R, t_array);
        }, "Generate a random SE3_2 pose (rotation + velocity + position)")

        .def_static("tangent_zero", []() {
                return Vec9d::Zero();
            }, "Zero element of se_2(3).",
            py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // Instance accessors (return copies)
        // ---------------------------------------------------------------------
        .def("asMatrix", &SE3d_2::asMatrix, "Return 5x5 extended pose matrix", py::return_value_policy::copy)
        .def("R", &SE3d_2::R, "Return rotation part", py::return_value_policy::copy)
        .def("q", [](const SE3d_2& self){
            const auto& q = self.q(); Vec4d v; v << q.w(), q.x(), q.y(), q.z(); return v;
        }, "Return rotation quaternion as [w, x, y, z]")
        .def("t", &SE3d_2::t, "Return translation array", py::return_value_policy::copy)
        .def("v", [](const SE3d_2& self){ return self.t()[0]; }, "Return velocity vector")
        .def("p", [](const SE3d_2& self){ return self.t()[1]; }, "Return position vector")
        .def("inv", &SE3d_2::inv, "Return inverse extended pose", py::return_value_policy::copy)
        .def("Adjoint", &SE3d_2::Adjoint, "Return Adjoint matrix", py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // Operator overloads
        // ---------------------------------------------------------------------
        .def("__mul__",
            [](const SE3d_2& a, const SE3d_2& b){
                return a * b;
            },
            "Compose extended poses", py::arg("other"))

        // ---------------------------------------------------------------------
        // __call__ -> asMatrix
        // ---------------------------------------------------------------------
        .def("__call__", &SE3d_2::asMatrix,
             "Call operator to get the extended pose matrix (5x5).",
             py::return_value_policy::copy)

        // ---------------------------------------------------------------------
        // __repr__
        // ---------------------------------------------------------------------
        .def("__repr__", [](const SE3d_2& self){
            return "<SE3_2 extended pose>"; // TODO: improve representation
        }
    );

    // =========================================================================
    // Vectorized operators
    // -------------------------------------------------------------------------
    // Same maths as the scalar API above, but crossing the Python/C++ boundary
    // once per *array* instead of once per element. Add a new one with a single
    // def_unary/def_binary line -- see the `batch` namespace.
    // =========================================================================
    py::module_ bm = m.def_submodule(
        "batch",
        "Vectorized Lie-group operators.\n\n"
        "Every function takes C-contiguous float64 arrays shaped (N, *element) and returns\n"
        "(N, *element). The maths is identical to the scalar API; only the number of\n"
        "Python->C++ crossings differs (one per array, not one per entity).");

    // ---- SO(3) --------------------------------------------------------------
    pybind_batch::def_unary<Vec3d, Matrix3d>(
        bm, "so3_exp", [](const Vec3d& u) { return SO3d::exp(u).asMatrix(); },
        "Exponential map, (N,3) -> (N,3,3).");
    pybind_batch::def_unary<Matrix3d, Vec3d>(
        bm, "so3_log", [](const Matrix3d& R) { return SO3d::log(SO3d(R)); },
        "Logarithmic map, (N,3,3) -> (N,3).");
    pybind_batch::def_unary<Matrix3d, Matrix3d>(
        bm, "so3_inv", [](const Matrix3d& R) { return SO3d(R).inv().asMatrix(); },
        "Inverse, (N,3,3) -> (N,3,3).");
    pybind_batch::def_unary<Vec3d, Matrix3d>(
        bm, "so3_right_jacobian", [](const Vec3d& u) { return SO3d::rightJacobian(u); },
        "Right Jacobian, (N,3) -> (N,3,3).");
    pybind_batch::def_unary<Vec3d, Matrix3d>(
        bm, "so3_inv_right_jacobian", [](const Vec3d& u) { return SO3d::invRightJacobian(u); },
        "Inverse right Jacobian, (N,3) -> (N,3,3).");

    pybind_batch::def_binary<Matrix3d, Matrix3d, Matrix3d>(
        bm, "so3_compose",
        [](const Matrix3d& a, const Matrix3d& b) { return (SO3d(a) * SO3d(b)).asMatrix(); },
        "Group composition A*B, (N,3,3) x (N,3,3) -> (N,3,3).");
    pybind_batch::def_binary<Matrix3d, Vec3d, Matrix3d>(
        bm, "so3_retract",
        [](const Matrix3d& R, const Vec3d& u) { return (SO3d(R) * SO3d::exp(u)).asMatrix(); },
        "Right retraction R*exp(u), (N,3,3) x (N,3) -> (N,3,3). The integration primitive.");
    pybind_batch::def_binary<Matrix3d, Vec3d, Vec3d>(
        bm, "so3_rotate", [](const Matrix3d& R, const Vec3d& v) { return Vec3d(R * v); },
        "Rotate vectors, (N,3,3) x (N,3) -> (N,3).");

    // ---- SE(3) --------------------------------------------------------------
    pybind_batch::def_unary<Vec6d, Matrix4d>(
        bm, "se3_exp", [](const Vec6d& u) { return SE3d::exp(u).asMatrix(); },
        "Exponential map, (N,6) -> (N,4,4).");
    pybind_batch::def_unary<Matrix4d, Vec6d>(
        bm, "se3_log", [](const Matrix4d& T) { return SE3d::log(SE3d(T)); },
        "Logarithmic map, (N,4,4) -> (N,6).");
    pybind_batch::def_unary<Matrix4d, Matrix4d>(
        bm, "se3_inv", [](const Matrix4d& T) { return SE3d(T).inv().asMatrix(); },
        "Inverse pose, (N,4,4) -> (N,4,4).");

    pybind_batch::def_binary<Matrix4d, Matrix4d, Matrix4d>(
        bm, "se3_compose",
        [](const Matrix4d& a, const Matrix4d& b) { return (SE3d(a) * SE3d(b)).asMatrix(); },
        "Group composition A*B, (N,4,4) x (N,4,4) -> (N,4,4).");
    pybind_batch::def_binary<Matrix4d, Vec6d, Matrix4d>(
        bm, "se3_retract",
        [](const Matrix4d& T, const Vec6d& u) { return (SE3d(T) * SE3d::exp(u)).asMatrix(); },
        "Right retraction T*exp(u), (N,4,4) x (N,6) -> (N,4,4).");
    pybind_batch::def_binary<Matrix4d, Vec3d, Vec3d>(
        bm, "se3_transform",
        [](const Matrix4d& T, const Vec3d& p) {
            return Vec3d(T.topLeftCorner<3, 3>() * p + T.topRightCorner<3, 1>());
        },
        "Apply a pose to points, (N,4,4) x (N,3) -> (N,3). The frame-change primitive.");

    // TODO: include more bindings as needed
}

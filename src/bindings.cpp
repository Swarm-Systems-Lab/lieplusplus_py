#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <sstream>
#include <iomanip>

// Include Lie++ headers
#include <groups/SO3.hpp>
#include <groups/SEn3.hpp>

namespace py = pybind11;
using Eigen::Matrix3d;
using Eigen::Matrix4d;
using Eigen::Vector3d;
using Eigen::Vector4d;
using Eigen::Quaterniond;

// using group::SO3; // template; we'll instantiate SO3<double>

namespace py = pybind11;
using namespace group;

PYBIND11_MODULE(_core, m) {
    m.doc() = "Python bindings for Lie++ library";

    // SO(3) - 3D Rotation Group
    py::class_<SO3<double>>(m, "SO3")
        // Constructors
        .def(py::init<>(), "Default constructor (identity rotation)")
        .def(py::init<const Quaterniond&>(), "Constructor from quaternion", py::arg("q"))
        .def(py::init<const Matrix3d&>(), "Constructor from rotation matrix", py::arg("R"))
        .def(py::init<const Vector3d&, const Vector3d&>(),
             "Constructor from two vectors u, v such that R * u = v",
             py::arg("u"), py::arg("v"))

        // Static methods (return copies)
        .def_static("wedge", &SO3<double>::wedge,
                    "Wedge operator: R^3 -> so(3). Returns 3x3 matrix.", py::arg("u"),
                    py::return_value_policy::copy)
        .def_static("vee", &SO3<double>::vee,
                    "Vee operator: so(3) -> R^3. Returns 3-vector.", py::arg("U"),
                    py::return_value_policy::copy)
        .def_static("adjoint", &SO3<double>::adjoint,
                    "Adjoint operator for so(3). Returns 3x3 matrix.", py::arg("u"),
                    py::return_value_policy::copy)
        .def_static("Gamma2", &SO3<double>::Gamma2,
                    "Gamma2 matrix for SO3. Returns 3x3 matrix.", py::arg("u"),
                    py::return_value_policy::copy)
        .def_static("leftJacobian", &SO3<double>::leftJacobian,
                    "Left Jacobian of SO3. Returns 3x3 matrix.", py::arg("u"),
                    py::return_value_policy::copy)
        .def_static("invLeftJacobian", &SO3<double>::invLeftJacobian,
                    "Inverse Left Jacobian of SO3. Returns 3x3 matrix.", py::arg("u"),
                    py::return_value_policy::copy)
        .def_static("rightJacobian", &SO3<double>::rightJacobian,
                    "Right Jacobian (calls leftJacobian(-u)). Returns 3x3 matrix.", py::arg("u"),
                    py::return_value_policy::copy)
        .def_static("invRightJacobian", &SO3<double>::invRightJacobian,
                    "Inverse Right Jacobian. Returns 3x3 matrix.", py::arg("u"),
                    py::return_value_policy::copy)
        .def_static("random", []() {
                        Quaterniond q = Quaterniond::UnitRandom(); // random unit quaternion
                        return SO3<double>(q);
                    }, "Generate a random SO3 rotation")

        // Exponential / Log maps
        .def_static("exp", &SO3<double>::exp,
                    "Exponential map: R^3 (so3) -> SO3. Accepts 3-vector.", py::arg("u"),
                    py::return_value_policy::copy)
        .def_static("log", &SO3<double>::log,
                    "Logarithmic map: SO3 -> R^3 (so3). Accepts SO3 instance.", py::arg("X"),
                    py::return_value_policy::copy)

        // Instance accessors (return copies to be safe)
        .def("asMatrix", &SO3<double>::asMatrix,
             "Return rotation as 3x3 matrix.", py::return_value_policy::copy)
        .def("R", &SO3<double>::R,
             "Return rotation matrix (3x3).", py::return_value_policy::copy)
        // .def("q", &SO3<double>::q,
        //      "Return quaternion as [w, x, y, z].", py::return_value_policy::copy)
        .def("q", [](const SO3<double>& self) {
            const auto& q = self.q();
            Vector4d v;
            v << q.w(), q.x(), q.y(), q.z();
            return v;
        }, "Return quaternion as [w, x, y, z]")
        .def("inv", &SO3<double>::inv,
             "Return inverse rotation (SO3).", py::return_value_policy::copy)
        .def("Adjoint", &SO3<double>::Adjoint,
             "Return Adjoint matrix (3x3).", py::return_value_policy::copy)
        .def("invAdjoint", &SO3<double>::invAdjoint,
             "Return inverse Adjoint (3x3).", py::return_value_policy::copy)

        // Mutating methods
        .def("multiplyRight", &SO3<double>::multiplyRight,
             "In-place multiplication: this = this * other. Returns self.", py::arg("other"),
             py::return_value_policy::reference_internal)
        .def("multiplyLeft", &SO3<double>::multiplyLeft,
             "In-place multiplication: this = other * this. Returns self.", py::arg("other"),
             py::return_value_policy::reference_internal)
        .def("fromq", &SO3<double>::fromq,
             "Set this rotation from quaternion (normalized).", py::arg("q"),
             py::return_value_policy::reference_internal)
        .def("fromR", &SO3<double>::fromR,
             "Set this rotation from rotation matrix.", py::arg("R"),
             py::return_value_policy::reference_internal)

        // Operators: multiplication
        // SO3 * SO3 -> SO3
        .def("__mul__", [](const SO3<double>& a, const SO3<double>& b) {
             return a * b;
         }, "Compose with another SO3", py::arg("other"))

        // SO3 * Matrix3d -> Matrix3d
        .def("__mul__", [](const SO3<double>& a, const Matrix3d& M) {
             return a * M;
         }, "Apply rotation to a 3x3 matrix (or compose with matrix)", py::arg("matrix"))

        // SO3 * Vector3d -> Vector3d
        .def("__mul__", [](const SO3<double>& a, const Vector3d& v) {
             return a * v;
         }, "Rotate a 3-vector", py::arg("vector"),
         py::return_value_policy::copy)

        // Rich representation
        .def("__repr__", [](const SO3<double>& self) {
             std::ostringstream oss;
             const auto q = self.q();
             const auto R = self.R();
             oss << "<SO3 q=[" << std::setprecision(6) << q.w() << ", "
                 << q.x() << ", " << q.y() << ", " << q.z() << "]"
                 << " trace=" << (R.trace()) << ">";
             return oss.str();
         });

    // SE(3) - Special Euclidean Group (pose: rotation + translation)
    py::class_<SEn3<double, 1>>(m, "SE3")
        // Constructors
        .def(py::init<>(), "Default constructor (identity pose)")
        .def(py::init<const SO3<double>&, const std::array<Vector3d, 1>&>(),
            "Constructor from rotation and translation array", py::arg("R"), py::arg("t"))
        .def(py::init<const Matrix4d&>(), "Constructor from 4x4 transformation matrix", py::arg("T"))
        // Convenience constructor from single translation vector
        .def(py::init([](const SO3<double>& R, const Vector3d& t) {
            std::array<Vector3d, 1> t_array = {t};
            return SEn3<double, 1>(R, t_array);
        }), "Constructor from rotation and translation vector", py::arg("R"), py::arg("t"))
        
        // Static methods
        .def_static("wedge", &SEn3<double, 1>::wedge, "Wedge operator: R6 -> se(3)", py::arg("u"))
        .def_static("vee", &SEn3<double, 1>::vee, "Vee operator: se(3) -> R6", py::arg("U"))
        .def_static("random", []() {
            Quaterniond q = Quaterniond::UnitRandom();
            SO3<double> R(q);                      // random rotation
            Vector3d t = Vector3d::Random();       // random translation
            std::array<Vector3d, 1> t_array = {t};
            return SEn3<double, 1>(R, t_array);
        }, "Generate a random SE3 pose (rotation + translation)")

        // Exponential / Log maps
        .def_static("exp", &SEn3<double, 1>::exp, "Exponential map: se(3) -> SE(3)", py::arg("u"))
        .def_static("log", &SEn3<double, 1>::log, "Logarithmic map: SE(3) -> se(3)", py::arg("T"))

        // Instance accessors (return copies)
        .def("asMatrix", &SEn3<double, 1>::asMatrix, "Return 4x4 transformation matrix", py::return_value_policy::copy)
        .def("R", &SEn3<double, 1>::R, "Return rotation part", py::return_value_policy::copy)
        .def("q", [](const SEn3<double, 1>& self) {
            const auto& q = self.q();
            Vector4d v; v << q.w(), q.x(), q.y(), q.z(); return v;
        }, "Return rotation quaternion as [w, x, y, z]")
        .def("t", &SEn3<double, 1>::t, "Return translation array", py::return_value_policy::copy)
        .def("translation", [](const SEn3<double, 1>& self){ return self.t()[0]; }, "Return translation vector")
        .def("inv", &SEn3<double, 1>::inv, "Return inverse pose", py::return_value_policy::copy)
        .def("Adjoint", &SEn3<double, 1>::Adjoint, "Return Adjoint matrix", py::return_value_policy::copy)

        // Operators
        .def("__mul__", [](const SEn3<double, 1>& a, const SEn3<double, 1>& b){ return a * b; }, "Compose poses", py::arg("other"))
        .def("__mul__", [](const SEn3<double, 1>& a, const Vector3d& p){ return a * p; }, "Transform point", py::arg("point"), py::return_value_policy::copy)

        // Representation
        .def("__repr__", [](const SEn3<double, 1>& self){
            return "<SE3 pose>";
    });


    // SE_2(3) - Extended Special Euclidean Group (pose + velocity)
    py::class_<SEn3<double, 2>>(m, "SE23")
        // Constructors
        .def(py::init<>(), "Default constructor (identity extended pose)")
        .def(py::init<const SO3<double>&, const std::array<Vector3d, 2>&>(),
            "Constructor from rotation and translation array [velocity, position]", py::arg("R"), py::arg("t"))
        // Convenience constructor from std::vector<Vector3d>
        .def(py::init([](const SO3<double>& R, const std::vector<Vector3d>& translations){
            if(translations.size() != 2) throw std::invalid_argument("Expected exactly 2 translation vectors [velocity, position]");
            std::array<Vector3d,2> t_array = {translations[0], translations[1]};
            return SEn3<double, 2>(R, t_array);
        }), "Constructor from rotation and translation vectors [velocity, position]", py::arg("R"), py::arg("translations"))

        // Static methods
        .def_static("wedge", &SEn3<double, 2>::wedge, "Wedge operator: R9 -> se_2(3)", py::arg("u"))
        .def_static("vee", &SEn3<double, 2>::vee, "Vee operator: se_2(3) -> R9", py::arg("U"))
        .def_static("random", []() {
            Quaterniond q = Quaterniond::UnitRandom();
            SO3<double> R(q);                // random rotation
            Vector3d v = Vector3d::Random(); // random velocity
            Vector3d p = Vector3d::Random(); // random position
            std::array<Vector3d, 2> t_array = {v, p};
            return SEn3<double, 2>(R, t_array);
        }, "Generate a random SE23 pose (rotation + velocity + position)")
        
        // Exponential / Log maps
        .def_static("exp", &SEn3<double, 2>::exp, "Exponential map: se_2(3) -> SE_2(3)", py::arg("u"))
        .def_static("log", &SEn3<double, 2>::log, "Logarithmic map: SE_2(3) -> se_2(3)", py::arg("T"))

        // Instance accessors
        .def("asMatrix", &SEn3<double, 2>::asMatrix, "Return 5x5 extended pose matrix", py::return_value_policy::copy)
        .def("R", &SEn3<double, 2>::R, "Return rotation part", py::return_value_policy::copy)
        .def("q", [](const SEn3<double, 2>& self){
            const auto& q = self.q(); Vector4d v; v << q.w(), q.x(), q.y(), q.z(); return v;
        }, "Return rotation quaternion as [w, x, y, z]")
        .def("t", &SEn3<double, 2>::t, "Return translation array", py::return_value_policy::copy)
        .def("v", [](const SEn3<double, 2>& self){ return self.t()[0]; }, "Return velocity vector")
        .def("p", [](const SEn3<double, 2>& self){ return self.t()[1]; }, "Return position vector")
        .def("inv", &SEn3<double, 2>::inv, "Return inverse extended pose", py::return_value_policy::copy)
        .def("Adjoint", &SEn3<double, 2>::Adjoint, "Return Adjoint matrix", py::return_value_policy::copy)

        // Operators
        .def("__mul__", [](const SEn3<double, 2>& a, const SEn3<double, 2>& b){ return a * b; }, "Compose extended poses", py::arg("other"))

        // Representation
        .def("__repr__", [](const SEn3<double, 2>& self){
            return "<SE23 extended pose>";
    });

    // // Add version info
    // m.attr("__version__") = VERSION_INFO;
}
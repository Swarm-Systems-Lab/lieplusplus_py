// pybind_batch.hpp -- vectorize single-element C++ kernels for numpy, generically.
//
// Scalar kernels are the right default for robotics maths: one robot's algebra rarely needs
// vectorization. The cost of calling them from Python is not the arithmetic (tens of nanoseconds)
// but the pybind boundary crossing (~1-1.5 us), so a Python loop over N entities pays it N times.
// These helpers cross once and loop in C++.
//
// Nothing here is library-specific: it only assumes fixed-size Eigen types in and out. Drop this
// header into any pybind11 project and vectorize an operator with one line:
//
//     namespace pb = pybind_batch;
//     pb::def_unary<Vec3d, Matrix3d>(m, "so3_exp",
//                                    [](const Vec3d& u) { return SO3::exp(u).asMatrix(); },
//                                    "Exponential map.");
//
// What callers get for free:
//   * shape polymorphism -- pass one element or a stack; the return matches
//   * leading-axis broadcasting -- pair N with 1 (a shared pose against many points)
//   * layout/dtype freedom -- non-contiguous views, Fortran order, float32 and lists all convert
//   * an `out=` parameter -- write into an existing array, allocating nothing
//   * shape errors naming the operator and the argument

#pragma once

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include <Eigen/Core>
#include <algorithm>
#include <string>
#include <vector>

namespace pybind_batch {

namespace py = pybind11;

// Inputs accept anything convertible; `out` must already be a writable C-contiguous float64
// array, since silently copying it would defeat the point of passing it.
using InArr = py::array_t<double, py::array::c_style | py::array::forcecast>;
using OutArr = py::array_t<double, py::array::c_style>;

// -- element traits ---------------------------------------------------------------------------
template <typename T>
struct Elem;

template <int R, int C>
struct Elem<Eigen::Matrix<double, R, C>> {
    static constexpr int rows = R;
    static constexpr int cols = C;
    static constexpr bool is_vector = (C == 1);
    static constexpr int size = R * C;
    static constexpr int rank = is_vector ? 1 : 2;  // trailing dims of ONE element
    // numpy is row-major; a fixed-size Eigen *vector* may not be declared RowMajor.
    using Layout = Eigen::Matrix<double, R, C, is_vector ? Eigen::ColMajor : Eigen::RowMajor>;

    static std::vector<py::ssize_t> dims() {
        if (is_vector) return {R};
        return {R, C};
    }
    static std::string shape_str() {
        std::string tail = is_vector ? std::to_string(R)
                                     : std::to_string(R) + ", " + std::to_string(C);
        return "(" + tail + ") or (N, " + tail + ")";
    }
};

// -- argument inspection ------------------------------------------------------------------------
template <typename T>
struct Operand {
    const double* data = nullptr;
    py::ssize_t count = 1;   // 1 when a single element (broadcasts)
    bool batched = false;

    // Index of the element to use for output row i (a single element repeats).
    py::ssize_t at(py::ssize_t i) const { return count == 1 ? 0 : i; }
};

[[noreturn]] inline void shape_error(const char* op, const char* arg, const std::string& want,
                                     const std::string& got) {
    throw std::invalid_argument(std::string(op) + ": argument '" + arg + "' must have shape " +
                                want + ", got " + got);
}

inline std::string describe(const InArr& a) {
    std::string s = "(";
    for (py::ssize_t k = 0; k < a.ndim(); ++k) {
        s += std::to_string(a.shape(k));
        if (k + 1 < a.ndim()) s += ", ";
    }
    return s + ")";
}

template <typename T>
Operand<T> inspect(const InArr& a, const char* op, const char* arg) {
    const auto dims = Elem<T>::dims();
    const py::ssize_t rank = static_cast<py::ssize_t>(dims.size());

    Operand<T> in;
    if (a.ndim() == rank) {
        in.batched = false;
        in.count = 1;
    } else if (a.ndim() == rank + 1) {
        in.batched = true;
        in.count = a.shape(0);
    } else {
        shape_error(op, arg, Elem<T>::shape_str(), describe(a));
    }

    const py::ssize_t offset = in.batched ? 1 : 0;
    for (py::ssize_t k = 0; k < rank; ++k) {
        if (a.shape(k + offset) != dims[k]) shape_error(op, arg, Elem<T>::shape_str(), describe(a));
    }
    in.data = a.data();
    return in;
}

// -- element read / write -----------------------------------------------------------------------
template <typename T>
inline T read(const double* base, py::ssize_t i) {
    return T(Eigen::Map<const typename Elem<T>::Layout>(base + i * Elem<T>::size));
}

template <typename T>
inline void write(double* base, py::ssize_t i, const T& value) {
    Eigen::Map<typename Elem<T>::Layout>(base + i * Elem<T>::size) = value;
}

// -- broadcasting -------------------------------------------------------------------------------
// Operands are compatible when their counts are equal, or one of them is a single element.
inline py::ssize_t broadcast(py::ssize_t a, py::ssize_t b, const char* op) {
    if (a == b || b == 1) return a;
    if (a == 1) return b;
    throw std::invalid_argument(std::string(op) +
                                ": leading dimensions do not broadcast, got " + std::to_string(a) +
                                " and " + std::to_string(b));
}

// -- output allocation ----------------------------------------------------------------------------
template <typename Out>
py::array make_output(py::ssize_t n, bool single, const py::object& out, const char* op) {
    std::vector<py::ssize_t> shape;
    if (!single) shape.push_back(n);
    for (auto d : Elem<Out>::dims()) shape.push_back(d);

    if (out.is_none()) return OutArr(shape);

    OutArr provided;
    try {
        provided = out.cast<OutArr>();
    } catch (const py::cast_error&) {
        throw std::invalid_argument(std::string(op) +
                                    ": 'out' must be a writable C-contiguous float64 array");
    }
    if (provided.ndim() != static_cast<py::ssize_t>(shape.size())) {
        throw std::invalid_argument(std::string(op) + ": 'out' has the wrong rank");
    }
    for (size_t k = 0; k < shape.size(); ++k) {
        if (provided.shape(k) != shape[k]) {
            throw std::invalid_argument(std::string(op) + ": 'out' has the wrong shape");
        }
    }
    return provided;
}

// -- the maps -------------------------------------------------------------------------------------
template <typename In, typename Out, typename F>
py::array map_unary(const InArr& x, const py::object& out, const F& f, const char* op) {
    const auto a = inspect<In>(x, op, "x");
    py::array result = make_output<Out>(a.count, !a.batched, out, op);
    double* dst = static_cast<double*>(result.mutable_data());
    for (py::ssize_t i = 0; i < a.count; ++i) write<Out>(dst, i, f(read<In>(a.data, a.at(i))));
    return result;
}

template <typename A, typename B, typename Out, typename F>
py::array map_binary(const InArr& x, const InArr& y, const py::object& out, const F& f,
                     const char* op) {
    const auto a = inspect<A>(x, op, "x");
    const auto b = inspect<B>(y, op, "y");
    const py::ssize_t n = broadcast(a.count, b.count, op);
    const bool single = !a.batched && !b.batched;

    py::array result = make_output<Out>(n, single, out, op);
    double* dst = static_cast<double*>(result.mutable_data());
    for (py::ssize_t i = 0; i < n; ++i)
        write<Out>(dst, i, f(read<A>(a.data, a.at(i)), read<B>(b.data, b.at(i))));
    return result;
}

// -- registration (one line per vectorized operator) ----------------------------------------------
inline std::string doc_with_shapes(const char* doc, const std::string& in, const std::string& out) {
    return std::string(doc) + "\n\nShapes: " + in + " -> " + out +
           "\nPass one element or a stack; the result matches. `out=` writes in place.";
}

template <typename In, typename Out, typename F>
void def_unary(py::module_& m, const char* name, F f, const char* doc) {
    std::string owned(name);
    m.def(
        name,
        [f, owned](const InArr& x, py::object out) {
            return map_unary<In, Out>(x, out, f, owned.c_str());
        },
        py::arg("x"), py::arg("out") = py::none(),
        doc_with_shapes(doc, Elem<In>::shape_str(), Elem<Out>::shape_str()).c_str());
}

template <typename A, typename B, typename Out, typename F>
void def_binary(py::module_& m, const char* name, F f, const char* doc) {
    std::string owned(name);
    m.def(
        name,
        [f, owned](const InArr& x, const InArr& y, py::object out) {
            return map_binary<A, B, Out>(x, y, out, f, owned.c_str());
        },
        py::arg("x"), py::arg("y"), py::arg("out") = py::none(),
        doc_with_shapes(doc, Elem<A>::shape_str() + " x " + Elem<B>::shape_str(),
                        Elem<Out>::shape_str())
            .c_str());
}

}  // namespace pybind_batch

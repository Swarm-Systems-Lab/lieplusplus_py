cmake_minimum_required(VERSION 3.18)
project(lieplusplus_py LANGUAGES CXX)

# Pass version to C++ code
add_definitions(-DVERSION="${SKBUILD_PROJECT_VERSION}")

# Use FetchContent to obtain dependencies if not present
include(FetchContent)

# pybind11 via CMake package
find_package(pybind11 CONFIG REQUIRED)

# Try to find Eigen3; fall back to fetching it
find_package(Eigen3 QUIET)
if(NOT Eigen3_FOUND)
    message(STATUS "Eigen3 not found, fetching via FetchContent")
    FetchContent_Declare(
        eigen
        GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
        GIT_TAG 3.4.0
    )
    FetchContent_MakeAvailable(eigen)
    # FetchContent provides eigen_SOURCE_DIR variable
else()
    message(STATUS "Found system Eigen3: ${Eigen3_VERSION}")
endif()

# Fetch Lie-plusplus if not included
set(LPP_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/external/Lie-plusplus/include")
if(NOT EXISTS ${LPP_INCLUDE_DIR})
    message(STATUS "Lie-plusplus not found, fetching via FetchContent")
    FetchContent_Declare(
        lieplusplus
        GIT_REPOSITORY https://github.com/jesusBV20/Lie-plusplus.git
        GIT_TAG main
    )
    FetchContent_MakeAvailable(lieplusplus)
    # Lie-plusplus is header-only; includes will be ${lieplusplus_SOURCE_DIR}/include
    set(LPP_INCLUDE_DIR "${lieplusplus_SOURCE_DIR}/include")
endif()

# Create the pybind11 module
pybind11_add_module(_core
    src/bindings.cpp
)

# Set C++ standard
target_compile_features(_core PRIVATE cxx_std_17)

# Include directories
if(TARGET Eigen3::Eigen)
    target_link_libraries(_core PRIVATE Eigen3::Eigen)
elseif(DEFINED eigen_SOURCE_DIR)
    target_include_directories(_core PRIVATE ${eigen_SOURCE_DIR})
else()
    message(WARNING "Eigen include directories not found; compilation may fail")
endif()

target_include_directories(_core PRIVATE ${LPP_INCLUDE_DIR})

# Link libraries if needed (pybind11 handles Python linkage)

# Export include dirs for downstream
message(STATUS "Eigen include: ${EIGEN3_INCLUDE_DIRS}")
message(STATUS "Lie-plusplus include: ${LPP_INCLUDE_DIR}")

# Install the compiled extension into the purelib path so it lands next to the
# Python package in the final wheel.
install(
    TARGETS _core
    LIBRARY DESTINATION ${SKBUILD_PLATLIB_DIR}/lieplusplus
    ARCHIVE DESTINATION ${SKBUILD_PLATLIB_DIR}/lieplusplus
    RUNTIME DESTINATION ${SKBUILD_PLATLIB_DIR}/lieplusplus
)

from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyMadngTpsa(PythonPackage):
    """Python bindings to the GTPSA (truncated power series) engine of MAD-NG."""

    homepage = "https://github.com/MethodicalAcceleratorDesign/madng-tpsa"
    pypi = "madng-tpsa/madng_tpsa-0.3.2.tar.gz"

    license("GPL-3.0-only")

    version("0.3.2", sha256="bcded827b436de5823f74c158c20ad569ecb53b7d9adb9449b7c046054140150")

    # PyPI has no linux-aarch64 wheel, so this is always built from the sdist:
    # a C23 shared library (libmadng_tpsa) linked against BLAS/LAPACK and
    # loaded at runtime through cffi.
    depends_on("c", type="build")

    depends_on("python@3.11:", type=("build", "run"))
    depends_on("py-scikit-build-core@0.10:", type="build")
    depends_on("py-setuptools-scm@8:", type="build")
    # CMake C_STANDARD 23 needs CMake 3.21.
    depends_on("cmake@3.21:", type="build")

    # Found by CMake's FindBLAS/FindLAPACK through CMAKE_PREFIX_PATH.
    depends_on("blas")
    depends_on("lapack")

    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))


from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *
import os


class PyXsuite(PythonPackage):
    """Xsuite: tracking simulations for particle accelerators."""

    homepage = "https://github.com/xsuite/xsuite"
    #url = "https://github.com/xsuite/xsuite/archive/refs/tags/v0.36.7.tar.gz"
    git = "https://github.com/xsuite/xsuite.git"

    license("Apache-2.0")

    version("main", branch="main")
    version("0.36.7", tag="v0.36.7", submodules=True)

    #version("0.36.7", sha256="0425b01189f2cdd5ed2782895596aacd439232365c914d45f46ab14d85e267f1")
    #version("0.35.1", sha256="136bb4cb4cc8b5e823423138f59ae2cc98264b523669b14876b628d818d00bbb")

    # Core dependencies
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-numpy", type=("build", "run"))

    # Optional: FFTW
    depends_on("py-pyfftw", type=("build", "run"), when="+fftw")

    # Optional: GPU/OpenCL backends
    depends_on("py-pyopencl", type=("build", "run"), when="+opencl")
    depends_on("py-cupy", type=("build", "run"), when="+cuda")

    # Variants for enabling optional backends
    variant("fftw", default=False, description="Enable FFTW backend via pyfftw")
    variant("opencl", default=False, description="Enable OpenCL backend via pyopencl")
    variant("cuda", default=False, description="Enable CUDA backend via CuPy")

    depends_on("py-pandas")
    depends_on("py-scipy")
    depends_on("py-lark")
    depends_on("py-pytest")
    depends_on("py-sphinx")
    depends_on("py-cython")

    #other parts of the xsuite suite
    depends_on("py-xtrack@0.88.8")
    depends_on("py-xfields@0.25.1")
    depends_on("py-xcoll@0.6.2")
    depends_on("py-xobjects@0.5.2")
    depends_on("py-xdeps")
    depends_on("py-xpart@0.23.1")
    depends_on("py-xwakes")

    def setup_build_environment(self, env):
        # Skip kernel building during spack build to avoid the lib directory issue
        # Kernels will be built when the package is first used
        env.set('SKIP_KERNEL_BUILD', '1')

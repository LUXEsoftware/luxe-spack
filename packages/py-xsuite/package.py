from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXsuite(PythonPackage):
    """Xsuite: tracking simulations for particle accelerators.

    Meta-package pinning a consistent set of the Xsuite components."""

    homepage = "https://github.com/xsuite/xsuite"
    url = "https://github.com/xsuite/xsuite/archive/refs/tags/v0.62.2.tar.gz"
    git = "https://github.com/xsuite/xsuite.git"

    license("Apache-2.0")

    version("main", branch="main")
    version("0.62.2", sha256="92752320cb1c3c998bf13627d43ec0129c34cc3aa3a74d7f03749b5adc4417fb")
    version("0.36.7", tag="v0.36.7", submodules=True)

    variant("fftw", default=False, description="Enable FFTW backend via pyfftw")
    variant("opencl", default=False, description="Enable OpenCL backend via pyopencl")
    variant("cuda", default=False, description="Enable CUDA backend via CuPy")
    variant("geant4", default=True, when="@0.37:",
            description="Enable the Xcoll Geant4 (BDSIM) scattering engine")
    # Since 0.37 xsuite refuses to JIT-compile tracking kernels unless allowed
    # to, and expects them prebuilt in xsuite/lib (as shipped in the wheels).
    variant("prebuilt_kernels", default=True, when="@0.37:",
            description="Compile the CPU tracking kernels at install time")

    depends_on("python@3.11:", type=("build", "run"), when="@0.62:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@77:", type="build", when="@0.62:")
    depends_on("py-setuptools-scm@8:", type="build", when="@0.62:")
    depends_on("py-wheel", type="build", when="@:0.36")
    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-pyfftw", type=("build", "run"), when="+fftw")
    depends_on("py-pyopencl", type=("build", "run"), when="+opencl")
    depends_on("py-cupy", type=("build", "run"), when="+cuda")

    # Exact component versions, as pinned by the xsuite release itself.
    _components = {
        "0.62.2": {
            "xtrack": "0.114.1",
            "xfields": "0.27.3",
            "xcoll": "0.12.3",
            "xobjects": "0.7.0",
            "xdeps": "0.10.21",
            "xpart": "0.23.18",
        },
        "0.36.7": {
            "xtrack": "0.88.8",
            "xfields": "0.25.1",
            "xcoll": "0.6.2",
            "xobjects": "0.5.2",
            "xpart": "0.23.1",
        },
    }
    for _ver, _pins in _components.items():
        for _name, _pin in _pins.items():
            depends_on(f"py-{_name}@{_pin}", type=("build", "run"), when=f"@{_ver}")
    # Not pinned by xsuite (and xdeps 0.10.6, pinned by 0.36.7, was never
    # packaged here).
    depends_on("py-xdeps", type=("build", "run"))
    depends_on("py-xwakes", type=("build", "run"))

    depends_on("py-xcoll+geant4", type=("build", "run"), when="+geant4")
    depends_on("py-xcoll~geant4", type=("build", "run"), when="~geant4")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+prebuilt_kernels"):
            env.set("XSUITE_KERNEL_BUILD_THREADS", str(make_jobs))
        else:
            env.set("SKIP_KERNEL_BUILD", "1")  # xsuite <= 0.36
            env.set("XSUITE_SKIP_KERNEL_BUILD", "1")
        # The version is otherwise derived from git metadata (setuptools-scm),
        # which a release tarball does not have.
        if not self.spec.satisfies("@main"):
            env.set("SETUPTOOLS_SCM_PRETEND_VERSION", str(self.version))

    def setup_run_environment(self, env):
        # Kernels not covered by the prebuilt set (other element combinations,
        # user-defined elements, or ~prebuilt_kernels) are compiled on the fly
        # instead of raising PrebuiltKernelNotFoundError, as in xsuite <= 0.36.
        env.set("XSUITE_ALLOW_KERNEL_COMPILATION", "1")

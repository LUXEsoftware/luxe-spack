from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXobjects(PythonPackage):
    """In-memory serialization and code generator for CPU and GPU (part of
    Xsuite)."""

    homepage = "https://github.com/xsuite/xobjects"
    url = "https://github.com/xsuite/xobjects/archive/refs/tags/v0.7.0.tar.gz"

    license("Apache-2.0")

    version("0.7.0", sha256="edff537367eb0e9423fe698a77770429e5a4e6f4adf0e644160dda64b3fe7b71")
    version("0.5.2", sha256="869e5c4991c6b28f5a6d5333a0f4d25e2542ba818e191373b1728723a65b6c79")

    depends_on("c", type="build")

    depends_on("python@3.9:", type=("build", "run"), when="@0.7:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@77:", type="build", when="@0.7:")

    depends_on("py-numpy", type=("build", "run"))
    # Kernels are compiled at runtime through cffi.
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

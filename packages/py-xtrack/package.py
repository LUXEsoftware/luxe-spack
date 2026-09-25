from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXtrack(PythonPackage):
    """Tracking library for particle accelerators (part of Xsuite)."""

    homepage = "https://github.com/xsuite/xtrack"
    url = "https://github.com/xsuite/xtrack/archive/refs/tags/v0.114.1.tar.gz"

    license("Apache-2.0")

    version("0.114.1", sha256="ab219c797cf6a642223aa5f5df7a5aa537494780a63d25074bb7f91716d2583d")
    version("0.88.8", sha256="20b117628bfaafa3f784d154bd1b2ca150ee1de05cf3e541424dd83059b5c965")
    version("0.88.7", sha256="5c8e04018b55413f2117ed3739759d160bba776d68660c2590237a026d64ca96")
    version("0.88.6", sha256="9a69a68d2ab4bd3a3acb2d7ca407098b63c827a5435e06082b46f7d82bc374fb")

    depends_on("python@3.11:", type=("build", "run"), when="@0.114:")

    depends_on("py-setuptools@43:", type="build")
    depends_on("py-setuptools@77:", type="build", when="@0.114:")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas@2:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-xobjects", type=("build", "run"))
    depends_on("py-xdeps", type=("build", "run"))
    # Imported unconditionally by xtrack.base_element.
    depends_on("py-madng-tpsa@0.3.1:", type=("build", "run"), when="@0.114:")

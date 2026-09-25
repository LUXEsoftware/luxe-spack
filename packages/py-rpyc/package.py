from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyRpyc(PythonPackage):
    """RPyC: remote python call, a transparent symmetric distributed computing
    library. Provides the rpyc_classic server script."""

    homepage = "https://github.com/tomerfiliba-org/rpyc"
    pypi = "rpyc/rpyc-6.0.2.tar.gz"

    license("MIT")

    version("6.0.2", sha256="8e780a6a71b842128a80a337c64adfb6f919014e069951832161c9efc630c93b")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-hatchling@1.6:", type="build")

    depends_on("py-plumbum", type=("build", "run"))

from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXfields(PythonPackage):
    """Field maps and particle-in-cell (part of Xsuite)."""

    homepage = "https://github.com/xsuite/xfields"
    url = "https://github.com/xsuite/xfields/archive/refs/tags/v0.27.3.tar.gz"

    license("Apache-2.0")

    version("0.27.3", sha256="37352b6d0aea3ef2a8c4ae27524103130e2ae01692481e2200b7c9db2e807de0")
    version("0.25.1", sha256="1586e2bee26021086ce8918f28106f2674ada4f762c3bf7b76967b3e1a0f4264")
    version("0.25.0", sha256="a94ead231802ce7c15e4b2f107734f6f44befe0502755eff1150ef5d6de7d4fe")
    version("0.24.0", sha256="43faf361a6a2066276ea0debd09c1806b42d3ddbf8942654c6581b6113081e1e")

    depends_on("python@3.10:", type=("build", "run"), when="@0.27:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@77:", type="build", when="@0.27:")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-xobjects", type=("build", "run"))
    depends_on("py-xtrack", type=("build", "run"))

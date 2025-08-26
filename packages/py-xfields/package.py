from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXfields(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/xsuite/xfields"
    url = "https://github.com/xsuite/xfields/archive/refs/tags/v0.25.1.tar.gz"

    version("0.25.1", sha256="1586e2bee26021086ce8918f28106f2674ada4f762c3bf7b76967b3e1a0f4264")
    version("0.25.0", sha256="a94ead231802ce7c15e4b2f107734f6f44befe0502755eff1150ef5d6de7d4fe")
    version("0.24.0", sha256="43faf361a6a2066276ea0debd09c1806b42d3ddbf8942654c6581b6113081e1e")

    depends_on('py-setuptools')
    depends_on('py-numpy')
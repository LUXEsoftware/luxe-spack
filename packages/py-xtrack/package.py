from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXtrack(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/xsuite/xtrack"
    url = "https://github.com/xsuite/xtrack/archive/refs/tags/v0.88.8.tar.gz"

    version("0.88.8", sha256="20b117628bfaafa3f784d154bd1b2ca150ee1de05cf3e541424dd83059b5c965")
    version("0.88.7", sha256="5c8e04018b55413f2117ed3739759d160bba776d68660c2590237a026d64ca96")
    version("0.88.6", sha256="9a69a68d2ab4bd3a3acb2d7ca407098b63c827a5435e06082b46f7d82bc374fb")

    depends_on('py-setuptools')
    depends_on('py-numpy')
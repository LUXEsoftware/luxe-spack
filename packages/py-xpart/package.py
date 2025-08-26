from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXpart(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/xsuite/xpart"
    url = "https://github.com/xsuite/xpart/archive/refs/tags/v0.23.1.tar.gz"

    version("0.23.1", sha256="c2fd94755de1742b72f2e8018164c73079ab1356fdd4209c504d0d6ca1952adb")
    version("0.23.0", sha256="3045f48e37bd8f43c9d830c3ee7c8357fdbb023e4ea8d074c94b7eae94a6e2ac")
    version("0.22.0", sha256="416bf141aae80ca4241acbd6773a2b4d75913cbd06a356dcd889bc87e158d554")

    depends_on('py-setuptools')
    depends_on('py-numpy')
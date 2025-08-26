from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXobjects(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/xsuite/xobjects"
    url = "https://github.com/xsuite/xobjects/archive/refs/tags/v0.5.2.tar.gz"

    version("0.5.2", sha256="869e5c4991c6b28f5a6d5333a0f4d25e2542ba818e191373b1728723a65b6c79")

    depends_on("c", type="build")
    
    depends_on('py-setuptools')
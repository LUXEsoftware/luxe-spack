from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXwakes(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/xsuite/xwakes"
    url = "https://github.com/xsuite/xwakes/archive/refs/tags/v0.2.5.tar.gz"

    version("0.2.5", sha256="7a318e7d26b9e1f92ff0a751631c107d904e724e87277aa0640b474188640889")
    version("0.2.4", sha256="b45d71928150b8c7c5d0fc620b727183b3cb1ae346762915c8186284ec2ac010")
    version("0.2.3", sha256="30d50040b25f4e40068998f5d46d8bed5fbdb949fdddbe607c02b334200c835f")

    depends_on('py-setuptools')
    depends_on('py-numpy')
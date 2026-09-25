from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXwakes(PythonPackage):
    """Wake and impedance toolbox, usable in Xsuite, DELPHI and others."""

    homepage = "https://github.com/xsuite/xwakes"
    url = "https://github.com/xsuite/xwakes/archive/refs/tags/v0.2.10.tar.gz"

    license("Apache-2.0")

    version("0.2.10", sha256="b37af03cb278102aae4cd9b3b5b580f54b2133ebc99d0eed6abc115daf0d1ef1")
    version("0.2.5", sha256="7a318e7d26b9e1f92ff0a751631c107d904e724e87277aa0640b474188640889")
    version("0.2.4", sha256="b45d71928150b8c7c5d0fc620b727183b3cb1ae346762915c8186284ec2ac010")
    version("0.2.3", sha256="30d50040b25f4e40068998f5d46d8bed5fbdb949fdddbe607c02b334200c835f")

    depends_on("py-setuptools@43:", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-xpart", type=("build", "run"))
    depends_on("py-xfields", type=("build", "run"))

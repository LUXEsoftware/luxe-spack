from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXsuite(PythonPackage):
    """Python bindings for Xsuite"""

    homepage = "https://github.com/xsuite/xsuite"
    url = "https://github.com/xsuite/xsuite/archive/refs/tags/v0.36.7.tar.gz"
    git = "https://github.com/xsuite/xsuite.git"

    version("main", branch="main")

    version("0.36.7", sha256="0425b01189f2cdd5ed2782895596aacd439232365c914d45f46ab14d85e267f1")
    version("0.35.1", sha256="136bb4cb4cc8b5e823423138f59ae2cc98264b523669b14876b628d818d00bbb")

    depends_on("py-pandas")
    depends_on("py-scipy")
    depends_on("py-lark")
    depends_on("py-pytest")
    depends_on("py-sphinx")
    depends_on('py-setuptools')
    depends_on("py-numpy")
    depends_on("py-wheel")
    depends_on("py-cython")

    #other parts of the xsuite suite
    depends_on("py-xtrack@0.88.8")
    depends_on("py-xfields@0.25.1")
    depends_on("py-xcoll@0.6.2")
    depends_on("py-xobjects@0.5.2")
    depends_on("py-xdeps")
    depends_on("py-xpart@0.23.1")
    depends_on("py-xwakes")

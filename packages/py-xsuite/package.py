from spack.package import *


class PyXsuite(PythonPackage):
    """Python bindings for Xsuite"""

    homepage = "https://github.com/xsuite/xsuite"
    url = "https://github.com/xsuite/xsuite/archive/refs/tags/v0.36.7.tar.gz"
    git = "https://github.com/xsuite/xsuite.git"

    version("main", branch="main")

    version("0.36.7",
        sha256="17a6f941e4fa06d08a628990f6816d1da5e545d65f533e6f598740d2cb76ace4",
    )

    depends_on("py-numpy")
    depends_on("py-pandas")
    depends_on("py-scipy")
    depends_on("py-cython")
    depends_on("py-lark")
    depends_on("py-pytest")
    depends_on("py-sphinx")
    #depends_on("py-sphinx_rtd_theme")
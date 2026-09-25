from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXdeps(PythonPackage):
    """Data dependency manager (part of Xsuite)."""

    homepage = "https://github.com/xsuite/xdeps"
    url = "https://github.com/xsuite/xdeps/archive/refs/tags/v0.10.21.tar.gz"

    license("Apache-2.0")

    version("0.10.21", sha256="f175fafa272a529ed7b70547b2d22b47aa709011e93e6d68db4d138e92335b21")
    version("0.10.5", sha256="080af0fceb05cf22893aecf360486db238e91e6260eb14ed51735688fdc5daca")
    version("0.10.4", sha256="280dfc5e6413edbb024afb3583051d05eac0fb089f7f9c53d9e84766bb6d71c9")
    version("0.10.3", sha256="d81331f63166b65bf1e21f13b8cb681496c7cb4e71d03f79f2ce39a53efa081a")

    # xdeps/refs.py is cythonized into a C extension.
    depends_on("c", type="build")

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-cython", type=("build", "run"))

    depends_on("py-lark", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

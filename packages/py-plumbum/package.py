from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyPlumbum(PythonPackage):
    """Plumbum: shell combinators library."""

    homepage = "https://github.com/tomerfiliba/plumbum"
    pypi = "plumbum/plumbum-2.0.2.tar.gz"

    license("MIT")

    version("2.0.2", sha256="233751d7819c9e6743ec1c2405927eb4fa52a284c7b894bd10e28106a9309a92")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-hatchling@1.27:", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-typing-extensions", type=("build", "run"), when="^python@:3.12")

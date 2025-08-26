from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXcoll(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/xsuite/xcoll"

    url = "https://github.com/xsuite/xcoll/archive/refs/tags/v0.6.2.tar.gz"

    version("0.6.2", sha256="01b65a718349a833033a0a6b8592ff1046400a24bf8c9bde8d81790ec94f496b")
    version("0.6.1", sha256="b6d608201c84f18cf142310fd678a48f2b5f2eec56957cd3f5c11274daed9c49")
    version("0.6.0", sha256="9fe100f0cfac61b531a36749b03036fd44fac93aa94e09b7ac59f344817eb6fd")
    version("0.5.12", sha256="cb48921157865ef9a47a803f0629f3ae9c8dd778a443772be65e8edeec4822fe")
    version("0.5.11", sha256="fe35139b49714678a59572564ec4c5d2db920d20be303fbaf2190421dca7e671")
    version("0.5.10", sha256="93949cf8db2f543d02643cc59d3f80e08eb7cddfbd8240adef8fd3dfc451cb10")
    version("0.5.9", sha256="5daf5fc2ecad7780732e04206029b2f13c4687b97b10ba56ea20d815d96fc8ae")
    version("0.5.8", sha256="588a4de7b3f34b5547d5380a2b54e50603c4b891a77a6927afa1c4a994b73c04")
    version("0.5.7", sha256="f875a99d94ad28fb8d4f7b04844100fbd48874c476e223cddd3e2561e6c760a9")
    version("0.5.6", sha256="941c659a3395845baa97180bd6c37be054405a0edd54e4de327bc0dc052ee45d")

    depends_on('py-numpy')
    depends_on('py-pandas')
    depends_on('py-xobjects')
    depends_on('py-xdeps')
    depends_on('py-xpart')
    depends_on('py-xtrack')
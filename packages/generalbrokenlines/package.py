from spack.pkg.k4.generalbrokenlines import Generalbrokenlines as K4Generalbrokenlines
from spack.package import *


class Generalbrokenlines(K4Generalbrokenlines):
    """GeneralBrokenLines, overridden to fetch from DESY GitLab.

    key4hep-spack fetches the V02 releases from the old GitHub mirror
    (github.com/GeneralBrokenLines/GeneralBrokenLines). Around 2026-11-15 that
    mirror was replaced by a sync of the upstream DESY GitLab repository: the
    tags were re-pointed to the GitLab commits, whose tree keeps the C++ library
    under cpp/ (next to fortran/ and python/) instead of at the top level. That
    broke both the key4hep sha256 pins and the top-level CMakeLists.txt the
    recipe expects. Fetch the tags from the canonical GitLab location instead
    (as spack-packages' builtin recipe does for V04) and build from cpp/.
    Only the versions key4hep-spack already provides are redeclared, so
    concretization preferences are unchanged.
    """

    __doc__ = K4Generalbrokenlines.__doc__ + (__doc__ or "")

    homepage = "https://gitlab.desy.de/millepede/general-broken-lines"
    url = "https://gitlab.desy.de/millepede/general-broken-lines/-/archive/V02-02-01/general-broken-lines-V02-02-01.tar.gz"
    git = "https://gitlab.desy.de/millepede/general-broken-lines.git"

    version("2.2.1", sha256="508b86a05463b59cb5f3415f702520fd5664ba5e59440430dae9536dbe940bf2")
    version("2.2.0", sha256="3df25a5f275a17fc9350ab78131e307c0aded5ef01b9d3fabb54d35ec954e292")
    version("2.1.3", sha256="10ca9dcb0fc125506dcceb0c8e81f5b4321186afdd1036647d59763f8f4179b0")
    version("2.1.2", sha256="16d39b4220b32c02cd1a38e662a7b4f82986f046bc2bb1d0767ae7315e49ea6a")
    version("2.1.1", sha256="9f59d93c3a19d180c0e4468cfc2282d7f0ce6d13d89faf492bb418534548b74f")
    version("2.1.0", sha256="a54999ba3944635dc1b1ae79c9fcfe4b92b8bfcbf44572fa2c356e9bd24d5dac")

    # cpp/CMakeLists.txt calls PROJECT(GBL) without LANGUAGES, which enables C
    # as well as C++; the k4 recipe only declares cxx.
    depends_on("c", type="build")

    root_cmakelists_dir = "cpp"

    def url_for_version(self, version):
        if version.isdevelop():
            return super().url_for_version(version)
        tag = "V" + "-".join(str(version[i]).zfill(2) for i in range(3))
        return f"{self.homepage}/-/archive/{tag}/general-broken-lines-{tag}.tar.gz"

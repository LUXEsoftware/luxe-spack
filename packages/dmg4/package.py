from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class Dmg4(CMakePackage):
    """Dark Matter simulations for Geant4"""

    homepage = "https://gitlab.cern.ch/P348/DMG4/-/wikis/home"
    url = "https://gitlab.cern.ch/P348/DMG4/-/archive/Version_2.5/DMG4-Version_2.5.tar.gz"
    git = "https://gitlab.cern.ch/P348/DMG4.git"

    version("2.5", sha256="374e23f589708ec302f917bf20a4010ba3d185361d93b994941d2a0275e8d7cf")
    version("2.4", sha256="d22dd47b29797138c9def4e85559625c023fc66b2d5bf8fc742bbcff4a175c9e")
    version("2.3", sha256="11c5ada8facc8a0f287cdf0a61f238aa1ba84aeb81a71455f395602e5424b15b")
    version("2.2", sha256="69423a19fa8d8a876936ff2013a1da39be75e671eeddaa6776416a5b7afc3cd6")
    version("2.1", sha256="dc4a4b8ab5a0f90c040d25c6fa266ac034b62b2b43761caa359e563501371134")
    version("2.0", sha256="1f866960edb942a9c03c4f0c1a0f18257ab1770acd63e87a2ae90cbb678ef7d2")
    version("1.2", sha256="a16a2ec543692d0b8c16f9d1384a76119cf00ccc7089aedba96302b85d0959cd")

    depends_on("cxx", type="build")

    # Match the C++ standard used to build Geant4. The DMG4 CMakeLists sets no
    # standard on the default build path (it only inherits flags from
    # Geant4_USE_FILE), so we pin it explicitly to keep the ABI consistent with
    # the Geant4 (and GSL) it links against.
    _cxxstd_values = ("11", "14", "17", "20")
    variant(
        "cxxstd",
        default="17",
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("geant4")
    depends_on("gsl")

    # Force Geant4 to the same C++ standard as DMG4.
    for _std in _cxxstd_values:
        depends_on(f"geant4 cxxstd={_std}", when=f"cxxstd={_std}")

    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]

import glob
import os

from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyXcoll(PythonPackage):
    """Xcoll: collimation in Xsuite simulations. Tracks particles through
    collimators and crystals with the built-in Everest scattering engine, or
    hands them over to Geant4 (through BDSIM) or FLUKA and back."""

    homepage = "https://github.com/xsuite/xcoll"
    url = "https://github.com/xsuite/xcoll/archive/refs/tags/v0.12.3.tar.gz"

    license("Apache-2.0")

    version("0.12.3", sha256="f79345ed0b0d5d412138d64a5d9f2bc5b7ebfe40deeb4527efd1adc3b6628081")
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

    # Geant4 hand-over (Geant4Collimator, Geant4Crystal, xc.geant4.engine) only
    # exists from 0.7.0 on; 0.5/0.6 merely define the LOST_ON_GEANT4_* states.
    # Upstream compiles the xcoll<->BDSIM pybind11 module (g4interface) lazily,
    # at runtime, into ~/.xcoll/lib via xc.geant4.interface.compile(). We build it
    # here instead, against the BDSIM of this stack, and install it into
    # site-packages so that `from g4interface import XtrackInterface` works for
    # every user out of the box (interface.compiled == True).
    variant("geant4", default=True, when="@0.7:",
            description="Build the Geant4 (BDSIM) scattering engine interface")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("python@3.10:", type=("build", "run"), when="@0.6.3:")
    depends_on("python@3.11:", type=("build", "run"), when="@0.11:")

    depends_on("py-poetry-core@1.0.8:", type="build")
    depends_on("py-poetry-core@2:", type="build", when="@0.7:")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas@1.4:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"), when="@0.7:")
    # Only needed to read CollimatorDatabase yaml files before 0.7; a hard
    # dependency since.
    depends_on("py-ruamel-yaml@0.17.31:", type=("build", "run"))
    # The Geant4 interface module imports requests at import time.
    depends_on("py-requests", type=("build", "run"), when="@0.7:")
    # Used to compile the FLUKA coupling at runtime (FLUKA itself is licensed
    # software and has to be provided by the user).
    depends_on("meson", type=("build", "run"), when="@0.9:")

    depends_on("py-xobjects@0.5:", type=("build", "run"))
    depends_on("py-xdeps@0.10.5:", type=("build", "run"))
    depends_on("py-xpart@0.23:", type=("build", "run"))
    depends_on("py-xtrack@0.84.8:", type=("build", "run"))
    with when("@0.12:"):
        depends_on("py-xobjects@0.7:", type=("build", "run"))
        depends_on("py-xdeps@0.10.21:", type=("build", "run"))
        depends_on("py-xpart@0.23.18:", type=("build", "run"))
        depends_on("py-xtrack@0.114.1:", type=("build", "run"))

    with when("+geant4"):
        # Must be the compiler family Geant4 was built with: BDSIM's CMake
        # config pulls in Geant4_CXX_FLAGS, which are compiler specific.
        depends_on("cxx", type="build")
        depends_on("cmake@3.21:", type="build")
        depends_on("py-pybind11", type=("build", "link"))
        # g4interface links libbdsim/libgmad/librebdsim; xcoll also runs
        # `bdsim --version` and looks up `bdsim` and `geant4-config` on PATH
        # before it agrees to start the engine. BDSIM <= 1.7.7 is handled by
        # patch() below, at the cost of tipped collimator jaws.
        depends_on("bdsim", type=("build", "link", "run"))
        depends_on("geant4", type=("build", "link", "run"))
        # Runs BDSIM in a separate rpyc server process so that the Geant4
        # engine can be stopped and restarted within one python session
        # ("re-entry protection"); without it a restart needs a new process.
        depends_on("py-rpyc", type="run")

    @property
    def _g4interface_src(self):
        return join_path(
            self.stage.source_path, "xcoll", "scattering_routines", "geant4", "scattering_src"
        )

    @when("+geant4 ^bdsim@:1.7.7")
    def patch(self):
        # Same source adaptation xcoll's own Geant4Interface.compile() applies
        # for BDSIM older than '1.7.7.develop' (i.e. up to the 1.7.7 release):
        # the link bunch class had its SixTrack-era name, and there is no
        # AddLinkCollimatorTipJaw, so tipped jaws fall back to plain jaws.
        with working_dir(self._g4interface_src):
            for name in ("BDSXtrackInterface.hh", "BDSXtrackInterface.cpp"):
                filter_file("BDSLinkBunch", "BDSBunchSixTrackLink", name, string=True)
                filter_file(r"^.*// BDSIM >= 1\.7\.7\.develop\s*\n", "", name)

    @run_after("install", when="+geant4")
    def build_g4interface(self):
        spec = self.spec
        build_dir = join_path(self.stage.path, "g4interface-build")
        cmake = Executable(spec["cmake"].prefix.bin.cmake)
        args = [
            "-S", self._g4interface_src,
            "-B", build_dir,
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DPython3_EXECUTABLE={spec['python'].command.path}",
            f"-DBDSIM_DIR={spec['bdsim'].prefix.lib.cmake.bdsim}",
            # Never download pybind11 from GitHub during the build.
            "-DPYBIND11_USE_FETCHCONTENT_FALLBACK=OFF",
        ]
        pybind11_cfg = glob.glob(
            join_path(spec["py-pybind11"].prefix, "**", "pybind11Config.cmake"), recursive=True
        )
        if pybind11_cfg:
            args.append(f"-Dpybind11_DIR={os.path.dirname(pybind11_cfg[0])}")
        cmake(*args)
        cmake("--build", build_dir, "--parallel", str(make_jobs))

        libs = glob.glob(join_path(build_dir, "g4interface*.so"))
        if len(libs) != 1:
            raise InstallError(f"Expected exactly one g4interface module, found {libs}")
        mkdirp(python_platlib)
        install(libs[0], python_platlib)

        # Fail the build rather than ship an xcoll whose Geant4 engine refuses
        # to start: the module must load against this stack's BDSIM/Geant4.
        spec["python"].command(
            "-c",
            f"import sys; sys.path.insert(0, {python_platlib!r}); "
            "from g4interface import XtrackInterface",
        )

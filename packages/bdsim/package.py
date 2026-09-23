from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class Bdsim(CMakePackage):
    """Beam Delivery Simulation: a Geant4 based tool that tracks particles
    through an accelerator beam line and simulates their interaction with the
    machine, writing energy deposition and sampler data to ROOT files."""

    homepage = "http://www.pp.rhul.ac.uk/bdsim/manual/"
    url = "https://github.com/bdsim-collaboration/bdsim/archive/refs/tags/v1.7.8.tar.gz"
    git = "https://github.com/bdsim-collaboration/bdsim.git"

    license("GPL-3.0-only")

    version("develop", branch="develop")
    version("1.7.8", sha256="4c43a8d53f92efcfdf00476c0298dfdb22f32926d5a7f635c8cd545c6bb04fbc")
    version("1.7.7", sha256="8923a197c97984e32651f877c35c3f759ca8d20b661aaec200b83dbd72e4d7d9")
    version("1.7.6", sha256="7740d9fb3bcc9856a36b74130fae68def878d86c6f7e4a54c9d7a2db8dd770bc")
    version("1.7.5", sha256="d34a7643c7426f23c2fe94ffb0de33e0387d1607ed82cb1f32d798f50ad51194")
    version("1.7.4", sha256="a6f889a8a070c430908b3613704a0725bb4f4a4dae0820dbae12fe165038a333")
    version("1.7.3", sha256="06351d9df695891731e2a92d6795a0526d538faabbd4091e3e0bded1026127f6")
    version("1.7.2", sha256="f4ff6d43b5f3c403e9241957ee70733f48c0f3f1fa9fd8d17fc57b2e0b3799a0")
    version("1.7.1", sha256="079282dd301e76c8d97b4bc8d5ff26bb2588214f609c1e88ffddfc24859212c9")
    version("1.7.0", sha256="519bdede40470907d3305556ed5cf9523a2d7c0446db764338741d0ca43a86b4")

    # BDSIM never takes the C++ standard from us: cmake/Geant4.cmake inspects
    # Geant4_CXX_FLAGS and *overrides* CMAKE_CXX_STANDARD with whatever standard
    # Geant4 was compiled with (a -DCMAKE_CXX_STANDARD on the command line is
    # shadowed by the plain set() at the top of the top-level CMakeLists). This
    # variant therefore does not configure BDSIM itself - it pins the standard of
    # the stack BDSIM compiles and links against, which is what actually decides
    # the ABI. Keeping geant4 and root on the same standard here avoids linking a
    # C++11 Geant4 against a C++17 ROOT.
    _cxxstd_values = ("11", "14", "17", "20")
    variant(
        "cxxstd",
        default="17",
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("gdml", default=True, description="Load GDML geometry (needs Xerces-C)")
    variant("gzstream", default=True, description="Compressed (gzip) input/output support")
    variant("boost", default=False, description="4D differential flux scorers (cellflux4d)")
    variant("hepmc3", default=False, description="Load event generator files with HepMC3")
    variant("hdf5", default=False, description="HDF5 field maps for the plasma module")
    variant("python", default=False, description="Build the pybind11 python bindings")
    variant("event_display", default=False, description="ROOT EVE based event display")
    variant(
        "double_output",
        default=False,
        description="Double precision output - doubles the output file size",
    )

    # project(bdsim LANGUAGES CXX) - no C compiler is ever probed.
    depends_on("cxx", type="build")

    depends_on("cmake@3.10:", type="build")
    # The gmad input language parser is generated at build time.
    depends_on("bison@2.4:", type="build")
    depends_on("flex", type="build")

    # cmake/Geant4.cmake aborts the configure ("Currently Geant4 builds with
    # multithreading are not supported") when Geant4_DEFINITIONS contains
    # G4MULTITHREADED, so Geant4 has to be serial. Note that under a unified
    # environment this pulls the whole stack onto geant4~threads.
    depends_on("geant4@10.7: ~threads")
    depends_on("clhep")
    depends_on("root@6:")

    # Geant4's spack recipe always enables GEANT4_USE_GDML, so the configure-time
    # check that Geant4 can read GDML is always satisfied; BDSIM links Xerces-C
    # itself on top of that.
    depends_on("xerces-c", when="+gdml")

    # Spack's geant4 uses the system zlib (GEANT4_USE_SYSTEM_ZLIB), so the
    # gzstream library falls through to find_package(ZLIB) rather than to
    # Geant4's builtin one.
    depends_on("zlib-api", when="+gzstream")

    depends_on("boost@1.71: +system", when="+boost")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("hdf5 +cxx", when="+hdf5")
    depends_on("root +opengl", when="+event_display")

    with when("+python"):
        depends_on("python@3.8:", type=("build", "run"))
        depends_on("py-pybind11", type=("build", "link"))

    # Keep the C++ standard consistent across the pieces BDSIM links together.
    # clhep follows from geant4, which already pins its clhep to its own cxxstd.
    for _std in _cxxstd_values:
        depends_on(f"geant4 cxxstd={_std}", when=f"cxxstd={_std}")
        depends_on(f"root cxxstd={_std}", when=f"cxxstd={_std}")

    def cmake_args(self):
        args = [
            self.define_from_variant("USE_GDML", "gdml"),
            self.define_from_variant("USE_GZSTREAM", "gzstream"),
            self.define_from_variant("USE_BOOST", "boost"),
            self.define_from_variant("USE_HEPMC3", "hepmc3"),
            self.define_from_variant("USE_PLASMA_HDF5", "hdf5"),
            self.define_from_variant("USE_PYTHON_BINDINGS", "python"),
            self.define_from_variant("USE_EVENT_DISPLAY", "event_display"),
            self.define_from_variant("USE_ROOT_DOUBLE_OUTPUT", "double_output"),
            # BDSIM ships its own FindROOT.cmake, which shells out to root-config
            # found via ROOTSYS or PATH instead of going through
            # CMAKE_PREFIX_PATH. Point it at the root of this spec explicitly.
            self.define(
                "ROOT_CONFIG_EXECUTABLE", self.spec["root"].prefix.bin.join("root-config")
            ),
        ]

        if self.spec.satisfies("+python"):
            args.append(self.define("Python_EXECUTABLE", self.spec["python"].command.path))

        return args

    def setup_run_environment(self, env):
        # What the installed bin/bdsim.sh sets up: rebdsim and bare ROOT need the
        # BDSIM headers to interpret the classes stored in the output files.
        env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include.bdsim)
        env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include.bdsim.analysis)
        env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include.bdsim.parser)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        if self.spec.satisfies("+python"):
            # The bindings are installed to lib/python/bdsim, not to site-packages.
            env.prepend_path("PYTHONPATH", self.prefix.lib.python)

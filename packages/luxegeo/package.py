from spack.package import *

class Luxegeo(CMakePackage):
    """dd4hep-style geometry description for LUXE detectors"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/LUXEsoftware/luxegeo"
    git = "https://github.com/LUXEsoftware/luxegeo"

    # FIXME: Add proper versions and checksums here.
    version("main", branch="main")

    depends_on("cxx", type="build")

    depends_on("lcio")
    depends_on("dd4hep")
    depends_on("root")
    depends_on("python", type="build")
    depends_on("ninja", type="build")
    depends_on("podio")

    def cmake_args(self):
        args = []  
        args.append(self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'))
        return args
    
    def setup_run_environment(self, env):
        env.set("luxegeo_DIR", self.prefix.share.luxegeo)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["luxegeo"].libs.directories[0])

    def setup_build_environment(self, env):
        env.set("luxegeo_DIR", self.prefix.share.luxegeo)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["lcio"].libs.directories[0])
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("luxegeo_DIR", self.prefix.share.luxegeo)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["luxegeo"].libs.directories[0])
        env.prepend_path("LD_LIBRARY_PATH", self.spec["lcio"].libs.directories[0])

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("luxegeo_DIR", self.prefix.share.luxegeo)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["luxegeo"].libs.directories[0])
        env.prepend_path("LD_LIBRARY_PATH", self.spec["lcio"].libs.directories[0])

    # dd4hep tests need to run after install step:
    # disable the usual check
    def check(self):
        pass

    # instead add custom check step that runs after installation
    @run_after("install")
    def install_check(self):
        print(self)
        with working_dir(self.build_directory):
            if self.run_tests:
                ninja("test")
from spack.package import *
from spack.pkg.k4.key4hep_stack import *

class Lxsim(CMakePackage, Key4hepPackage):
    """LUXE simulation framework"""

    homepage = "https://github.com/LUXEsoftware/lxsim"
    git      = "https://github.com/LUXEsoftware/lxsim.git"
    url      = "https://github.com/LUXEsoftware/lxsim/archive/refs/tags/v00-01.tar.gz"

    maintainers = ['']

    version('bsm_npod_calice_ecal_g4v11',  branch='bsm_npod_calice_ecal_g4v11')

    depends_on('geant4')
    depends_on('doxygen')
    depends_on('glib')

    def cmake_args(self):
        args = []  
        args.append(self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'))
        args.append(self.define('BUILD_TESTING', self.run_tests))
        return args

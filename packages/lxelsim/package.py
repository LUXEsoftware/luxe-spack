from spack.package import *
from spack.pkg.k4.key4hep_stack import *

class Lxelsim(CMakePackage, Key4hepPackage):
    """LUXE simulation framework"""

    homepage = "https://github.com/LUXEsoftware/lxelsim"
    git      = "https://github.com/LUXEsoftware/lxelsim.git"
    url      = "https://github.com/LUXEsoftware/lxelsim/archive/refs/tags/v00-01.tar.gz"

    maintainers = ['']

    version('master',  branch='master')

    depends_on('geant4')
    depends_on('doxygen')
    depends_on('glib')
    depends_on('hdf5 +cxx +hl')

    def cmake_args(self):
        args = []  
        args.append(self.define('CMAKE_CXX_STANDARD', '20'))
        #args.append(self.define('BUILD_TESTING', self.run_tests))
        return args

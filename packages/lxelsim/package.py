from spack.package import *
from spack.pkg.k4.key4hep_stack import *

import os

class Lxelsim(CMakePackage, Key4hepPackage):
    """LUXE simulation framework"""

    homepage = "https://github.com/LUXEsoftware/lxelsim"
    git      = "https://github.com/LUXEsoftware/lxelsim.git"
    url      = "https://github.com/LUXEsoftware/lxelsim/archive/refs/tags/v00-01.tar.gz"

    maintainers = ['madbaron']

    version('master',  branch='master')

    depends_on('geant4')
    depends_on('doxygen')
    depends_on('glib')
    depends_on('hdf5')

    def cmake_args(self):
        args = []
        args.append(self.define('CMAKE_CXX_STANDARD', '20'))

        # Ensure CMake/Find modules pick up Spack-installed HDF5
        h5 = self.spec['hdf5']
        h5_prefix = str(h5.prefix)

        # If the HDF5 CMake package config directory exists, point CMake to it
        h5_cmake_dir = os.path.join(h5_prefix, 'lib', 'cmake', 'HDF5')
        if os.path.isdir(h5_cmake_dir):
            args.append(self.define('HDF5_DIR', h5_cmake_dir))

        # Always provide HDF5 root and add it to CMAKE_PREFIX_PATH as a robust fallback
        args.append(self.define('HDF5_ROOT', h5_prefix))

        # Extend CMAKE_PREFIX_PATH so find_package searches Spack prefixes first
        # Use semicolon-separated list which CMake expects
        cmake_prefix_path = ';'.join(filter(None, [h5_prefix, str(self.spec.prefix)]))
        args.append(self.define('CMAKE_PREFIX_PATH', cmake_prefix_path))

        # Provide explicit include directory if present (fallback)
        h5_include = os.path.join(h5_prefix, 'include')
        if os.path.isdir(h5_include):
            args.append(self.define('HDF5_INCLUDE_DIRS', h5_include))

        # Provide explicit library paths for common HDF5 libs as a fallback
        lib_dir = os.path.join(h5_prefix, 'lib')
        if os.path.isdir(lib_dir):
            libs = []
            for libname in ('libhdf5.so', 'libhdf5.a', 'libhdf5_hl.so', 'libhdf5_hl.a'):
                lp = os.path.join(lib_dir, libname)
                if os.path.exists(lp):
                    libs.append(lp)
            if libs:
                args.append(self.define('HDF5_LIBRARIES', ';'.join(libs)))

        return args

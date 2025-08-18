from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from spack.package import *
from spack.pkg.k4.key4hep_stack import *

class LuxeStack(BundlePackage, Key4hepPackage):
    """Bundle package to install LUXE Software Stack"""
    
    homepage = 'https://github.com/LUXEsoftware'
    
    maintainers = ['madbaron']

    ##################### versions ########################
    #######################################################
    ###  nightly build
    version(datetime.today().strftime('%Y-%m-%d'))

    version("main", branch="main")

    ### stable build
    #version('0.1')

    # this bundle package installs a custom setup script,
    # so need to add the install phase
    # (normally doesn't exist for a bundle package)
    phases = ['install']

    variant('devtools', default=True,
            description='add tools necessary for software development to the stack')
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('llvm', default=False, description='Build with LLVM')
    variant('ml', default=False, description='Build with machine learning tools')
    variant('pytools', default=False, description='Build with python tools')

    # Add compilers to the build dependencies
    # so that we have them available to set them in the env script
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on('root')
    depends_on('dd4hep')

    ##################### developer tools #################
    #######################################################
    with when('+devtools'):
        depends_on('cmake')
        depends_on('ninja')
        depends_on('doxygen')
        depends_on('gdb')

    depends_on('llvm', when='+llvm')

    with when('+ml'):
        # ML tools
        depends_on('onnx')
        depends_on('xgboost')
        depends_on('py-onnxruntime')
        depends_on('py-onnx')

    with when('+pytools'):
        # Python tools
        depends_on('py-h5py')
        depends_on('py-ipython')
        # depends_on('py-jupytext') # this requires rust and node-js which take too long to compile
        depends_on('py-matplotlib')
        depends_on('py-pandas')
        depends_on('py-particle')
        depends_on('py-pip')
        depends_on('py-scikit-learn')
        depends_on('py-scipy')
        depends_on('py-uproot')
        depends_on('py-xgboost')


    def setup_run_environment(self, env):
        # set locale to avoid certain issues with xerces-c
        # (see https://github.com/key4hep/key4hep-spack/issues/170)
        env.set("LC_ALL", "C")
        env.set('LUXE_STACK', os.path.join(self.spec.prefix, 'setup.sh'))
        env.set('LUXE_RELEASE_VERSION', self.spec.version)

        # ROOT needs to be in LD_LIBRARY_PATH to prevent using system installations
        env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        env.prepend_path("PYTHONPATH", self.spec["root"].prefix.lib)

        # set vdt, needed for root, see https://github.com/spack/spack/pull/37278
        if "vdt" in self.spec:
            env.prepend_path("CPATH", self.spec["vdt"].prefix.include)
            # When building podio with +rntuple there are warnings constantly without this
            env.prepend_path("LD_LIBRARY_PATH", self.spec["vdt"].libs.directories[0])

    def install(self, spec, prefix):
        return install_setup_script(self, spec, prefix, 'LUXE_LATEST_SETUP_PATH')

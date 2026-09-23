from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyPica(PythonPackage):
    """PICA (Polarized ICS CAlculator): Monte Carlo code for the simulation of
    Inverse Compton Scattering gamma-ray spectra including the photon
    polarization. Output is HDF5 in a PTARMIGAN-compatible format."""

    homepage = "https://github.com/hixps/pica"
    git = "https://github.com/hixps/pica.git"
    url = "https://github.com/hixps/pica/archive/refs/tags/v1.2.9.tar.gz"

    license("GPL-3.0-only")

    # main is well ahead of the only tag (config refactor, yaml float loading
    # fix, dacite-based input parsing) while still reporting __version__ 1.2.9.
    version("main", branch="main")
    version("1.2.9", sha256="3334d833ef9d18722cef5551f1b2ba6a52ad370b2434660c5480982816e09cd8")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-setuptools@61:", type="build")

    depends_on("py-numpy@2:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-dacite", type=("build", "run"), when="@main")

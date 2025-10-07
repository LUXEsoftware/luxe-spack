from spack_repo.builtin.build_systems.generic import Package
from spack.package import *


class Luxegeo(Package):
    """dd4hep-style geometry description for LUXE detectors"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/LUXEsoftware/luxegeo"
    git = "https://github.com/LUXEsoftware/luxegeo"

    # FIXME: Add proper versions and checksums here.
    version("main", branch="main")

    depends_on("dd4hep")

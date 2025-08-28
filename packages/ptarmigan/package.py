from spack_repo.builtin.build_systems.cargo import CargoPackage
from spack.package import *


class Ptarmigan(CargoPackage):
    """Simulate the interaction between a high-energy particle beam and an intense laser pulse"""

    homepage = "https://tgblackburn.github.io/ptarmigan/"
    url = "https://github.com/tgblackburn/ptarmigan/archive/refs/tags/v1.4.2.tar.gz"

    maintainers("tgblackburn")

    license("Apache-2.0", checked_by="tgblackburn")

    version("1.4.2", sha256="b873b99526a9699bd219091b7c2546968a987ae6b6523529cb0f9f81840cb5da")
    version("1.3.5", sha256="3ea818b8a3ffa547588a824d55c9859a1b4d552c436567b56cf404ca58af4c88")
    version("1.3.2", sha256="1ee8c5f093e8c7dd9d29845805974468a1c2c8c07fb8757e8a151271d7d679e5")
    version("1.2.1", sha256="e618168ce0e422933a4dad55503bffaa99b2b21e32834a294091ed26404dd4b7")
    version("1.1.0", sha256="009f1ed88deb7c792e1f778d9be3e1be3faa1f147f5880ca6f94347dc9c284e1")

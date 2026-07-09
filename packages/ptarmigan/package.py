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

    variant("mpi", default=False, description="Enable MPI support")
    variant("hdf5", default=False, description="Enable HDF5 output support")

    depends_on("mpi", when="+mpi", type="build")
    depends_on("hdf5", when="+hdf5", type="build")
    depends_on("hdf5+mpi", when="+mpi+hdf5", type="build")

    # Building the MPI Rust bindings (the `mpi-sys`/`cc` crates compile a C shim,
    # `bindgen` needs libclang) pulls in a C compiler. As a CargoPackage, ptarmigan
    # otherwise declares no language dependency, so there would be no compiler node
    # for the `%clang` requirement below to bind to and concretization would fail
    # with "requires the Clang compiler" even when clang is registered with spack.
    depends_on("c", type="build", when="+mpi")

    # Upstream documents MPI builds as requiring Clang.
    requires("%clang", when="+mpi", msg="Ptarmigan +mpi requires the Clang compiler")

    def setup_build_environment(self, env):
        # super() reaches CargoBuilder.setup_build_environment (sets CARGO_HOME);
        # must be kept or the cargo build breaks.
        super().setup_build_environment(env)
        # The hdf5-output feature pulls the `hdf5-sys` crate, whose build script
        # locates HDF5 via the HDF5_DIR env var (falling back to pkg-config /
        # system paths). Point it explicitly at the hdf5 spack dependency so it
        # uses our +mpi HDF5 instead of failing to find one ("panicked at
        # hdf5-sys .../build.rs"). bindgen (via mpi-sys) also needs libclang; the
        # llvm dependency provides it and clang is on PATH.
        if self.spec.satisfies("+hdf5"):
            env.set("HDF5_DIR", self.spec["hdf5"].prefix)

    @property
    def build_args(self):
        # --locked: build against the committed Cargo.lock (vergen 4.0.3 + git2
        # 0.18.2). `cargo install` ignores Cargo.lock by default and re-resolves,
        # which bumps vergen to 4.2.0 and git2 to 0.21.0 -- and vergen 4.2.0 does
        # not compile against git2 0.21.0 ("could not compile `vergen`", E0308).
        # Pinning to the lockfile keeps the known-good crate versions. This is
        # independent of the C compiler (it fails the same way with gcc or clang).
        args = ["--locked"]
        features = []

        if "+mpi" in self.spec:
            features.append("with-mpi")

        if "+hdf5" in self.spec:
            features.append("hdf5-output")

        if features:
            args.extend(["--features", ",".join(features)])

        return args
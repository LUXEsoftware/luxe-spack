from spack_repo.builtin.packages.py_llvmlite.package import PyLlvmlite as BuiltinPyLlvmlite
from spack.package import *


class PyLlvmlite(BuiltinPyLlvmlite):
    """llvmlite, overridden to disable LTO.

    llvmlite's FFI CMake build hard-requires -flto (LLVMLITE_FLTO defaults ON)
    and aborts with FATAL_ERROR "-flto flag is not supported by the compiler"
    when its `check_cxx_compiler_flag(-flto ...)` probe fails. Under the spack
    clang compiler-wrapper that probe fails spuriously (a plain
    `clang -flto` compile+link through the same wrapper succeeds and uses the
    LLVMgold plugin), which breaks py-llvmlite -> py-numba -> py-xsuite on the
    all-clang stack. LTO is a link-time optimization only, so turn it off via the
    LLVMLITE_FLTO env var that ffi/build.py reads; the resulting libllvmlite is
    functionally identical.
    """

    __doc__ = BuiltinPyLlvmlite.__doc__ + (__doc__ or "")

    def setup_build_environment(self, env):
        super().setup_build_environment(env)
        env.set("LLVMLITE_FLTO", "OFF")

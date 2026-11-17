from spack.pkg.k4.generalbrokenlines import Generalbrokenlines as K4Generalbrokenlines
from spack.package import *


class Generalbrokenlines(K4Generalbrokenlines):
    """GeneralBrokenLines, overridden to fetch tagged versions by git commit.

    key4hep-spack pins these versions by the sha256 of GitHub's auto-generated
    /archive/V0X-YY-ZZ.tar.gz tarballs. Around 2026-11-15 GitHub regenerated
    those archives for this repository (the top-level directory lost its "V"
    prefix), so every tarball checksum changed although the tags still point to
    the same commits (cross-checked against gitlab.desy.de). Pinning the tag
    commits instead keeps the source identical and is immune to archive churn.
    Only the versions key4hep-spack already provides are redeclared, so
    concretization preferences are unchanged.
    """

    __doc__ = K4Generalbrokenlines.__doc__ + (__doc__ or "")

    version("2.2.1", commit="455c39beb3e0b81fa4085d88da8acbd5f17c2c6c")
    version("2.2.0", commit="206a72f15dab9c8ed405b1cfb367b374fb0528f5")
    version("2.1.3", commit="8acaade19c20e9ef23d1244a555fead6ef149c33")
    version("2.1.2", commit="d83681db9bebe68a635a21e2df09d1f27995185f")
    version("2.1.1", commit="e600882aa1303a8d789329d2117919666c9948fe")
    version("2.1.0", commit="5973c0a629721be5b7a44d2d06507c753d5d54c1")

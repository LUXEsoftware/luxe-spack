# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetry(PythonPackage):
    """Python dependency management and packaging made easy."""

    homepage = "https://python-poetry.org/"
    pypi = "poetry/poetry-1.1.12.tar.gz"

    license("MIT")
    url = "https://github.com/python-poetry/poetry/archive/refs/tags/2.1.4.tar.gz"

    version("2.1.4", sha256="77698481d9b330478ca6a2435303c409ff60d7b790fc06895e33f6d797347876")
    version("2.1.3", sha256="9a847496ac6d5b1c15f9252c8382c5a478c9a9bffb9d3712f2c084df3eb11fab")
    version("2.1.2", sha256="e674047e4730f0898789c8a1274e99f346edea130f4bd4ecf8189e40786723df")
    version("2.1.1", sha256="1e33bc9c202d08ebde998bcb151f5f18ef56e70be0b10d126e831b78e337c046")
    version("2.1.0", sha256="2ae1ab9f063a83fa6159647791c54629e55370de6ae8224de5507b481cb1ecc1")
    version("2.0.1", sha256="9e9f7a7b868338e40134f2e705bc5162fc0779043083b926e434963cf39e806a")
    version("2.0.0", sha256="ba4a93bd8e9c3668fab4e42215ddd85cbcddb9c02bdd9baf6291feef983dd32c")
    version("1.8.5", sha256="c42471ed067606f9d33678d729a1b9e6e70341faeabfff32f2f406892740ee0d")
    version("1.8.4", sha256="bdfee484c70e9de6c7ce5869c0693dd592b95e77ecdf8e3edd2fd3b9745db19a")
    version("1.8.3", sha256="4da8d1b19cfb50536c6b54e984b88cec3bc1203f9749d5f4958db5cbb0c7b7bc")

    depends_on("c", type="build")

    depends_on("python@3.8:3", when="@1.6.0:", type=("build", "run"))
    depends_on("python@3.7:3", when="@1.2.0:", type=("build", "run"))
    depends_on("python@2.7,3.5:3", type=("build", "run"))
    depends_on("py-poetry-core@1.7.0", when="@1.6.1", type=("build", "run"))
    depends_on("py-poetry-core@1.2.0", when="@1.2.1", type=("build", "run"))
    depends_on("py-poetry-core@1.1.0", when="@1.2.0", type=("build", "run"))
    depends_on("py-poetry-core@1.0.7:1.0", when="@:1.1", type=("build", "run"))
    depends_on("py-poetry-plugin-export@1.5.0:1", when="@1.6.1", type=("build", "run"))
    depends_on("py-poetry-plugin-export@1.0.7:1", when="@1.2.1:", type=("build", "run"))
    depends_on("py-poetry-plugin-export@1.0.6:1", when="@1.2.0:", type=("build", "run"))
    depends_on(
        "py-backports-cached-property@1.0.2:1", when="@1.2.1:^python@:3.7", type=("build", "run")
    )
    depends_on("py-cachecontrol@0.13+filecache", when="@1.6.1", type=("build", "run"))
    depends_on("py-cachecontrol@0.12.9:0.12+filecache", when="@1.2.1:1.2", type=("build", "run"))
    depends_on("py-cachy@0.3.0:0.3", when="@:1.2", type=("build", "run"))
    depends_on("py-cleo@2", when="@1.6.1", type=("build", "run"))
    depends_on("py-cleo@1", when="@1.2", type=("build", "run"))
    depends_on("py-cleo@0.8.1:0.8", when="@:1.1", type=("build", "run"))
    depends_on("py-clikit@0.6.2:0.6", when="@:1.1", type=("build", "run"))
    depends_on("py-crashtest@0.4.1:0.4", when="@1.6.1", type=("build", "run"))
    depends_on("py-crashtest@0.3", when="@:1.2", type=("build", "run"))
    depends_on("py-html5lib@1.0:1", when="@:1.2", type=("build", "run"))
    depends_on("py-importlib-metadata@4.4:", when="@1.2: ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-metadata@1.6:1", when="@:1.1 ^python@:3.7", type=("build", "run"))
    depends_on("py-jsonschema@4.10.0:4.17", when="@1.6.1", type=("build", "run"))
    depends_on("py-jsonschema@4.10.0:4", when="@1.2:", type=("build", "run"))
    depends_on("py-keyring@24", when="@1.6.1", type=("build", "run"))
    depends_on("py-keyring@21.2.0:", when="@1.1.13:", type=("build", "run"))
    depends_on("py-keyring@21.2.0:21", when="@1.1.12 ^python@3.6:3", type=("build", "run"))
    depends_on("py-packaging@20.4:", when="@1.2:", type=("build", "run"))
    depends_on("py-packaging@20.4:20", when="@:1.1", type=("build", "run"))
    depends_on("py-pexpect@4.7:4", type=("build", "run"))
    depends_on("py-pkginfo@1.9.4:1", when="@1.6.1", type=("build", "run"))
    depends_on("py-pkginfo@1.5:1", when="@1.2:", type=("build", "run"))
    depends_on("py-pkginfo@1.4:1", when="@:1.1", type=("build", "run"))
    depends_on("py-platformdirs@3", when="@1.6.1", type=("build", "run"))
    depends_on("py-platformdirs@2.5.2:2", when="@1.2", type=("build", "run"))
    depends_on("py-requests@2.26:2", when="@1.6.1", type=("build", "run"))
    depends_on("py-requests@2.18:2", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.9.1:1", when="@1.6.1", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.9.1:0.9", when="@:1.2", type=("build", "run"))
    depends_on("py-shellingham@1.5:1", when="@1.2:", type=("build", "run"))
    depends_on("py-shellingham@1.1:1", when="@:1.1", type=("build", "run"))
    depends_on("py-tomlkit@0.11.4:0", when="@1.6.1", type=("build", "run"))
    depends_on("py-tomlkit@0.11.1,0.11.4:0", when="@1.2", type=("build", "run"))
    depends_on("py-tomlkit@0.7:0", when="@:1.1", type=("build", "run"))
    depends_on("py-virtualenv@20.22.0:20", when="@1.6.1", type=("build", "run"))
    depends_on("py-virtualenv@20.4.3:20.4.4,20.4.7:", when="@1.2", type=("build", "run"))
    depends_on("py-virtualenv@20.0.26:20", when="@:1.1", type=("build", "run"))
    depends_on("py-xattr@0.10", when="platform=darwin @1.6.1", type=("build", "run"))
    depends_on("py-xattr@0.9.7:0.9", when="platform=darwin @1.2")
    depends_on("py-urllib3@1.26.0:1", when="@1.2")
    depends_on("py-dulwich@0.21.2:0.21", when="@1.6.1", type=("build", "run"))
    depends_on("py-dulwich@0.20.46:0.20", when="@1.2.1")
    depends_on("py-dulwich@0.20.44:0.20", when="@1.2.0")
    depends_on("py-build@0.10", when="@1.6.1", type=("build", "run"))
    depends_on("py-installer@0.7.0:0.7", when="@1.6.1", type=("build", "run"))
    depends_on("py-pyproject-hooks@1", when="@1.6.1", type=("build", "run"))
    depends_on("py-tomli@2.0.1:2", when="@1.6.1^python@:3.10", type=("build", "run"))
    depends_on("py-trove-classifiers@2022.5.19:", when="@1.6.1", type=("build", "run"))
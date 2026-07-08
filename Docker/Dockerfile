###############################################################################
#  Repository: ${IMAGE}/luxe-sw
###############################################################################

FROM ubuntu:24.04

# --------------------------------------------------------------------------- #
#  System packages 
# --------------------------------------------------------------------------- #
RUN apt update && apt install -y wget && \
    wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc && \
    echo "deb http://apt.llvm.org/noble/ llvm-toolchain-noble-20 main" | tee /etc/apt/sources.list.d/llvm-20.list

# Install pre-compiled LLVM binaries to avoid expensive source builds in CI.
# llvm-20-dev is REQUIRED (not just the llvm-20 runtime/tools package):
# py-llvmlite's FFI does `find_package(LLVM REQUIRED CONFIG)` and links
# statically against LLVM, so it needs the LLVM CMake exports
# (/usr/lib/llvm-20/lib/cmake/llvm/LLVMConfig.cmake), the headers
# (/usr/lib/llvm-20/include) and the static archives (libLLVM*.a) - all of
# which ship in llvm-20-dev, not in llvm-20. Without it, find_package fails
# immediately and py-llvmlite (-> py-numba -> py-pandas -> py-xsuite) crashes.
# libzstd-dev/zlib1g-dev are also needed so LLVM's CMake exports (LLVMSupport ->
# zstd::libzstd_shared, ZLIB::ZLIB) resolve when py-llvmlite links against LLVM.

RUN apt update -y && apt upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    build-essential git python3 unzip gfortran file curl wget pkg-config rsync tzdata libgl1-mesa-dev libglu1-mesa libglu1-mesa-dev libkrb5-dev \
    llvm-20 llvm-20-dev clang-20 lld-20 libzstd-dev zlib1g-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    echo ". $HOME/.cargo/env" > ${HOME}/setup_env.sh

# --------------------------------------------------------------------------- #
#  Bootstrap spack + spack-packages.
#  Pins are supplied at build time by CI, resolved from the key4hep-spack repo:
#    SPACK_COMMIT          <- key4hep-spack/.latest-commit
#    SPACK_PACKAGES_COMMIT <- key4hep-spack/.latest-packages-commit
#    KEY4HEP_SPACK_SHA     <- key4hep-spack main HEAD (the SHA the pins were read from)
# --------------------------------------------------------------------------- #
ENV SPACK_COLOR="always"
ARG SPACK_COMMIT
ARG SPACK_PACKAGES_COMMIT

# Setting up Spack
RUN git clone https://github.com/spack/spack.git /opt/spack && \
    echo "export SPACK_ROOT=/opt/spack" >> /opt/setup_spack.sh && \
    echo ". /opt/spack/share/spack/setup-env.sh" >> /opt/setup_spack.sh && \
    echo "alias setup_spack=\". /opt/setup_spack.sh\"" >> /etc/profile.d/aliases.sh && \
    if [ -n "${SPACK_COMMIT}" ]; then cd /opt/spack && git checkout ${SPACK_COMMIT}; fi

# Checkout spack packages and register them as the builtin repo
RUN . /opt/setup_spack.sh && \
    git clone https://github.com/spack/spack-packages /opt/spack-packages && \
    cd /opt/spack-packages && \
    if [ -n "${SPACK_PACKAGES_COMMIT}" ]; then git checkout ${SPACK_PACKAGES_COMMIT}; fi && \
    spack repo set --destination "/opt/spack-packages" builtin

# Configure spack: padded install paths (buildcache relocation) and system compilers.
# Register gcc/gfortran (build-essential). clang is NOT registered here on purpose:
# the LLVM 20 clang compiler is declared authoritatively (with its compiler paths)
RUN . /opt/setup_spack.sh && \
    spack config add 'config:install_tree:padded_length:128' && \
    spack compiler find

# --------------------------------------------------------------------------- #
#  Add the key4hep-spack repository (the `k4` namespace luxe-stack imports
#  from, and where most externals / key4hep packages are defined). 
# --------------------------------------------------------------------------- #
ARG KEY4HEP_SPACK_REPO=key4hep/key4hep-spack
ARG KEY4HEP_SPACK_SHA
RUN . /opt/setup_spack.sh && \
    REPOPATH=${SPACK_ROOT}/var/key4hep-spack && \
    git clone https://github.com/${KEY4HEP_SPACK_REPO} ${REPOPATH} && \
    cd ${REPOPATH} && \
    if [ -n "${KEY4HEP_SPACK_SHA}" ]; then git checkout ${KEY4HEP_SPACK_SHA}; fi

# Apply key4hep's patches to spack packages, then register the repo
RUN . /opt/setup_spack.sh && \
    REPOPATH=${SPACK_ROOT}/var/key4hep-spack && \
    cd /opt/spack-packages && \
    . ${REPOPATH}/.cherry-pick

RUN . /opt/setup_spack.sh && \
    spack repo add ${SPACK_ROOT}/var/key4hep-spack

# --------------------------------------------------------------------------- #
#  LUXE-specific bootstrap 
# --------------------------------------------------------------------------- #
ARG LUXE_SHA=80aa392e12b7e553f7dbfb099adb7c0e67b80924
ARG GITHUB_REPOSITORY=LUXEsoftware/luxe-spack

# Adding repository: LUXE
RUN . /opt/setup_spack.sh && \
    REPOPATH=${SPACK_ROOT}/var/luxe-spack && \
    git clone https://github.com/${GITHUB_REPOSITORY} ${REPOPATH} && \
    cd ${REPOPATH} && \
    git checkout ${LUXE_SHA}

# Apply our patches to spack (after key4hep's: overrides py-numba/py-llvmlite for LLVM 20)
RUN . /opt/setup_spack.sh && \
    REPOPATH=${SPACK_ROOT}/var/luxe-spack && \
    cd /opt/spack-packages && \
    . ${REPOPATH}/.cherry-pick

# Add the package repositories
ARG SPACK_BUILDCACHE
ARG OCI_USERNAME
RUN . /opt/setup_spack.sh && \
    spack repo add ${SPACK_ROOT}/var/luxe-spack && \
    if [ -n "${SPACK_BUILDCACHE}" ]; then \
        spack mirror add --oci-username "${OCI_USERNAME}" --oci-password-variable OCI_PASSWORD --unsigned --autopush local-buildcache "${SPACK_BUILDCACHE}";\
    fi

# Create the release environment
RUN . /opt/setup_spack.sh && \
    cd ${SPACK_ROOT}/var/luxe-spack/environments/luxe-release && \
    spack env activate . && \
    cd - && \
    echo ". /opt/setup_spack.sh" >> ${HOME}/setup_env.sh && \
    echo "cd ${SPACK_ROOT}/var/luxe-spack/environments/luxe-release" >> ${HOME}/setup_env.sh && \
    echo "spack env activate ." >> ${HOME}/setup_env.sh && \
    echo "cd -" >> ${HOME}/setup_env.sh && \
    echo "spack env status" >> ${HOME}/setup_env.sh

# Concretizing the LUXE stack reusing system rust as external.
RUN --mount=type=secret,id=ocipass \
    . ${HOME}/setup_env.sh && \
    OCI_PASSWORD=$(cat /run/secrets/ocipass) spack external find rust --not-buildable && \
    OCI_PASSWORD=$(cat /run/secrets/ocipass) spack concretize --reuse

# Installing fragments of dependency tree in separate layers for cached debugging
ENV SPACK_INSTALL_OPTS="--only-concrete --no-add --fail-fast"

RUN --mount=type=secret,id=ocipass \
    . ${HOME}/setup_env.sh && \
    OCI_PASSWORD=$(cat /run/secrets/ocipass) spack install ${SPACK_INSTALL_OPTS} && \
    spack env deactivate && \
    spack gc -y && \
    spack clean -a && \
    { spack mirror remove local-buildcache || true; }

RUN . ${HOME}/setup_env.sh && \
    LUXE_STACK_PATH=$(spack find --format "{prefix}" luxe-stack) && \
    LUXE_STACK_PATH_CLEANED=$(echo ${LUXE_STACK_PATH} | sed -E 's/\x1b\[[0-9;]*m//g') && \
    echo "source ${LUXE_STACK_PATH_CLEANED}/setup.sh" > /opt/setup_luxe.sh && \
    echo "alias setup_luxe=\". ${LUXE_STACK_PATH_CLEANED}/setup.sh\"" >> /etc/profile.d/aliases.sh

# Setting up users to be used for the local environment setup
RUN useradd --shell /bin/bash --create-home luxe
USER luxe
WORKDIR /home/luxe

# Auto-source the LUXE environment when starting a container
ENTRYPOINT ["/bin/bash", "-c", "source /opt/setup_luxe.sh && exec /bin/bash"]

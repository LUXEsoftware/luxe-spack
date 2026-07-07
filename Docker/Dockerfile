###############################################################################
#  Repository: ${IMAGE}/luxe-sw
#  Tag:        ${VERSION}-alma9
###############################################################################

ARG OS=ubuntu24
FROM ghcr.io/key4hep/key4hep-externals-${OS}:2026-04-23

ARG LUXE_SHA=80aa392e12b7e553f7dbfb099adb7c0e67b80924
ARG GITHUB_REPOSITORY=LUXEsoftware/luxe-spack

# --------------------------------------------------------------------------- #
#  System packages 
# --------------------------------------------------------------------------- #
RUN apt update && apt install -y wget && \
    wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc && \
    echo "deb http://apt.llvm.org/noble/ llvm-toolchain-noble-20 main" | tee /etc/apt/sources.list.d/llvm-20.list

# Install pre-compiled LLVM binaries to avoid expensive source builds in CI.
# libzstd-dev/zlib1g-dev are needed so LLVM's CMake exports (LLVMSupport ->
# zstd::libzstd_shared, ZLIB::ZLIB) resolve when py-llvmlite links against LLVM.

RUN apt update -y && apt upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    build-essential git python3 unzip gfortran file curl wget pkg-config rsync tzdata libgl1-mesa-dev libglu1-mesa libglu1-mesa-dev libkrb5-dev \
    llvm-20 clang-20 lld-20 libzstd-dev zlib1g-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    echo ". $HOME/.cargo/env" > ${HOME}/setup_env.sh

# Adding repository: LUXE
RUN . /opt/setup_spack.sh && \
    REPOPATH=${SPACK_ROOT}/var/luxe-spack && \
    git clone https://github.com/${GITHUB_REPOSITORY} ${REPOPATH} && \
    cd ${REPOPATH} && \
    git checkout ${LUXE_SHA}

# Apply our patches to spack
RUN . /opt/setup_spack.sh && \
    REPOPATH=${SPACK_ROOT}/var/luxe-spack && \
    cd /opt/spack && \
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

# Concretizing the LUXE stack reusing system packages as external
RUN --mount=type=secret,id=ocipass \
    . ${HOME}/setup_env.sh && \
    OCI_PASSWORD=$(cat /run/secrets/ocipass) spack external find --not-buildable && \
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

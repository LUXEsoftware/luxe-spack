###############################################################################
#  Repository: ${IMAGE}/luxe-sw
#  Tag:        ${VERSION}-alma9
###############################################################################

ARG OS=alma9
# mucoll tag is only available recent tag
FROM ghcr.io/key4hep/key4hep-externals-${OS}:2025-08-05-mucoll

ARG LUXE_SHA=80aa392e12b7e553f7dbfb099adb7c0e67b80924
ARG GITHUB_REPOSITORY=LUXEsoftware/luxe-spack

# Adding repository: LUXE
RUN . /opt/setup_spack.sh && \
    REPOPATH=${SPACK_ROOT}/var/luxe-spack && \
    git clone https://github.com/${GITHUB_REPOSITORY} ${REPOPATH} && \
    cd ${REPOPATH} && \
    git checkout ${LUXE_SHA} && \
    cd -

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    echo ". $HOME/.cargo/env" > ${HOME}/setup_env.sh

# Apply our patches to spack
RUN . /opt/setup_spack.sh && \
    REPOPATH=${SPACK_ROOT}/var/luxe-spack && \
    cd /opt/spack && \
    . ${REPOPATH}/.cherry-pick && \
    cd -

# Add the package repositories
ARG SPACK_BUILDCACHE
ARG OCI_USERNAME
RUN --mount=type=secret,id=ocipass \
    OCI_PASSWORD=$(cat /run/secrets/ocipass) && \
    . /opt/setup_spack.sh && \
    spack repo add ${SPACK_ROOT}/var/luxe-spack && \
    if [ -n "${SPACK_BUILDCACHE}" ]; then \
        spack mirror remove local-buildcache || true; \
        spack mirror add --oci-username "${OCI_USERNAME}" --oci-password "${OCI_PASSWORD}" --unsigned --autopush local-buildcache "${SPACK_BUILDCACHE}";\
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
RUN . ${HOME}/setup_env.sh && \
    spack external find --not-buildable rust && \
    spack concretize --reuse

# Installing fragments of dependency tree in separate layers for cached debugging
ENV SPACK_INSTALL_OPTS="--only-concrete --no-add --fail-fast"

RUN . ${HOME}/setup_env.sh && \
    spack install ${SPACK_INSTALL_OPTS} && \
    spack clean -a

RUN . ${HOME}/setup_env.sh && \
    LUXE_STACK_PATH=$(spack find --format "{prefix}" luxe-stack) && \
    LUXE_STACK_PATH_CLEANED=$(echo ${LUXE_STACK_PATH} | sed -E 's/\x1b\[[0-9;]*m//g') && \
    echo "alias setup_luxe=\". ${LUXE_STACK_PATH_CLEANED}/setup.sh\"" >> /etc/profile.d/aliases.sh

# Setting up users to be used for the local environment setup
RUN useradd --shell /bin/bash --create-home luxe
USER luxe
WORKDIR /home/luxe

ENTRYPOINT ["/bin/bash", "--login"]


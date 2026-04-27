# docker/metawrap/Dockerfile
FROM biokea-binner-base:1.0
# tool-specific install
RUN micromamba install -y -n base -c conda-forge -c ursky -c bioconda metawrap-mg && micromamba clean --all --yes || echo "metawrap install heavy — pre-build may fail; live retry"
WORKDIR /work

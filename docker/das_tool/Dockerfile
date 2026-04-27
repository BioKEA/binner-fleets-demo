# docker/das_tool/Dockerfile
FROM biokea-binner-base:1.0
# tool-specific install
RUN micromamba install -y -n base -c conda-forge -c bioconda das_tool && micromamba clean --all --yes
WORKDIR /work

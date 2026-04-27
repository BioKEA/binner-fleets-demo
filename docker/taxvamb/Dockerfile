# docker/taxvamb/Dockerfile
FROM biokea-binner-base:1.0
# tool-specific install
RUN micromamba install -y -n base -c conda-forge -c bioconda "vamb>=5" && micromamba clean --all --yes
WORKDIR /work

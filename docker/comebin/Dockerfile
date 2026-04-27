# docker/comebin/Dockerfile
FROM biokea-binner-base:1.0
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
# tool-specific install
RUN micromamba install -y -n base -c conda-forge -c bioconda comebin && micromamba clean --all --yes
WORKDIR /work

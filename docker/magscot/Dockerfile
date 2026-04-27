# docker/magscot/Dockerfile
FROM biokea-binner-base:1.0
RUN micromamba install -y -n base -c conda-forge -c bioconda r-base diamond hmmer \
    && micromamba clean --all --yes
RUN git clone --depth 1 https://github.com/ikmb/MAGScoT /opt/MAGScoT
ENV PATH="/opt/MAGScoT:${PATH}"
WORKDIR /work

# docker/comebin/Dockerfile
FROM biokea-binner-base:1.0
USER root
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
# COMEBin install via git + its requirements (avoid bioconda pin issue)
RUN git clone --depth 1 https://github.com/ziyewang/COMEBin /opt/COMEBin
RUN micromamba install -y -n base -c conda-forge -c bioconda \
    bedtools samtools mmseqs2 fraggenescan \
    && micromamba clean --all --yes
RUN if [ -f /opt/COMEBin/requirements.txt ]; then \
        pip install --no-cache-dir -r /opt/COMEBin/requirements.txt || true; \
    fi
ENV PATH="/opt/COMEBin/COMEBin:/opt/COMEBin:${PATH}"
WORKDIR /work

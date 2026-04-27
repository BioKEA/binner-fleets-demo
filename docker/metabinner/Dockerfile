# docker/metabinner/Dockerfile
FROM biokea-binner-base:1.0
# tool-specific install
RUN git clone --depth 1 https://github.com/ziyewang/MetaBinner /opt/MetaBinner && cd /opt/MetaBinner && pip install --no-cache-dir . || echo "metabinner install partial"
WORKDIR /work

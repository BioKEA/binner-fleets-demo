# docker/genomeface/Dockerfile
FROM biokea-binner-base:1.0
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
# tool-specific install
RUN pip install --no-cache-dir genomeface || echo "genomeface install pending — verify upstream"
WORKDIR /work

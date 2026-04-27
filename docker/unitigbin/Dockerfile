# docker/unitigbin/Dockerfile
FROM biokea-binner-base:1.0
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
# tool-specific install
RUN git clone --depth 1 https://github.com/metagentools/UnitigBin /opt/UnitigBin || echo "unitigbin clone failed — research code; verify upstream"
WORKDIR /work

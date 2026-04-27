# docker/vamb/Dockerfile
FROM biokea-binner-base:1.0
USER root
# pycoverm (vamb dep) needs Rust toolchain to build wheel
RUN apt-get update && apt-get install -y --no-install-recommends rustc cargo \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir vamb
WORKDIR /work

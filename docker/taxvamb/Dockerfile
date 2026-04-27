# docker/taxvamb/Dockerfile
FROM biokea-binner-base:1.0
USER root
RUN apt-get update && apt-get install -y --no-install-recommends rustc cargo \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "vamb>=5"
WORKDIR /work

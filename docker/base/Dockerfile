# docker/base/Dockerfile — biokea-binner-base:1.0
FROM mambaorg/micromamba:1.5.8

USER root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates curl git wget unzip pigz \
    samtools bowtie2 bwa \
    && rm -rf /var/lib/apt/lists/*

RUN micromamba install -y -n base -c conda-forge -c bioconda \
    python=3.11 biopython pysam pyarrow polars pyyaml click pydantic \
    && micromamba clean --all --yes

ENV PATH="/opt/conda/bin:${PATH}"
WORKDIR /work

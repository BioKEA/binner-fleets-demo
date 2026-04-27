# docker/python2-legacy/Dockerfile — for MyCC, COCACOLA (Python 2 era)
FROM continuumio/miniconda3:4.10.3-alpine

# This older miniconda is the last that easily supports Python 2.7 envs
RUN conda create -n py2 python=2.7 -y \
    && conda clean --all --yes

# Common bio deps for Python 2 tools
RUN /opt/conda/envs/py2/bin/pip install --no-cache-dir \
    numpy==1.16.6 scipy==1.2.3 biopython==1.76 || true

ENV PATH="/opt/conda/envs/py2/bin:${PATH}"
WORKDIR /work

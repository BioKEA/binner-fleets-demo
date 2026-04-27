# docker/cocacola/Dockerfile — Python 2 era, git clone
FROM biokea-binner-base:1.0-python2-legacy
RUN git clone --depth 1 https://github.com/younglululu/COCACOLA /opt/COCACOLA \
    || echo "COCACOLA clone failed — operator unblock"
ENV PATH="/opt/COCACOLA:${PATH}"
WORKDIR /work

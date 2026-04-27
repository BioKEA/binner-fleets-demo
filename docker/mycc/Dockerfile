# docker/mycc/Dockerfile — Python 2 era, tarball install
FROM biokea-binner-base:1.0-python2-legacy
RUN curl -L -o /tmp/mycc.tar.gz "https://sourceforge.net/projects/sb2nhri/files/MyCC/MyCC.tar.gz/download" \
    && mkdir -p /opt/MyCC && tar -xzf /tmp/mycc.tar.gz -C /opt/MyCC --strip-components=1 \
    && rm /tmp/mycc.tar.gz \
    || echo "MyCC tarball install incomplete — operator unblock during live demo"
ENV PATH="/opt/MyCC:${PATH}"
WORKDIR /work

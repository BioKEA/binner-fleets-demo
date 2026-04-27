# docker/graphmb/Dockerfile
FROM biokea-binner-base:1.0
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
# graphmb's pip resolver fails on tensorflow vs torch conflict; install w/o deps + add what's needed
RUN pip install --no-cache-dir --no-deps graphmb
RUN pip install --no-cache-dir networkx tqdm scikit-learn
WORKDIR /work

# grpc client and server

FROM python:3.8

USER root
RUN groupadd -g 1000 rpcuser \
    && useradd -r -u 1000 -g rpcuser rpcuser \
    && mkdir -p /home/rpcuser/VideoFromFrames/output \
    && chown -R rpcuser:rpcuser /home/rpcuser

WORKDIR /home/rpcuser/VideoFromFrames

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

USER rpcuser

FROM debian:trixie-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        python3-venv \
        python3-pip \
        build-essential \
        vim \
        ca-certificates \
        libgl1 libglx-mesa0 libglib2.0-0 \
        libgomp1 \
        python3-dev \
        portaudio19-dev \
        python3-pyaudio \
        alsa-utils \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

ENV VENV=/opt/venv
RUN python3 -m venv $VENV
ENV PATH="$VENV/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
            numpy \
            flask \
            "opencv-python>=4.8.0,<5" \
            Pillow>=10.0.0 \
            pyaudio \
            edge_impulse_linux \
            sounddevice \
            cbor \
            six && \
    rm -rf ~/.cache/pip

RUN mkdir -p /app/
COPY model.eim \
     main.py \
     camera_server.py \
     index.html \
     start.sh \
     test_edge_impulse.py \
     /app/

RUN chmod +x /app/start.sh
RUN chmod +x /app/model.eim
RUN chmod +x /app/test_edge_impulse.py
WORKDIR /app

CMD ["/app/start.sh"]

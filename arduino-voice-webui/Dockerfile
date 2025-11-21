FROM debian:trixie
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        python3-venv \
        python3-pip \
        build-essential \
        vim \
        dbus \
        portaudio19-dev \
        python3-pyaudio \
        sox \
        python3-dev \
        alsa-utils \
        ca-certificates \
        libgl1 libglx-mesa0 libglib2.0-0 \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

ENV VENV=/opt/venv
RUN python3 -m venv $VENV
ENV PATH="$VENV/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel && \
    pip install https://github.com/arduino/app-bricks-py/releases/download/release%2F0.5.0/arduino_app_bricks-0.5.0-py3-none-any.whl && \
    pip install --no-cache-dir \
            numpy \
            watchdog \
            pyalsaaudio \
            edge_impulse_linux \
            pyaudio \
            "opencv-python>=4.5.1.48,<5" \
            sounddevice \
            flask \
            six && \
    rm -rf ~/.cache/pip

RUN mkdir -p /app/
COPY deployment.eim \
     classify.py \
     index.html \
     arduino.png \
     edgeimpulse.png \
     foundries.png \
     qualcomm.png \
     off.png \
     blue.png \
     green.png \
     purple.png \
     red.png \
     yellow.png \
     start.sh \
     /app/

RUN chmod +x /app/start.sh
RUN chmod +x /app/deployment.eim
WORKDIR /app

CMD ["/app/start.sh"]

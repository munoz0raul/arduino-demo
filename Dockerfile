FROM debian:trixie
ENV DEBIAN_FRONTEND=noninteractive

COPY arduino.asc /etc/apt/keyrings/arduino.asc
COPY arduino.conf /etc/apt/auth.conf.d/arduino.conf
COPY arduino.list /etc/apt/sources.list.d/arduino.list

RUN chmod 644 /etc/apt/keyrings/arduino.asc && \
    chmod 600 /etc/apt/auth.conf.d/arduino.conf

RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates

RUN apt-get update && \
    apt-get install -y \
        arduino-cli python3 python3-venv python3-dev python3-pip \
        build-essential gcc \
        libasound2 libasound2-dev \
        libgpiod3 bash git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*



RUN arduino-cli core install arduino:zephyr -v

ENV VENV=/opt/venv
RUN python3 -m venv $VENV
ENV PATH="$VENV/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel

RUN pip install git+https://github.com/arduino/app-bricks-py.git
RUN pip install arduino_iot_cloud
RUN pip install numpy watchdog pyalsaaudio

COPY openocd /opt/openocd

RUN mkdir -p /app/sketch/
COPY sketch.ino /app/sketch/
COPY sketch.yaml /app/sketch/
COPY heart_frames.h /app/sketch/
COPY main.py /app/

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh
WORKDIR /app
CMD ["python", "/app/main.py"]


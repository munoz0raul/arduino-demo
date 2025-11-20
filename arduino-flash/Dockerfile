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
    apt-get install -y arduino-cli libgpiod3 bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN arduino-cli core install arduino:zephyr -v

COPY openocd /opt/openocd

COPY build.sh /usr/local/bin/build.sh
RUN chmod +x /usr/local/bin/build.sh

WORKDIR /tmp/sketch
CMD ["/usr/local/bin/build.sh"]

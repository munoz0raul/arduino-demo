# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025, Foundries.io

# Dockerfile
FROM eclipse-mosquitto:2.0

# Copia os dois arquivos de config
COPY config/mosquitto.conf /mosquitto/config/mosquitto.conf
COPY config/passwords     /mosquitto/config/passwords

# Garante permissões e dirs padrão
RUN chown -R mosquitto:mosquitto /mosquitto/config && \
    chmod 600 /mosquitto/config/passwords || true && \
    mkdir -p /mosquitto/data /mosquitto/log && \
    chown -R mosquitto:mosquitto /mosquitto/data /mosquitto/log
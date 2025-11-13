# Use Ubuntu base image with systemd support
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV container=docker

# Enable systemd
# STOPSIGNAL SIGRTMIN+3

EXPOSE 1883

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        systemd systemd-sysv \
        mosquitto mosquitto-clients \
        apache2 vim iproute2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy over service configurations
COPY configs/coordinator.conf /etc/mosquitto/conf.d/

# Enable services to start on boot
RUN systemctl enable mosquitto
CMD ["/sbin/init"]

# Use Ubuntu base image with systemd support
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV container=docker


EXPOSE 1883

# Install packages
# Install Python 3.11 and other packages
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    # add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        systemd systemd-sysv \
        mosquitto mosquitto-clients \
        apache2 vim iproute2


# Copy over service configurations and project
COPY configs/coordinator.conf /etc/mosquitto/conf.d/
ADD ./backend /workspace/backend
ADD ./frontend /workspace/frontend

# Enable services to start on boot
RUN systemctl enable mosquitto
CMD ["/sbin/init"]

# Use Ubuntu base image with systemd support
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV container=docker

# Enable systemd
# STOPSIGNAL SIGRTMIN+3

EXPOSE 1883
EXPOSE 3030
EXPOSE 8080

# Install packages
# Install Python 3.11 and other packages
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    # add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-venv \
        systemd systemd-sysv \
        mosquitto mosquitto-clients \
        apache2 vim iproute2 \
        curl && \
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
        apt-get install -y nodejs


# Copy over service configurations and project
COPY configs/coordinator.conf /etc/mosquitto/conf.d/
COPY configs/001-app.conf /etc/apache2/sites-enabled
COPY configs/ports.conf /etc/apache2/
COPY configs/backend.service /etc/systemd/system/backend.service
ADD ./backend /workspace/backend
ADD ./frontend /workspace/frontend

# Frontend Setup
RUN cd /workspace/frontend && \
    rm -fr node_modules package-lock.json && \
    npm install && \
    npm run build && \
    rm -rf /var/www/app && \
    mkdir -p /var/www/app && \
    cp -r  dist/* /var/www/app/ && \
    cd /

# Backend setup
RUN cd /workspace/backend && \
    rm -rf env/ && \
    python3 -m venv env && \
    . env/bin/activate && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn && \
    gunicorn -k uvicorn.workers.UvicornWorker app.main:app -D --bind 0.0.0.0:3030 && \
    cd /


# Enable services to start on boot
RUN systemctl enable apache2 && \
    systemctl enable mosquitto && \
    systemctl enable backend.service
CMD ["/sbin/init"]

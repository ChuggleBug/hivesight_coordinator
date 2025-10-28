
FROM ubuntu:latest

WORKDIR /workspace

RUN apt-get update && \
    apt-get install -y curl

# Keepalive
CMD [ "/usr/bin/tail", "-f", "/dev/null"]
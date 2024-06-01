FROM ubuntu:latest

RUN apt update && apt install -y \
    devenv \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

CMD ["/bin/bash"]
FROM ubuntu:latest

RUN apt update && apt install -y \
    bash \
    make \
    sudo \
    gosu

WORKDIR /app/

COPY . /app/

CMD ["/bin/bash"]
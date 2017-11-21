FROM ubuntu:16.04

# Install environment
RUN apt-get update -y && apt-get install -y \
    git \
    wget \
    python3.5 \
    python3-pip \
    python-setuptools \
    python3-nacl \
    apt-transport-https \
    ca-certificates \
    build-essential \
    pkg-config \
    cmake \
    libssl-dev \
    libsqlite3-dev \
    libsodium-dev \
    curl

# Install rust toolchain
RUN curl -o rustup https://sh.rustup.rs
RUN chmod +x rustup
RUN ./rustup -y

# Build libindy
WORKDIR /root
RUN git clone https://github.com/hyperledger/indy-sdk.git
WORKDIR /root/indy-sdk/libindy
RUN ls
RUN /root/.cargo/bin/cargo build

# Move libindy to lib path
USER root
RUN mv target/debug/libindy.so /usr/lib

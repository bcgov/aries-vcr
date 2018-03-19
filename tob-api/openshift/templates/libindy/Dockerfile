FROM ubuntu:16.04

# Install environment
RUN apt-get update -y && \
apt-get install -y \
    git \
    curl \
    build-essential \
    pkg-config \
    cmake \
    libssl-dev \
    libsqlite3-dev \
    libsodium-dev \
    libzmq3-dev

RUN apt-get install -y sqlite3 libsqlite3-dev

ENV HOME=/opt/app-root/src
WORKDIR $HOME

# Install rust toolchain
RUN curl -o rustup https://sh.rustup.rs
RUN chmod +x rustup
RUN ./rustup -y

# Build libindy
RUN git clone https://github.com/bcgov/indy-sdk.git
WORKDIR $HOME/indy-sdk/libindy
RUN git fetch
RUN git checkout enterprise-wallet
RUN $HOME/.cargo/bin/cargo build

# Move libindy to lib path
RUN mv target/debug/libindy.so /usr/lib

WORKDIR $HOME

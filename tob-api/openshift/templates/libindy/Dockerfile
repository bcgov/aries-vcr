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
    libsodium-dev

ENV HOME=/opt/app-root/src
WORKDIR $HOME

# Install rust toolchain
RUN curl -o rustup https://sh.rustup.rs
RUN chmod +x rustup
RUN ./rustup -y

# Build libindy
RUN git clone https://github.com/ianco/indy-sdk.git
WORKDIR $HOME/indy-sdk/libindy
RUN git fetch
RUN git checkout a191cde163ced0035217711a8eae24e65513158c
RUN $HOME/.cargo/bin/cargo build

# Move libindy to lib path
RUN mv target/debug/libindy.so /usr/lib

WORKDIR $HOME

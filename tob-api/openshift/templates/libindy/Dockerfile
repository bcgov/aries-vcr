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
# RUN git checkout 50c58ee5df8d9ecb8f111be74fd1b49403f82378
RUN git checkout tob-wallet
RUN $HOME/.cargo/bin/cargo build

# Move libindy to lib path
RUN mv target/debug/libindy.so /usr/lib

WORKDIR $HOME

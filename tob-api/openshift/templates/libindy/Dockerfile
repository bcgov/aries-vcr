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
    libzmq3-dev \
    sqlite3

ENV HOME=/opt/app-root/src
WORKDIR $HOME

# Install rust toolchain
RUN curl -o rustup https://sh.rustup.rs && \
	chmod +x rustup && \
	./rustup -y

# Build libindy
RUN git clone https://github.com/bcgov/indy-sdk.git && \
	cd indy-sdk/libindy && \
	$HOME/.cargo/bin/cargo build && \
	mv target/debug/libindy.so /usr/lib && \
	rm -rf $HOME/.cargo

WORKDIR $HOME

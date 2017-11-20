FROM centos/python-36-centos7:latest

RUN apt-get update -y && apt-get install -y \
    git \
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
RUN git clone https://github.com/hyperledger/indy-sdk.git
WORKDIR /home/indy/indy-sdk/libindy
RUN /home/indy/.cargo/bin/cargo build

# Move libindy to lib path
USER root
RUN mv target/debug/libindy.so /usr/lib

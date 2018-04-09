FROM ubuntu:16.04

# Install environment
RUN apt-get update -y && \
	apt-get install -y --no-install-recommends \
		build-essential \
		ca-certificates \
		cmake \
		curl \
		git \
		libssl-dev \
		libsqlite3-dev \
		libsodium-dev \
		libzmq3-dev \
		pkg-config \
		sqlite3

ENV HOME=/opt/app-root/src
WORKDIR $HOME

# Install rust toolchain and indy-sdk
RUN curl -o rustup https://sh.rustup.rs && \
	chmod +x rustup && \
	./rustup -y && \
	git clone https://github.com/bcgov/indy-sdk.git && \
	cd indy-sdk/libindy && \
	$HOME/.cargo/bin/cargo build && \
	mv target/debug/libindy.so /usr/lib && \
	cd $HOME && \
	rm -rf .cargo .rustup indy-sdk

WORKDIR $HOME

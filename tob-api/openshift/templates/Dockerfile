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


ENV HOME=/home/user
WORKDIR $HOME

# Install rust toolchain
RUN curl -o rustup https://sh.rustup.rs
RUN chmod +x rustup
RUN ./rustup -y

RUN git clone https://github.com/hyperledger/indy-sdk.git
WORKDIR $HOME/indy-sdk/libindy
RUN $HOME/.cargo/bin/cargo build
# Move libindy to lib path
RUN mv target/debug/libindy.so /usr/lib
WORKDIR $HOME



EXPOSE 8080

ENV PYTHON_VERSION=3.6 \
    PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    STI_SCRIPTS_PATH=/usr/libexec/s2i


ENV LC_ALL="C"
ENV LC_CTYPE="en_US.utf-8"

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Python 3.6" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,python,python36,rh-python36" \
      com.redhat.component="python36-docker" \
      io.openshift.s2i.scripts-url="image:///${STI_SCRIPTS_PATH}" \
      name="centos/python-36-centos7" \
      version="1" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>"

ENV SUMMARY="Platform for building and running Python $PYTHON_VERSION applications" \
    DESCRIPTION="Python $PYTHON_VERSION available as docker container is a base platform for \
building and running various Python $PYTHON_VERSION applications and frameworks. \
Python is an easy to learn, powerful programming language. It has efficient high-level \
data structures and a simple but effective approach to object-oriented programming. \
Python's elegant syntax and dynamic typing, together with its interpreted nature, \
make it an ideal language for scripting and rapid application development in many areas \
on most platforms."

# RUN yum install -y centos-release-scl-rh && \
#     yum-config-manager --enable centos-sclo-rh-testing && \
#     INSTALL_PKGS="rh-python36 rh-python36-python-devel rh-python36-python-setuptools rh-python36-python-pip \
#      nss_wrapper httpd24 httpd24-httpd-devel httpd24-mod_ssl httpd24-mod_auth_kerb httpd24-mod_ldap \
#          httpd24-mod_session atlas-devel gcc-gfortran libffi-devel libtool-ltdl enchant" && \
#     yum install -y --setopt=tsflags=nodocs --enablerepo=centosplus $INSTALL_PKGS && \

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH.
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# - Create a Python virtual environment for use by any application to avoid
#   potential conflicts with Python packages preinstalled in the main Python
#   installation.
# - In order to drop the root user, we have to make some directories world
#   writable as OpenShift default security model is to run the container
#   under random UID.


RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip

RUN pip install virtualenv 

RUN virtualenv .

# RUN chgrp -R 0 /usr/lib/libindy.so \
#   && chmod -R g+rwX /usr/lib

RUN chgrp -R 0 $STI_SCRIPTS_PATH \
  && chmod -R g+rwX $STI_SCRIPTS_PATH

USER 1001

# Set the default CMD to print the usage of the language image.
CMD $STI_SCRIPTS_PATH/usage

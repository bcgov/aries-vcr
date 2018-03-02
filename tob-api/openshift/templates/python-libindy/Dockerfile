FROM libindy:latest

# Install environment
RUN apt-get update -y && \
apt-get install -y \
    python3.5 \
    python3-pip \
    python-setuptools \
    python3-nacl \
    apt-transport-https \
    ca-certificates

ENV HOME=/opt/app-root/src
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

ENV SUMMARY="Platform for building and running Python $PYTHON_VERSION applications" \
    DESCRIPTION="Python $PYTHON_VERSION available as docker container is a base platform for \
building and running various Python $PYTHON_VERSION applications and frameworks. \
Python is an easy to learn, powerful programming language. It has efficient high-level \
data structures and a simple but effective approach to object-oriented programming. \
Python's elegant syntax and dynamic typing, together with its interpreted nature, \
make it an ideal language for scripting and rapid application development in many areas \
on most platforms."

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

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH.
COPY ./s2i/bin/. $STI_SCRIPTS_PATH

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
RUN virtualenv /opt/app-root

RUN chgrp -R 0 $STI_SCRIPTS_PATH \
  && chmod -R g+rwx $STI_SCRIPTS_PATH

RUN chgrp -R 0 /usr/bin/fix-permissions \
  && chmod -R g+rwx /usr/bin/fix-permissions

RUN chgrp -R 0 /usr/bin/cgroup-limits \
  && chmod -R g+rwx /usr/bin/cgroup-limits

RUN chgrp -R 0 /generate_container_user \
  && chmod -R g+rwx /generate_container_user

RUN chgrp -R 0 $HOME \
  && chmod -R g+rwx $HOME

# Cache bust this every build
# RUN curl 138.197.170.136/genesis > /opt/app-root/genesis

USER 1001

# Set the default CMD to print the usage of the language image.
CMD $STI_SCRIPTS_PATH/usage
FROM von-image:py36-latest

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

USER root

# - In order to drop the root user, we have to make some directories world
#   writable as OpenShift default security model is to run the container
#   under random UID.
RUN chown -R indy:0 $HOME $STI_SCRIPTS_PATH \
       /usr/bin/fix-permissions /usr/bin/cgroup-limits /generate_container_user && \
    chmod -R ug+rw $HOME && \
    chmod -R ug+rwx $STI_SCRIPTS_PATH \
       /usr/bin/fix-permissions /usr/bin/cgroup-limits /generate_container_user

USER indy

# Set the default CMD to print the usage of the language image.
CMD $STI_SCRIPTS_PATH/usage

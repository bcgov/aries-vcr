#!/bin/bash
export MSYS_NO_PATHCONV=1
set -e

if [ -z "${S2I_HOME}" ]; then
  S2I_HOME="../../s2i"
fi
S2I_EXE="${S2I_HOME}/s2i.exe"

SCRIPT_HOME="$( cd "$( dirname "$0" )" && pwd )"
export COMPOSE_PROJECT_NAME="tob"

# =================================================================================================================
# Usage:
# - https://github.com/nrempel/von-network/blob/master/manage
# - https://gist.github.com/nrempel/e1e587e93cc4f721b7d00b2f8f015234
#
# - https://github.com/nrempel/von-network/blob/master/docker-compose.yml
# - https://gist.github.com/nrempel/d2681ab11c03e2d138f4317ad834c2bb
# -----------------------------------------------------------------------------------------------------------------
usage() {
  cat <<-EOF
  
  Usage: $0 {start|stop|build}
  
  Options:
  
  build - Build the docker images for the project.
          You need to do this first, since the builds require
          a combination of Docker and S2I builds.

  start - Creates the application containers from the built images
          and starts the services based on the docker-compose.yml file.          
  
  stop - Stops the services.  This is a non-destructive process.  The containers
         are not deleted so they will be reused the next time you run start.
          

EOF
exit 1
}
# -----------------------------------------------------------------------------------------------------------------
# Functions:
# -----------------------------------------------------------------------------------------------------------------
buildImages() {
  #
  # tob-web
  #
  echo -e "\nBuilding angular-builder image ..."
  docker build \
    -t 'angular-builder' \
    -f '../tob-web/openshift/templates/angular-builder/Dockerfile' '../tob-web/openshift/templates/angular-builder/'
  
  echo -e "\nBuilding nginx-runtime image ..."
  docker build \
    -t 'nginx-runtime' \
    -f '../tob-web/openshift/templates/nginx-runtime/Dockerfile' '../tob-web/openshift/templates/nginx-runtime/'
  
  echo -e "\nBuilding angular-on-nginx image ..."
  ${S2I_EXE} build \
    '../tob-web' \
    'angular-builder' \
    'angular-on-nginx' \
    --runtime-image \
    "nginx-runtime" \
    -a "/opt/app-root/src/dist/:app" 

  #
  # tob-solr
  #
  echo -e "\nBuilding solr-base image ..."
  docker build \
    https://github.com/bcgov/openshift-solr.git \
    -t 'solr-base'
  
  echo -e "\nBuilding solr image ..."
  ${S2I_EXE} build \
    '../tob-solr' \
    'solr-base' \
    'solr'

  #
  # tob-db
  #
    # Nothing to build here ...
  
  #
  # tob-api
  #
  echo -e "\nBuilding schema-spy image ..."
  docker build \
    https://github.com/bcgov/SchemaSpy.git \
    -t 'schema-spy'

  echo -e "\nBuilding libindy image ..."
  docker build \
    -t 'libindy' \
    -f '../tob-api/openshift/templates/libindy/Dockerfile' '../tob-api/openshift/templates/libindy/'

  echo -e "\nBuilding python-libindy image ..."
  docker build \
    -t 'python-libindy' \
    -f '../tob-api/openshift/templates/python-libindy/Dockerfile' '../tob-api/openshift/templates/python-libindy/'

  echo -e "\nBuilding django image ..."
  ${S2I_EXE} build \
    '../tob-api' \
    'python-libindy' \
    'django'
}

configureEnvironment () {
  # tob-db
  export POSTGRESQL_DATABASE="THE_ORG_BOOK"
  export POSTGRESQL_USER="DB_USER"
  export POSTGRESQL_PASSWORD="DB_PASSWORD"

  # schema-spy
  export SCHEMA_SPY_DATABASE_SERVICE_NAME="localhost"
  export POSTGRESQL_DATABASE=${POSTGRESQL_DATABASE}
  export POSTGRESQL_USER=${POSTGRESQL_USER}
  export POSTGRESQL_PASSWORD=${POSTGRESQL_PASSWORD}

  # tob-solr
  export CORE_NAME="the_org_book"

  # tob-api
  #export DATABASE_SERVICE_NAME="localhost"
  export DATABASE_ENGINE="postgresql"
  export DATABASE_NAME=${POSTGRESQL_DATABASE}
  export DATABASE_USER=${POSTGRESQL_USER}
  export DATABASE_PASSWORD=${POSTGRESQL_PASSWORD}
  export DJANGO_SECRET_KEY=wpn1GZrouOryH2FshRrpVHcEhMfMLtmTWMC2K5Vhx8MAi74H5y
  export DJANGO_DEBUG=True
  export SOLR_SERVICE_NAME=""
  export SOLR_CORE_NAME=${CORE_NAME}

  # tob-web
  export API_URL="http://tob-api:8080/api/v1/"
  export IpFilterRules='#allow all; deny all;'
  export RealIpFrom='127.0.0.0/16'
}
# =================================================================================================================

pushd ${SCRIPT_HOME} >/dev/null

case "$1" in
  start)
    configureEnvironment
    docker-compose up tob-web tob-api
    #docker-compose up tob-web tob-api schema-spy tob-solr tob-db
    ;;
  stop)
      docker-compose stop
    ;;
  build)
    buildImages      
    ;;
  *)
    usage
esac

popd >/dev/null

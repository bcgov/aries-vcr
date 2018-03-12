#!/bin/bash
export DOCKERHOST=$(ifconfig | grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v 127.0.0.1 | awk '{ print $2 }' | cut -f2 -d: | head -n1)
export MSYS_NO_PATHCONV=1
set -e

S2I_EXE=s2i
if [ -z $(type -P "$S2I_EXE") ]; then
  echo -e "The ${S2I_EXE} executable is needed and not on your path."
  echo -e "It can be downloaded from here: https://github.com/openshift/source-to-image"
  echo -e "Make sure you place it in a directory on your path."
  exit 1
fi

SCRIPT_HOME="$( cd "$( dirname "$0" )" && pwd )"
export COMPOSE_PROJECT_NAME="tob"

# =================================================================================================================
# Usage:
# -----------------------------------------------------------------------------------------------------------------
usage() {
  cat <<-EOF

  Usage: $0 {start|stop|build|rm}

  Options:

  build - Build the docker images for the project.
          You need to do this first, since the builds require
          a combination of Docker and S2I builds.

          You can build individual components as shown below, components that have dependencies will have these dependencies built too.

          Examples:
           - Build the web UI only

            $0 build tob-web
 
           - Build the API server only.
 
            $0 build tob-api

           - Build the Solr Search Engine server only.
       
            $0 build tob-solr

          By default all containers that components comprise of, will be rebuilt.

            $0 build


  start - Creates the application containers from the built images
          and starts the services based on the docker-compose.yml file.

          You can pass in a list of containers to start.  
          By default all containers will be started.
          
          The API_URL used by tob-web can also be redirected.

          Examples:
          $0 start
          $0 start tob-solr
          $0 start tob-web
          $0 start tob-web API_URL=http://docker.for.win.localhost:56325/api/v1
          $0 start tob-api

  stop - Stops the services.  This is a non-destructive process.  The containers
         are not deleted so they will be reused the next time you run start.

  rm - Removes any existing application containers.

EOF
exit 1
}
# -----------------------------------------------------------------------------------------------------------------
# Default Settings:
# -----------------------------------------------------------------------------------------------------------------
DEFAULT_CONTAINERS="tob-db tob-solr tob-api schema-spy tob-web"
# -----------------------------------------------------------------------------------------------------------------
# Functions:
# -----------------------------------------------------------------------------------------------------------------
build-web() {
  #
  # tob-web
  #
  # The nginx-runtime image is used for the final runtime image.
  # The angular-app image is used to build the artifacts for the angular distribution.
  # The angular-on-nginx image is copy of the nginx-runtime image complete with a copy of the build artifacts.
  #
  echo -e "\nBuilding nginx-runtime image ..."
  docker build \
    -t 'nginx-runtime' \
    -f '../tob-web/openshift/templates/nginx-runtime/Dockerfile' '../tob-web/openshift/templates/nginx-runtime/'
  
  echo -e "\nBuilding angular-app image ..."
  ${S2I_EXE} build \
  	-e "NG_BASE_HREF=${WEB_BASE_HREF}" \
    '../tob-web' \
    'centos/nodejs-6-centos7:6' \
    'angular-app'

  echo -e "\nBuilding angular-on-nginx image ..."
  docker build \
    -t 'angular-on-nginx' \
    -f '../tob-web/openshift/templates/angular-on-nginx/Dockerfile' '../tob-web/openshift/templates/angular-on-nginx/'
}

build-solr() {
  #
  # tob-solr
  #
  echo -e "\nBuilding solr-base image ..."
  docker build \
    https://github.com/bcgov/openshift-solr.git \
    -t 'solr-base'

  echo -e "\nBuilding solr image ..."
  ${S2I_EXE} build \
    '../tob-solr/cores' \
    'solr-base' \
    'solr'
}

build-db() {
  #
  # tob-db
  #
    # Nothing to build here ...
  echo
}

build-schema-spy() {
  #
  # schema-spy
  #
  echo -e "\nBuilding schema-spy image ..."
  docker build \
    https://github.com/bcgov/SchemaSpy.git \
    -t 'schema-spy'
}

build-api() {
  #
  # tob-api
  #
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

buildImages() {
  build-web
  build-solr
  build-db
  build-schema-spy
  build-api
}

configureEnvironment () {

  if [ -f .env ]; then
  	export $(cat .env | xargs)
  fi

  for arg in $@; do
    case "$arg" in
      *=*)
        export ${arg}
        ;;  
    esac
  done
  
  if [ "$COMMAND" == "start" ]; then
    if [ -z "$seed" ]; then
      echo "You must provide a seed parameter. For example: seed=my_seed_000000000000000000000000."
      exit 1
    fi

    if [ ${#seed} -ne 32 ]; then
      echo "The seed parameter must be 32 characters long exactly."
      exit 1
    fi
  fi

  export INDY_WALLET_SEED=${seed}

  # tob-db
  export POSTGRESQL_DATABASE="THE_ORG_BOOK"
  export POSTGRESQL_USER="DB_USER"
  export POSTGRESQL_PASSWORD="DB_PASSWORD"

  # schema-spy
  export DATABASE_SERVICE_NAME="tob-db"
  export POSTGRESQL_DATABASE=${POSTGRESQL_DATABASE}
  export POSTGRESQL_USER=${POSTGRESQL_USER}
  export POSTGRESQL_PASSWORD=${POSTGRESQL_PASSWORD}

  # tob-solr
  export CORE_NAME="the_org_book"

  # tob-api
  export API_HTTP_PORT=${API_HTTP_PORT-8081}
  export DATABASE_SERVICE_NAME="tob-db"
  export DATABASE_ENGINE="postgresql"
  export DATABASE_NAME=${POSTGRESQL_DATABASE}
  export DATABASE_USER=${POSTGRESQL_USER}
  export DATABASE_PASSWORD=${POSTGRESQL_PASSWORD}
  export DJANGO_SECRET_KEY=wpn1GZrouOryH2FshRrpVHcEhMfMLtmTWMC2K5Vhx8MAi74H5y
  export DJANGO_DEBUG=True
  export SOLR_SERVICE_NAME="tob-solr"
  export SOLR_CORE_NAME=${CORE_NAME}
  export LEDGER_URL=${LEDGER_URL-http://$DOCKERHOST:9000}

  # tob-web
  export WEB_HTTP_PORT=${WEB_HTTP_PORT-8080}
  export WEB_BASE_HREF=${WEB_BASE_HREF:-/}
  export API_URL=${API_URL-http://tob-api:8080/api/v1/}
  export IpFilterRules='#allow all; deny all;'
  export RealIpFrom='127.0.0.0/16'
}

getStartupParams() {
  CONTAINERS=""
  ARGS="--force-recreate"

  for arg in $@; do
    case "$arg" in
      *=*)
        # Skip it
        ;;  
     -*)
        ARGS+=" $arg";;
      *)
        CONTAINERS+=" $arg";;
    esac
  done

  if [ -z "$CONTAINERS" ]; then
    CONTAINERS="$DEFAULT_CONTAINERS"
  fi

  echo ${ARGS} ${CONTAINERS}
}
# =================================================================================================================

pushd ${SCRIPT_HOME} >/dev/null

case "$1" in
  start)
    COMMAND=$1
    shift
    _startupParams=$(getStartupParams $@)
    configureEnvironment $@
    docker-compose up ${_startupParams}
    ;;
  stop)
    configureEnvironment
    docker-compose stop
    ;;
  rm)
    configureEnvironment
    docker-compose rm
    ;;
  build)
    COMMAND=$1
    shift
    _startupParams=$(getStartupParams $@)
    configureEnvironment $@
    case "$@" in
      tob-api)
        build-api
        ;;
      tob-web)
        build-web
        ;;
      tob-solr)
        build-solr
        ;;
      *)
       buildImages
    esac
    ;;
  *)
    usage
esac

popd >/dev/null

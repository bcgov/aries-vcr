#!/bin/bash

SCRIPT_DIR=$(dirname $0)
# =================================================================================================================
# Usage:
# -----------------------------------------------------------------------------------------------------------------
usage() {
  cat <<-EOF
  A helper script to pull images from an OpenShift docker registry.

  Usage: ${0} [ -h -x -r <OpenShiftRegistryAddress>] -i <ImageName> -n <OpenShiftProjectNamespace> ]

  OPTIONS:
  ========
    -i The name of the image to pull.
    -n The namespace of the OpenShift project.
       For example devex-von-tools
    -r Optional.  The address of the OpenShift docker registry, 
       such as your local registry, for example 172.30.1.1:5000.
       Defaults to docker-registry.pathfinder.gov.bc.ca

    -h prints the usage for the script
    -x run the script in debug mode to see what's happening

EOF
exit
}

# -----------------------------------------------------------------------------------------------------------------
# Initialization:
# -----------------------------------------------------------------------------------------------------------------
while getopts i:n:r:hx FLAG; do
  case $FLAG in
    i ) export DOCKER_IMAGE=$OPTARG ;;
    n ) export OPENSHIFT_NAMESPACE=$OPTARG ;;
    r ) export OPENSHIFT_REGISTRY_ADDRESS=$OPTARG ;;
    x ) export DEBUG=1 ;;
    h ) usage ;;
    \? ) #unrecognized option - show help
      echo -e \\n"Invalid script option: -${OPTARG}"\\n
      usage
      ;;
  esac
done

# Shift the parameters in case there any more to be used
shift $((OPTIND-1))
# echo Remaining arguments: $@

if [ ! -z "${DEBUG}" ]; then
  set -x
fi

if [ -z "${DOCKER_IMAGE}" ] || [ -z "${OPENSHIFT_NAMESPACE}" ]; then
  echo -e \\n"Missing parameters!"\\n  
  usage
fi

if [ -z "${OPENSHIFT_REGISTRY_ADDRESS}" ]; then
  OPENSHIFT_REGISTRY_ADDRESS=docker-registry.pathfinder.gov.bc.ca
fi

OPENSHIFT_IMAGE_SNIPPET=${DOCKER_IMAGE#*/}
OPENSHIFT_IMAGESTREAM_PATH=${OPENSHIFT_REGISTRY_ADDRESS}/${OPENSHIFT_NAMESPACE}/${OPENSHIFT_IMAGE_SNIPPET}
# =================================================================================================================

docker tag ${DOCKER_IMAGE} ${OPENSHIFT_IMAGESTREAM_PATH}
docker login ${OPENSHIFT_REGISTRY_ADDRESS} -u $(oc whoami) -p $(oc whoami -t)
docker push ${OPENSHIFT_IMAGESTREAM_PATH}
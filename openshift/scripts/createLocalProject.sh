#!/bin/bash

SCRIPT_DIR=$(dirname $0)

# ===================================================================================================
# Funtions
# ---------------------------------------------------------------------------------------------------
usage() {
  cat <<EOF
========================================================================================
Creates a local OpenShift project.
----------------------------------------------------------------------------------------
Usage:

  ${0} [-h -x] -p <project_namespace> [-n <displayname>] [-d <description>]

  OPTIONS:
  ========
    -h prints the usage for the script
    -x run the script in debug mode to see what's happening
    -p <project_namespace> the namespace for the project.
    -n <displayname> The display name for the project.
    -d <description> The description of the project.
EOF
exit 1
}

if [ -f ${SCRIPT_DIR}/commonFunctions.inc ]; then
  . ${SCRIPT_DIR}/commonFunctions.inc
fi

createProject (){
  namespace=$1
  display_name=$2
  description=$3
  
  echo "Creating new project; ${namespace} ..."
  oc new-project ${namespace} --display-name="${display_name}" --description="${description}" >/dev/null
}
# ===================================================================================================

# ===================================================================================================
# Setup
# ---------------------------------------------------------------------------------------------------
while getopts p:n:d:hx FLAG; do
  case $FLAG in
    p ) PROJECT_NAMESPACE=$OPTARG ;;
    n ) DISPLAY_NAME=$OPTARG ;;
    d ) DESCRIPTION=$OPTARG ;;
    x ) export DEBUG=1 ;;
    h ) usage ;;
    \?) #unrecognized option - show help
      echo -e \\n"Invalid script option"\\n
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

if [ -z "${PROJECT_NAMESPACE}" ]; then
  echo -e \\n"Missing parameters!"  
  usage
fi
# ===================================================================================================

if ! isLocalCluster; then
  echo "This script can only be run on a local cluster!"
  exit 1
fi

if ! projectExists ${PROJECT_NAMESPACE}; then
  createProject ${PROJECT_NAMESPACE} "${DISPLAY_NAME}" "${DESCRIPTION}"
  exitOnError
else
  echo "${PROJECT_NAMESPACE} exists ..."
fi
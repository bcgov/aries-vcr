#!/bin/bash

SCRIPT_DIR=$(dirname $0)

# ===================================================================================================
# Funtions
# ---------------------------------------------------------------------------------------------------
usage() {
  cat <<EOF
========================================================================================
Deletes a local OpenShift project.
----------------------------------------------------------------------------------------
Usage:

  ${0} [-h -x] -p <project_namespace>

  OPTIONS:
  ========
    -h prints the usage for the script
    -x run the script in debug mode to see what's happening
    -p <project_namespace> the namespace for the project.
EOF
exit 1
}

if [ -f ${SCRIPT_DIR}/commonFunctions.inc ]; then
  . ${SCRIPT_DIR}/commonFunctions.inc
fi

deleteProject (){
  projectName=$1  
  echo "Deleting project; ${projectName} ..."
  oc delete project ${projectName}
}
# ===================================================================================================

# ===================================================================================================
# Setup
# ---------------------------------------------------------------------------------------------------
while getopts p:n:d:hx FLAG; do
  case $FLAG in
    p ) PROJECT_NAMESPACE=$OPTARG ;;
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

if projectExists ${PROJECT_NAMESPACE}; then
  deleteProject ${PROJECT_NAMESPACE}
  exitOnError
else
  echo "${PROJECT_NAMESPACE} does not exist ..."
fi
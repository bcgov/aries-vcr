#!/bin/bash

SCRIPT_DIR=$(dirname $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"

# ===================================================================================================
# Funtions
# ---------------------------------------------------------------------------------------------------
usage() {
  cat <<EOF
========================================================================================
Creates a local project set in OpenShift
----------------------------------------------------------------------------------------
Usage:

  ${0} [-h -x -D]

  OPTIONS:
  ========
    -D delete the local projects created by this script.
    -h prints the usage for the script
    -x run the script in debug mode to see what's happening

  Update settings.sh and settings.local.sh files to set defaults
EOF
exit 1
}

# Set project and local environment variables
if [ -f settings.sh ]; then
  echo -e \\n"Loading default project settings from settings.sh ..."\\n
  . settings.sh
fi

if [ -f ${SCRIPTS_DIR}/commonFunctions.inc ]; then
  . ${SCRIPTS_DIR}/commonFunctions.inc
fi

while getopts xhD FLAG; do
  case $FLAG in
    D ) export DELETE_PROJECTS=1 ;;
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

if [ ! -z "${DEBUG}" ]; then
  set -x
fi
# ===================================================================================================

if ! isLocalCluster; then
  echo "This script can only be run on a local cluster!"
  exit 1
fi

# Iterate through Tools, Dev, Test and Prod projects and create them if they don't exist.
for project in ${TOOLS} ${PROJECT_NAMESPACE}-${DEV} ${PROJECT_NAMESPACE}-${TEST} ${PROJECT_NAMESPACE}-${PROD}; do

  if [ -z ${DELETE_PROJECTS} ]; then
    # Create ..."
    ${SCRIPTS_DIR}/createLocalProject.sh \
      -p ${project}
    exitOnError
  else
    # Delete ..."
    ${SCRIPTS_DIR}/deleteLocalProject.sh \
      -p ${project}
    exitOnError
  fi
done

# ToDo:
# - Run the build and deployment generation too.

#!/bin/bash

SCRIPT_DIR=$(dirname $0)

# ===================================================================================
usage() {
cat <<EOF

================================================================================
Creating GLUSTER endpoints and services in a given project.
--------------------------------------------------------------------------------
Usage: 
  ${0} [ -h -x ] -p <TARGET_PROJECT_NAME>

Options:
  -h prints the usage for the script
  -x run the script in debug mode to see what's happening
================================================================================
EOF
exit 1
}
# ------------------------------------------------------------------------------
# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts p:xh FLAG; do
  case $FLAG in
    p ) TARGET_PROJECT_NAME=$OPTARG ;;
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

if [ -z "${TARGET_PROJECT_NAME}" ]; then
  echo -e \\n"Missing parameters!"  
  usage
fi
# -----------------------------------------------------------------------------------
if [ -z "${GLUSTER_ENDPOINT_CONFIG}" ]; then
  GLUSTER_ENDPOINT_CONFIG=https://raw.githubusercontent.com/BCDevOps/openshift-tools/master/resources/glusterfs-cluster-app-endpoints.yml
fi
  
if [ -z "${GLUSTER_SVC_CONFIG}" ]; then
  GLUSTER_SVC_CONFIG=https://raw.githubusercontent.com/BCDevOps/openshift-tools/master/resources/glusterfs-cluster-app-service.yml
fi
  
if [ -z "${GLUSTER_SVC_NAME}" ]; then
  GLUSTER_SVC_NAME=glusterfs-cluster-app
fi
# ==============================================================================

RTN_VAL=$(oc projects | grep ${TARGET_PROJECT_NAME})
if [ -z "$RTN_VAL" ]; then
	echo "Unable to create ${GLUSTER_SVC_NAME} in ${TARGET_PROJECT_NAME}, the ${TARGET_PROJECT_NAME} project does not exist ..."
	echo
else
	RTN_VAL=$(oc get svc -n ${TARGET_PROJECT_NAME} | grep ${GLUSTER_SVC_NAME})
	if [ -z "$RTN_VAL" ]; then
		echo "Creating ${GLUSTER_SVC_NAME} in ${TARGET_PROJECT_NAME} ..."
		echo

		oc create \
			-f ${GLUSTER_ENDPOINT_CONFIG} \
			-n ${TARGET_PROJECT_NAME}
		echo

		oc create \
			-f ${GLUSTER_SVC_CONFIG} \
			-n ${TARGET_PROJECT_NAME}
		echo
	else
		echo "${GLUSTER_SVC_NAME} already exists in ${TARGET_PROJECT_NAME} ..."
		echo
	fi
fi
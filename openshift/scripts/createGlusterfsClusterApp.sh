#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)

# ===================================================================================
# Grant deployment configuration(s) access to the images in the tools project
# ===================================================================================
TARGET_PROJECT_NAME=${1}
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
if [ -z "$TARGET_PROJECT_NAME" ]; then
	echo "You must supply TARGET_PROJECT_NAME."
	MissingParam=1
fi

if [ ! -z "$MissingParam" ]; then
	echo "============================================"
	echo "One or more parameters are missing!"
	echo "--------------------------------------------"	
	echo "TARGET_PROJECT_NAME[{1}]: ${1}"
    echo "============================================"
	echo
	exit 1
fi
# -----------------------------------------------------------------------------------
GLUSTER_ENDPOINT_CONFIG=https://raw.githubusercontent.com/BCDevOps/openshift-tools/master/resources/glusterfs-cluster-app-endpoints.yml
GLUSTER_SVC_CONFIG=https://raw.githubusercontent.com/BCDevOps/openshift-tools/master/resources/glusterfs-cluster-app-service.yml
GLUSTER_SVC_NAME=glusterfs-cluster-app
# ===================================================================================
if [ ! -z "$DEBUG_MESSAGES" ]; then
	echo
	echo "------------------------------------------------------------------------"
	echo "Parameters for call to oc command ..."
	echo "------------------------------------------------------------------------"
	echo "TARGET_PROJECT_NAME=${TARGET_PROJECT_NAME}"
	echo "------------------------------------------------------------------------"
	echo
fi

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
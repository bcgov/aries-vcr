#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)

# ===================================================================================
# Granting deployment configurations access to the images in the tools project
# ===================================================================================
TARGET_PROJECT_NAME=${1}
TOOLS_PROJECT_NAME=${2}
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
if [ -z "$TARGET_PROJECT_NAME" ]; then
	echo "You must supply TARGET_PROJECT_NAME."
	MissingParam=1
fi

if [ -z "$TOOLS_PROJECT_NAME" ]; then
	echo "You must supply TOOLS_PROJECT_NAME."
	MissingParam=1
fi

if [ ! -z "$MissingParam" ]; then
	echo "============================================"
	echo "One or more parameters are missing!"
	echo "--------------------------------------------"	
	echo "TARGET_PROJECT_NAME[{1}]: ${1}"
	echo "TOOLS_PROJECT_NAME[{2}]: ${2}"
    echo "============================================"
	echo
	exit 1
fi
# ===================================================================================

echo "Granting deployment configuration access from ${TARGET_PROJECT_NAME}, to ${TOOLS_PROJECT_NAME} ..."

if [ ! -z "$DEBUG_MESSAGES" ]; then
	echo
	echo "------------------------------------------------------------------------"
	echo "Parameters for call to oc command ..."
	echo "------------------------------------------------------------------------"
	echo "TARGET_PROJECT_NAME=${TARGET_PROJECT_NAME}"
	echo "TOOLS_PROJECT_NAME=${TOOLS_PROJECT_NAME}"
	echo "------------------------------------------------------------------------"
	echo
fi

oc policy add-role-to-user \
system:image-puller \
system:serviceaccount:${TARGET_PROJECT_NAME}:default \
-n ${TOOLS_PROJECT_NAME}
echo

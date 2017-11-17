#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
OUTPUT_DIR="${SCRIPT_DIR}/../"

# ===========================================================================
# Configure Jenkins Pipeline
# ===========================================================================
PIPELINE_NAME=${1}
GIT_URI=${2}
GIT_REF=${3}
CONTEXT_DIR=${4}
JENKINSFILE_PATH=${5}

BUILD_CONFIG_POST_FIX=${6}
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
if [ -z "$PIPELINE_NAME" ]; then
	echo "You must supply PIPELINE_NAME."
	MissingParam=1
fi

if [ -z "$GIT_URI" ]; then
	echo "You must supply GIT_URI."
	MissingParam=1
fi

if [ -z "$GIT_REF" ]; then
	echo "Warning - GIT_REF is blank."
	echo
fi

if [ -z "$CONTEXT_DIR" ]; then
	echo "Warning - CONTEXT_DIR is blank."
	echo
fi

if [ -z "$JENKINSFILE_PATH" ]; then
	echo "Warning - JENKINSFILE_PATH is blank."
	echo
fi

if [ -z "$BUILD_CONFIG_POST_FIX" ]; then
	BUILD_CONFIG_POST_FIX="_BuildConfig.json"
	echo "Defaulting 'BUILD_CONFIG_POST_FIX' to ${BUILD_CONFIG_POST_FIX} ..."
	echo
fi

if [ ! -z "$MissingParam" ]; then
	echo "============================================"
	echo "One or more parameters are missing!"
	echo "--------------------------------------------"	
	echo "PIPELINE_NAME[{1}]: ${1}"
	echo "GIT_URI[{2}]: ${2}"
	echo "GIT_REF[{3}]: ${3}"
	echo "CONTEXT_DIR[{4}]: ${4}"
	echo "JENKINSFILE_PATH[{5}]: ${5}"
	echo "BUILD_CONFIG_POST_FIX[{6}]: ${6}"	
    echo "============================================"
	echo
	exit 1
fi
# -----------------------------------------------------------------------------------
BUILD_CONFIG_TEMPLATE=https://raw.githubusercontent.com/BCDevOps/openshift-tools/master/provisioning/pipeline/resources/pipeline-build.json
BUILD_CONFIG=${OUTPUT_DIR}${PIPELINE_NAME}-Pipeline${BUILD_CONFIG_POST_FIX}
# ===================================================================================

echo "Generating Jenkins pipeline build configuration for ${BUILD_NAME} ..."

if [ ! -z "$DEBUG_MESSAGES" ]; then
	echo
	echo "------------------------------------------------------------------------"
	echo "Parameters for call to 'oc process' for ${BUILD_NAME} ..."
	echo "------------------------------------------------------------------------"
	echo "Template=${BUILD_CONFIG_TEMPLATE}"
	echo "NAME=${PIPELINE_NAME}"
	echo "SOURCE_REPOSITORY_URL=${GIT_URI}"
	echo "SOURCE_REPOSITORY_REF=${GIT_REF}"
	echo "CONTEXT_DIR=${CONTEXT_DIR}"
	echo "JENKINSFILE_PATH=${JENKINSFILE_PATH}"
	echo "Output File=${BUILD_CONFIG}"
	echo "------------------------------------------------------------------------"
	echo
fi

oc process \
-f ${BUILD_CONFIG_TEMPLATE} \
-p NAME=${PIPELINE_NAME} \
-p SOURCE_REPOSITORY_URL=${GIT_URI} \
-p SOURCE_REPOSITORY_REF=${GIT_REF} \
-p CONTEXT_DIR=${CONTEXT_DIR} \
-p JENKINSFILE_PATH=${JENKINSFILE_PATH} \
> ${BUILD_CONFIG}
echo "Generated ${BUILD_CONFIG} ..."
echo

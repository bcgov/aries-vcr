#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
OUTPUT_DIR="${SCRIPT_DIR}/../"
TEMPLATE_DIR="${SCRIPT_DIR}/../templates/"

# ===========================================================================
# Generate Build Configuration
# ===========================================================================
GIT_URI=${1}
GIT_REF=${2}
BUILD_NAME=${3}
OUTPUT_IMAGE_TAG=${4}
BUILD_CONFIG_TEMPLATE=${5}
BUILD_CONFIG_POST_FIX=${6}
SOURCE_CONTEXT_DIR=${7}
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
if [ -z "$GIT_URI" ]; then
	echo "You must supply GIT_URI."
	MissingParam=1
fi

if [ -z "$GIT_REF" ]; then
	echo "You must supply GIT_REF."
	MissingParam=1
fi

if [ -z "$BUILD_NAME" ]; then
	BUILD_NAME="angular-builder"
	echo "Defaulting 'BUILD_NAME' to ${BUILD_NAME} ..."
	echo
fi

if [ -z "$OUTPUT_IMAGE_TAG" ]; then
	OUTPUT_IMAGE_TAG="latest"
	echo "Defaulting 'OUTPUT_IMAGE_TAG' to ${OUTPUT_IMAGE_TAG} ..."
	echo
fi

if [ -z "$BUILD_CONFIG_TEMPLATE" ]; then
	BUILD_CONFIG_TEMPLATE="${TEMPLATE_DIR}angular-builder/angular-builder.json"
	echo "Defaulting 'BUILD_CONFIG_TEMPLATE' to ${BUILD_CONFIG_TEMPLATE} ..."
	echo
fi

if [ -z "$BUILD_CONFIG_POST_FIX" ]; then
	BUILD_CONFIG_POST_FIX="_BuildConfig.json"
	echo "Defaulting 'BUILD_CONFIG_POST_FIX' to ${BUILD_CONFIG_POST_FIX} ..."
	echo
fi

if [ -z "$SOURCE_CONTEXT_DIR" ]; then
	SOURCE_CONTEXT_DIR="prototypes/tob-web/openshift/templates/angular-builder"
	echo "Defaulting 'SOURCE_CONTEXT_DIR' to ${SOURCE_CONTEXT_DIR} ..."
	echo
fi

if [ ! -z "$MissingParam" ]; then
	echo "============================================"
	echo "One or more parameters are missing!"
	echo "--------------------------------------------"	
	echo "GIT_URI[{1}]: ${1}"
	echo "GIT_REF[{2}]: ${2}"
	echo "BUILD_NAME[{3}]: ${3}"
	echo "OUTPUT_IMAGE_TAG[{4}]: ${4}"
	echo "BUILD_CONFIG_TEMPLATE[{5}]: ${5}"
	echo "BUILD_CONFIG_POST_FIX[{6}]: ${6}"
	echo "SOURCE_CONTEXT_DIR[{7}]: ${7}"
    echo "============================================"
	echo
	exit 1
fi
# -----------------------------------------------------------------------------------
BUILD_CONFIG=${OUTPUT_DIR}${BUILD_NAME}${BUILD_CONFIG_POST_FIX}
# ===================================================================================

echo "Generating build configuration for ${BUILD_NAME} ..."

if [ ! -z "$DEBUG_MESSAGES" ]; then
	echo
	echo "------------------------------------------------------------------------"
	echo "Parameters for call to 'oc process' for ${BUILD_NAME} ..."
	echo "------------------------------------------------------------------------"
	echo "Template=${BUILD_CONFIG_TEMPLATE}"
	echo "NAME=${BUILD_NAME}"
	echo "GIT_REPO_URL=${GIT_URI}"
	echo "GIT_REF=${GIT_REF}"
	echo "SOURCE_CONTEXT_DIR=${SOURCE_CONTEXT_DIR}"
	echo "OUTPUT_IMAGE_TAG=${OUTPUT_IMAGE_TAG}"
	echo "Output File=${BUILD_CONFIG}"
	echo "------------------------------------------------------------------------"
	echo
fi

oc process \
-f ${BUILD_CONFIG_TEMPLATE} \
-p NAME=${BUILD_NAME} \
-p GIT_REPO_URL=${GIT_URI} \
-p GIT_REF=${GIT_REF} \
-p SOURCE_CONTEXT_DIR=${SOURCE_CONTEXT_DIR} \
-p OUTPUT_IMAGE_TAG=${OUTPUT_IMAGE_TAG} \
> ${BUILD_CONFIG}
echo "Generated ${BUILD_CONFIG} ..."
echo

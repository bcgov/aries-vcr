#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"

# ===================================================================================
# Script for initializing an OpenShift project environment.
#
# * Requires the OpenShift Origin CLI
# -----------------------------------------------------------------------------------
# Usage on Windows:
#  MSYS_NO_PATHCONV=1 ./initializeProjects.sh
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
PROJECT_NAMESPACE="${1}"
TOOLS_PROJECT_NAME="${2}"
DEV_PROJECT_NAME="${3}"
TEST_PROJECT_NAME="${4}"
PROD_PROJECT_NAME="${5}"
# -----------------------------------------------------------------------------------
if [ -z "$PROJECT_NAMESPACE" ]; then
	echo "You must supply PROJECT_NAMESPACE."
	echo -n "Please enter the root namespace of the project; for example 'devex-von': "
	read PROJECT_NAMESPACE
	PROJECT_NAMESPACE="$(echo "${PROJECT_NAMESPACE}" | tr '[:upper:]' '[:lower:]')"
	echo
fi

if [ -z "$TOOLS_PROJECT_NAME" ]; then
	TOOLS_PROJECT_NAME="tools"
	echo "Defaulting 'TOOLS_PROJECT_NAME' to ${TOOLS_PROJECT_NAME} ..."
	echo
fi

if [ -z "$DEV_PROJECT_NAME" ]; then
	DEV_PROJECT_NAME="dev"
	echo "Defaulting 'DEV_PROJECT_NAME' to ${DEV_PROJECT_NAME} ..."
	echo
fi

if [ -z "$TEST_PROJECT_NAME" ]; then
	TEST_PROJECT_NAME="test"
	echo "Defaulting 'TEST_PROJECT_NAME' to ${TEST_PROJECT_NAME} ..."
	echo
fi

if [ -z "$PROD_PROJECT_NAME" ]; then
	PROD_PROJECT_NAME="prod"
	echo "Defaulting 'PROD_PROJECT_NAME' to ${PROD_PROJECT_NAME} ..."
	echo
fi
# -----------------------------------------------------------------------------------
TOOLS_PROJECT="${PROJECT_NAMESPACE}-${TOOLS_PROJECT_NAME}"
DEV_PROJECT="${PROJECT_NAMESPACE}-${DEV_PROJECT_NAME}"
TEST_PROJECT="${PROJECT_NAMESPACE}-${TEST_PROJECT_NAME}"
PROD_PROJECT="${PROJECT_NAMESPACE}-${PROD_PROJECT_NAME}"
# ===================================================================================

echo "============================================================================="
echo "Initializing project permissions ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/grantDeploymentPrivileges.sh \
	${DEV_PROJECT} \
	${TOOLS_PROJECT}

${SCRIPTS_DIR}/grantDeploymentPrivileges.sh \
	${TEST_PROJECT} \
	${TOOLS_PROJECT}

${SCRIPTS_DIR}/grantDeploymentPrivileges.sh \
	${PROD_PROJECT} \
	${TOOLS_PROJECT}

echo "============================================================================"
echo

echo "============================================================================="
echo "Initializing project Glusterfs Services ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/createGlusterfsClusterApp.sh \
	${TOOLS_PROJECT}

${SCRIPTS_DIR}/createGlusterfsClusterApp.sh \
	${DEV_PROJECT}

${SCRIPTS_DIR}/createGlusterfsClusterApp.sh \
	${TEST_PROJECT}

${SCRIPTS_DIR}/createGlusterfsClusterApp.sh \
	${PROD_PROJECT}

echo "============================================================================"
echo

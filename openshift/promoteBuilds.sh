#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=${DIR}

export MSYS_NO_PATHCONV=1
# ==============================================================================
# Script for setting up the deployment environment in OpenShift
#
# * Requires the OpenShift Origin CLI
# ------------------------------------------------------------------------------
# Usage on Windows:
#  ./promoteBuilds.sh [project_namespace] [deployment_env_name] [build_env_name]
#
# Example:
#  ./promoteBuilds.sh devex-von dev tools
# ------------------------------------------------------------------------------
# ToDo:
# * Add support for create or update.
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
PROJECT_NAMESPACE="${1}"
DEPLOYMENT_ENV_NAME="${2}"
BUILD_ENV_NAME="${3}"
# -----------------------------------------------------------------------------------
if [ -z "$PROJECT_NAMESPACE" ]; then
	echo "You must supply PROJECT_NAMESPACE."
	echo -n "Please enter the root namespace of the project; for example 'devex-von': "
	read PROJECT_NAMESPACE
	PROJECT_NAMESPACE="$(echo "${PROJECT_NAMESPACE}" | tr '[:upper:]' '[:lower:]')"
	echo
fi

if [ -z "$DEPLOYMENT_ENV_NAME" ]; then
	DEPLOYMENT_ENV_NAME="dev"
	echo "Defaulting 'DEPLOYMENT_ENV_NAME' to ${DEPLOYMENT_ENV_NAME} ..."
	echo
fi

if [ -z "$BUILD_ENV_NAME" ]; then
	BUILD_ENV_NAME="tools"
	echo "Defaulting 'BUILD_ENV_NAME' to ${BUILD_ENV_NAME} ..."
	echo
fi

if [ ! -z "$MissingParam" ]; then
	echo "============================================"
	echo "One or more parameters are missing!"
	echo "--------------------------------------------"
	echo "PROJECT_NAMESPACE[{1}]: ${1}"
	echo "DEPLOYMENT_ENV_NAME[{2}]: ${2}"
	echo "BUILD_ENV_NAME[{3}]: ${3}"
	echo "============================================"
	echo
	exit 1
fi
# -------------------------------------------------------------------------------------
DEPLOYMENT_PROJECT_NAME="${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME}"
BUILD_PROJECT_NAME="${PROJECT_NAMESPACE}-${BUILD_ENV_NAME}"
# -------------------------------------------------------------------------------------
SOLR_IMAGE_NAME=solr
DJANGO_IMAGE_NAME=django
ANGULAR_IMAGE_NAME=angular-on-nginx
SCHEMA_SPY_IMAGE_NAME=schema-spy
# ==============================================================================

echo "============================================================================="
echo "Switching to project ${BUILD_PROJECT_NAME} ..."
echo "-----------------------------------------------------------------------------"
oc project ${BUILD_PROJECT_NAME}
echo "============================================================================"
echo 

oc tag ${SOLR_IMAGE_NAME}:latest ${SOLR_IMAGE_NAME}:${DEPLOYMENT_ENV_NAME} --namespace=${BUILD_PROJECT_NAME}
oc tag ${DJANGO_IMAGE_NAME}:latest ${DJANGO_IMAGE_NAME}:${DEPLOYMENT_ENV_NAME} --namespace=${BUILD_PROJECT_NAME}
oc tag ${ANGULAR_IMAGE_NAME}:latest ${ANGULAR_IMAGE_NAME}:${DEPLOYMENT_ENV_NAME} --namespace=${BUILD_PROJECT_NAME}
oc tag ${SCHEMA_SPY_IMAGE_NAME}:latest ${SCHEMA_SPY_IMAGE_NAME}:${DEPLOYMENT_ENV_NAME} --namespace=${BUILD_PROJECT_NAME}
#!/bin/bash

USER_ID="$(id -u)"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_DIR=${DIR}
THIS_SCRIPT_PATH=${SCRIPT_DIR}/$(basename $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"
PROJECT_ROOT="${SCRIPT_DIR}/.."

export MSYS_NO_PATHCONV=1
# ==============================================================================
# Script for setting up a set of deployment environments in OpenShift
#
# * Requires the OpenShift Origin CLI
# ------------------------------------------------------------------------------
# Usage on Windows:
#  ./generateDeployments.sh [project_namespace] [deployment_env_name] [build_env_name]
#
# Example:
#  ./generateDeployments.sh devex-von dev tools
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
DEPLOYMENT_SCRIPT_NAME=generateDeployments.sh
# ==============================================================================

DEPLOYMENT_SCRIPTS=$(find . ${PROJECT_ROOT} -name "${DEPLOYMENT_SCRIPT_NAME}")
for SCRIPT in ${DEPLOYMENT_SCRIPTS}
	do
		SCRIPT=$(realpath ${SCRIPT})
		if [ ${SCRIPT} != ${THIS_SCRIPT_PATH} ]; then
			${SCRIPT} ${@}
		fi
	done

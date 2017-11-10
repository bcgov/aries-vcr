#!/bin/bash

export MSYS_NO_PATHCONV=1

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"
TEMPLATE_DIR="${SCRIPT_DIR}/templates"
# oc create does not like absolute paths
TEMPLATE_DIR=${TEMPLATE_DIR/${SCRIPT_DIR}/.}

changeDir (){
	#echo "Switching working directory to ${SCRIPT_DIR} ..."
	ORG_DIR=$(pwd)
	cd ${SCRIPT_DIR}
}

resetDir (){
	#echo "Switching working directory to ${ORG_DIR} ..."
	cd ${ORG_DIR}
}

changeDir
# ==============================================================================
# Script for setting up the deployment environment in OpenShift
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
	PROJECT_NAMESPACE="$(echo "${PROJECT_NAMESPACE}" | LC_CTYPE=C tr '[:upper:]' '[:lower:]')"
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
DeploymentConfigPostfix="_DeploymentConfig.json"

DEPLOYMENT_PROJECT_NAME="${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME}"
BUILD_PROJECT_NAME="${PROJECT_NAMESPACE}-${BUILD_ENV_NAME}"
# -------------------------------------------------------------------------------------
DJANGO_DEPLOYMENT_NAME="django"
DATABASE_SERVICES_NAME="postgresql"
DATABASE_ENGINE="postgresql"
DATABASE_NAME="TheOrgBook_Database"
SOLR_SERVICE_NAME="solr"
SOLR_CORE_NAME="the_org_book"

if [ ${DEPLOYMENT_ENV_NAME} = "dev" ]; then
	DJANGO_DEBUG="True"
else
	DJANGO_DEBUG="False"
fi

if [ -z "${DJANGO_SECRET_KEY}" ]; then
	echo "DJANGO_SECRET_KEY will be auto generated ..."
	DJANGO_SECRET_KEY=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9_' | fold -w 50 | head -n 1)
fi

SCHEMA_SPY_DEPLOYMENT_NAME="schema-spy"
# ==============================================================================

echo "============================================================================="
echo "Switching to project ${DEPLOYMENT_PROJECT_NAME} ..."
echo "-----------------------------------------------------------------------------"
oc project ${DEPLOYMENT_PROJECT_NAME}
echo "============================================================================"
echo

echo "============================================================================="
echo "Deleting previous deployment configuration files ..."
echo "-----------------------------------------------------------------------------"
for file in *${DeploymentConfigPostfix}; do
	echo "Deleting ${file} ..."
	rm -rf ${file};
done
echo "============================================================================="
echo

echo "============================================================================="
echo "Generating deployment configuration for ${DJANGO_DEPLOYMENT_NAME} ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/configureDeployment.sh \
	${DJANGO_DEPLOYMENT_NAME} \
	${DEPLOYMENT_ENV_NAME} \
	${BUILD_PROJECT_NAME} \
	"${DJANGO_DEPLOYMENT_NAME}-${DEPLOYMENT_PROJECT_NAME}.pathfinder.gov.bc.ca" \
	"512Mi" \
	${DATABASE_SERVICES_NAME} \
	${DATABASE_ENGINE} \
	${DATABASE_NAME} \
	"" \
	${DJANGO_SECRET_KEY} \
	${DJANGO_DEBUG} \
	${DATABASE_SERVICES_NAME} \
	${SOLR_SERVICE_NAME} \
	${SOLR_CORE_NAME} \
	"${TEMPLATE_DIR}/${DJANGO_DEPLOYMENT_NAME}-deploy.json"

echo "============================================================================="
echo

echo "============================================================================="
echo "Generating deployment configuration for ${SCHEMA_SPY_DEPLOYMENT_NAME} ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/configureSchemaSpyDeployment.sh \
	${SCHEMA_SPY_DEPLOYMENT_NAME} \
	${DEPLOYMENT_ENV_NAME} \
	${BUILD_PROJECT_NAME} \
	"${SCHEMA_SPY_DEPLOYMENT_NAME}-${DEPLOYMENT_PROJECT_NAME}.pathfinder.gov.bc.ca" \
	"512Mi" \
	${DATABASE_SERVICES_NAME} \
	${DATABASE_NAME} \
	${DATABASE_SERVICES_NAME} \
	"${TEMPLATE_DIR}/${SCHEMA_SPY_DEPLOYMENT_NAME}-deploy.json"

echo "============================================================================="
echo

# echo "============================================================================="
# echo "Creating deployment configurations in OpenShift project; ${DEPLOYMENT_PROJECT_NAME} ..."
# echo "-----------------------------------------------------------------------------"
# for file in *${DeploymentConfigPostfix}; do
	# echo "Loading ${file} ...";
	# oc create -f ${file};
	# echo;
# done
# echo "============================================================================="
# echo

resetDir
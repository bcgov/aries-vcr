#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"
TEMPLATE_DIR="${SCRIPT_DIR}/templates"

# ==============================================================================
# Script for setting up the build environment in OpenShift
#
# * Requires the OpenShift Origin CLI
# ------------------------------------------------------------------------------
# Usage on Windows:
#  MSYS_NO_PATHCONV=1 ./generateBuilds.sh [project_name] [git_ref] [git_uri]
# 
# Example:
#  MSYS_NO_PATHCONV=1 ./generateBuilds.sh devex-von-tools master https://github.com/bcgov/TheOrgBook.git
# ------------------------------------------------------------------------------
# ToDo:
# * Add support for create or update.
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
PROJECT_NAME="${1}"
GIT_REF="${2}"
GIT_URI="${3}"
# -----------------------------------------------------------------------------------
if [ -z "$PROJECT_NAME" ]; then
	echo "You must supply PROJECT_NAME."
	echo -n "Please enter the name of the tools project; for example 'devex-von-tools': "
	read PROJECT_NAME
	PROJECT_NAME="$(echo "${PROJECT_NAME}" | tr '[:upper:]' '[:lower:]')"
	echo
fi

if [ -z "$GIT_REF" ]; then
	GIT_REF="master"
	echo "Defaulting 'GIT_REF' to ${GIT_REF} ..."
	echo
fi

if [ -z "$GIT_URI" ]; then
	GIT_URI="https://github.com/bcgov/TheOrgBook.git"
	echo "Defaulting 'GIT_URI' to ${GIT_URI} ..."
	echo
fi

if [ ! -z "$MissingParam" ]; then
	echo "============================================"
	echo "One or more parameters are missing!"
	echo "--------------------------------------------"	
	echo "PROJECT_NAME[{1}]: ${1}"
	echo "GIT_REF[{2}]: ${2}"
	echo "GIT_URI[{3}]: ${3}"
	echo "============================================"
	echo
	exit 1
fi
# -------------------------------------------------------------------------------------
BuildConfigPostfix="_BuildConfig.json"
CONTEXT_DIR_ROOT="prototypes/tob-web"
TEMPLATE_CONTEXT_DIR_ROOT="${CONTEXT_DIR_ROOT}/openshift/templates"
ANGULAR_BUILDER_NAME="angular-builder"
NGINX_RUNTIME_NAME="nginx-runtime"
ANGULAR_ON_NGINX_NAME="angular-on-nginx"
# ==============================================================================

echo "============================================================================="
echo "Switching to project ${PROJECT_NAME} ..."
echo "-----------------------------------------------------------------------------"
oc project ${PROJECT_NAME}
echo "============================================================================"
echo 

echo "============================================================================="
echo "Deleting previous build configuration files ..."
echo "-----------------------------------------------------------------------------"
for file in *${BuildConfigPostfix}; do 
	echo "Deleting ${file} ..."
	rm -rf ${file};
done
echo "============================================================================="
echo

echo "============================================================================="
echo "Generating build configuration for ${ANGULAR_BUILDER_NAME} ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/configureBuild.sh \
	${GIT_URI} \
	${GIT_REF} \
	"${TEMPLATE_CONTEXT_DIR_ROOT}/${ANGULAR_BUILDER_NAME}/" \
	"${ANGULAR_BUILDER_NAME}" \
	"${TEMPLATE_DIR}/${ANGULAR_BUILDER_NAME}/${ANGULAR_BUILDER_NAME}.json"

echo "============================================================================="
echo

echo "============================================================================="
echo "Generating build configuration for ${NGINX_RUNTIME_NAME} ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/configureBuild.sh \
	${GIT_URI} \
	${GIT_REF} \
	"${TEMPLATE_CONTEXT_DIR_ROOT}/${NGINX_RUNTIME_NAME}/" \
	"${NGINX_RUNTIME_NAME}" \
	"${TEMPLATE_DIR}/${NGINX_RUNTIME_NAME}/${NGINX_RUNTIME_NAME}.json"
echo "============================================================================="
echo

echo "============================================================================="
echo "Generating build configuration for ${ANGULAR_ON_NGINX_NAME} ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/configureBuild.sh \
	${GIT_URI} \
	${GIT_REF} \
	"${CONTEXT_DIR_ROOT}/" \
	"${ANGULAR_ON_NGINX_NAME}" \
	"${TEMPLATE_DIR}/${ANGULAR_ON_NGINX_NAME}/${ANGULAR_ON_NGINX_NAME}-build.json"
echo "============================================================================="
echo

echo "============================================================================="
echo "Cleaning out existing OpenShift resources ..."
echo "============================================================================"
oc delete imagestreams,bc --all
echo

echo "============================================================================="
echo "Creating build configurations in OpenShift project; ${PROJECT_NAME} ..."
echo "============================================================================="
for file in *${BuildConfigPostfix}; do 
	echo "Loading ${file} ...";
	oc create -f ${file};
	echo;
done
echo

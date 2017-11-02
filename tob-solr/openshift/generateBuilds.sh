#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"
TEMPLATE_DIR="${SCRIPT_DIR}/templates"

export MSYS_NO_PATHCONV=1
# ==============================================================================
# Script for setting up the build environment in OpenShift
#
# * Requires the OpenShift Origin CLI
# ------------------------------------------------------------------------------
# Usage on Windows:
#  ./generateBuilds.sh [project_name] [git_ref] [git_uri]
#
# Example:
#  ./generateBuilds.sh devex-von-tools master https://github.com/bcgov/TheOrgBook.git
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
	GIT_URI="https://github.com/bcgov/openshift-solr.git"
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

SOLR_BASE_BUILD_NAME="solr-base"
SOLR_BASE_GIT_URI="https://github.com/bcgov/openshift-solr.git"
SOLR_BASE_GIT_REF="master"
SOLR_BASE_CONTEXT_DIR_ROOT=""

SOLR_BUILD_NAME="solr"
SOLR_GIT_URI=${GIT_URI}
SOLR_GIT_REF=${GIT_REF}
SOLR_CONTEXT_DIR_ROOT="tob-solr/cores"
SOLR_SOURCE_IMAGE_NAME="${SOLR_BASE_BUILD_NAME}"
SOLR_SOURCE_IMAGE_TAG="latest"
SOLR_SOURCE_IMAGE_NAMESPACE="${PROJECT_NAME}"
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
echo "Generating build configuration for ${SOLR_BASE_BUILD_NAME} ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/configureBaseBuild.sh \
	"${SOLR_BASE_GIT_URI}" \
	"${SOLR_BASE_GIT_REF}" \
	"${SOLR_BASE_CONTEXT_DIR_ROOT}" \
	${SOLR_BASE_BUILD_NAME} \
	"${TEMPLATE_DIR}/${SOLR_BASE_BUILD_NAME}-build.json"
echo "============================================================================="
echo

echo "============================================================================="
echo "Generating build configuration for ${SOLR_BUILD_NAME} ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/configureSolrBuild.sh \
	${SOLR_GIT_URI} \
	${SOLR_GIT_REF} \
	${SOLR_CONTEXT_DIR_ROOT} \
	${SOLR_BUILD_NAME} \
	"${TEMPLATE_DIR}/${SOLR_BUILD_NAME}-build.json" \
	${SOLR_SOURCE_IMAGE_NAME} \
	${SOLR_SOURCE_IMAGE_TAG} \
	${SOLR_SOURCE_IMAGE_NAMESPACE}
echo "============================================================================="
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

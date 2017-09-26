#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"

# ==============================================================================
# Script for setting up the build environment in OpenShift
#
# * Requires the OpenShift Origin CLI
# ------------------------------------------------------------------------------
# Usage on Windows:
#  MSYS_NO_PATHCONV=1 ./generateBuilds.sh
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
	PROJECT_NAME="the-org-book"
	echo "Defaulting 'PROJECT_NAME' to ${PROJECT_NAME} ..."
	echo
fi

if [ -z "$GIT_REF" ]; then
	GIT_REF="openshift"
	echo "Defaulting 'GIT_REF' to ${GIT_REF} ..."
	echo
fi

if [ -z "$GIT_URI" ]; then
	GIT_URI="https://github.com/WadeBarnes/TheOrgBook.git"
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
for file in *_BuildConfig.json; do 
	echo "Deleting ${file} ..."
	rm -rf ${file};
done
echo "============================================================================="
echo

echo "============================================================================="
echo "Generating build configuration for angular-builder ..."
echo "-----------------------------------------------------------------------------"
${SCRIPTS_DIR}/configureAngularBuilderBuild.sh \
	${GIT_URI} \
	${GIT_REF}
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
for file in *_BuildConfig.json; do 
	echo "Loading ${file} ...";
	oc create -f ${file};
	echo;
done
echo

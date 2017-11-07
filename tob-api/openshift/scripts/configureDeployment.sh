#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
OUTPUT_DIR="${SCRIPT_DIR}/../"

# ===========================================================================
# Configure Deployment
# ===========================================================================
DEPLOYMENT_NAME=${1}
TAG_NAME=${2}
IMAGE_NAMESPACE=${3}
APPLICATION_DOMAIN=${4}
MEMORY_LIMIT=${5}
DATABASE_SERVICE_NAME=${6}
DATABASE_ENGINE=${7}
DATABASE_NAME=${8}
APP_CONFIG=${9}
DJANGO_SECRET_KEY=${10}
DJANGO_DEBUG=${11}
DATABASE_DEPLOYMENT_NAME=${12}
SOLR_SERVICE_NAME=${13}
SOLR_CORE_NAME=${14}
DEPLOYMENT_CONFIG_TEMPLATE=${15}

DEPLOYMENT_CONFIG_POST_FIX=${16}
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
if [ -z "$DEPLOYMENT_NAME" ]; then
	echo "You must supply DEPLOYMENT_NAME."
	MissingParam=1
fi

if [ -z "$TAG_NAME" ]; then
	echo "You must supply TAG_NAME."
	MissingParam=1
fi

if [ -z "$IMAGE_NAMESPACE" ]; then
	echo "You must supply IMAGE_NAMESPACE."
	MissingParam=1
fi

if [ -z "$APPLICATION_DOMAIN" ]; then
	echo "You must supply APPLICATION_DOMAIN."
	MissingParam=1
fi

if [ -z "$MEMORY_LIMIT" ]; then
	echo "You must supply MEMORY_LIMIT."
	MissingParam=1
fi

if [ -z "$DATABASE_SERVICE_NAME" ]; then
	echo "You must supply DATABASE_SERVICE_NAME."
	MissingParam=1
fi

if [ -z "$DATABASE_ENGINE" ]; then
	echo "You must supply DATABASE_ENGINE."
	MissingParam=1
fi

if [ -z "$DATABASE_NAME" ]; then
	echo "You must supply DATABASE_NAME."
	MissingParam=1
fi

if [ -z "$APP_CONFIG" ]; then
	echo "WARNING; APP_CONFIG has not been specified."
fi

if [ -z "$DJANGO_SECRET_KEY" ]; then
	echo "You must supply DJANGO_SECRET_KEY."
	MissingParam=1
fi

if [ -z "$DJANGO_DEBUG" ]; then
	echo "You must supply DJANGO_DEBUG."
	MissingParam=1
fi

if [ -z "$DATABASE_DEPLOYMENT_NAME" ]; then
	echo "You must supply DATABASE_DEPLOYMENT_NAME."
	MissingParam=1
fi

if [ -z "$SOLR_SERVICE_NAME" ]; then
	echo "Warning SOLR_SERVICE_NAME is blank."
fi

if [ -z "$SOLR_CORE_NAME" ]; then
	echo "Warning SOLR_CORE_NAME is blank."
fi

if [ -z "$DEPLOYMENT_CONFIG_TEMPLATE" ]; then
	echo "You must supply DEPLOYMENT_CONFIG_TEMPLATE."
	MissingParam=1
fi

if [ -z "$DEPLOYMENT_CONFIG_POST_FIX" ]; then
	DEPLOYMENT_CONFIG_POST_FIX="_DeploymentConfig.json"
	echo "Defaulting 'DEPLOYMENT_CONFIG_POST_FIX' to ${DEPLOYMENT_CONFIG_POST_FIX} ..."
	echo
fi

if [ ! -z "$MissingParam" ]; then
	echo "============================================"
	echo "One or more parameters are missing!"
	echo "--------------------------------------------"	
	echo "DEPLOYMENT_NAME[{1}]: ${1}"
	echo "TAG_NAME[{2}]: ${2}"
	echo "IMAGE_NAMESPACE[{3}]: ${3}"
	echo "APPLICATION_DOMAIN[{4}]: ${4}"
	echo "MEMORY_LIMIT[{5}]: ${5}"
	echo "DATABASE_SERVICE_NAME[{6}]: ${6}"
	echo "DATABASE_ENGINE[{7}]: ${7}"
	echo "DATABASE_NAME[{8}]: ${8}"
	echo "APP_CONFIG[{9}]: ${9}"
	echo "DJANGO_SECRET_KEY[{10}]: ${10}"
	echo "DJANGO_DEBUG[{11}]: ${11}"
	echo "DATABASE_DEPLOYMENT_NAME[{12}]: ${12}"
	echo "SOLR_SERVICE_NAME[{13}]: ${13}"
	echo "SOLR_CORE_NAME[{14}]: ${14}"
	echo "DEPLOYMENT_CONFIG_TEMPLATE[{15}]: ${15}"
	echo "DEPLOYMENT_CONFIG_POST_FIX[{16}]: ${16}"
    echo "============================================"
	echo
	exit 1
fi
# -----------------------------------------------------------------------------------
DEPLOYMENT_CONFIG=${OUTPUT_DIR}${DEPLOYMENT_NAME}${DEPLOYMENT_CONFIG_POST_FIX}
# ===================================================================================

echo "Generating deployment configuration for ${DEPLOYMENT_NAME} ..."

if [ ! -z "$DEBUG_MESSAGES" ]; then
	echo
	echo "------------------------------------------------------------------------"
	echo "Parameters for call to 'oc process' for ${DEPLOYMENT_NAME} ..."
	echo "------------------------------------------------------------------------"
	echo "Template=${DEPLOYMENT_CONFIG_TEMPLATE}"
	echo "NAME=${DEPLOYMENT_NAME}"
	echo "TAG_NAME=${TAG_NAME}"
	echo "IMAGE_NAMESPACE=${IMAGE_NAMESPACE}"
	echo "APPLICATION_DOMAIN=${APPLICATION_DOMAIN}"
	echo "MEMORY_LIMIT=${MEMORY_LIMIT}"
	echo "DATABASE_SERVICE_NAME=${DATABASE_SERVICE_NAME}"
	echo "DATABASE_ENGINE=${DATABASE_ENGINE}"
	echo "DATABASE_NAME=${DATABASE_NAME}"
	echo "APP_CONFIG=${APP_CONFIG}"
	echo "DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}"
	echo "DJANGO_DEBUG=${DJANGO_DEBUG}"
	echo "DATABASE_DEPLOYMENT_NAME=${DATABASE_DEPLOYMENT_NAME}"
	echo "SOLR_SERVICE_NAME=${SOLR_SERVICE_NAME}"
	echo "SOLR_CORE_NAME=${SOLR_CORE_NAME}"
	echo "Output File=${DEPLOYMENT_CONFIG}"	
	echo "------------------------------------------------------------------------"
	echo
fi

oc process \
-f ${DEPLOYMENT_CONFIG_TEMPLATE} \
-p NAME=${DEPLOYMENT_NAME} \
-p TAG_NAME=${TAG_NAME} \
-p IMAGE_NAMESPACE=${IMAGE_NAMESPACE} \
-p APPLICATION_DOMAIN=${APPLICATION_DOMAIN} \
-p MEMORY_LIMIT=${MEMORY_LIMIT} \
-p DATABASE_SERVICE_NAME=${DATABASE_SERVICE_NAME} \
-p DATABASE_ENGINE=${DATABASE_ENGINE} \
-p DATABASE_NAME=${DATABASE_NAME} \
-p APP_CONFIG=${APP_CONFIG} \
-p DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY} \
-p DJANGO_DEBUG=${DJANGO_DEBUG} \
-p DATABASE_DEPLOYMENT_NAME=${DATABASE_DEPLOYMENT_NAME} \
-p SOLR_SERVICE_NAME=${SOLR_SERVICE_NAME} \
-p SOLR_CORE_NAME=${SOLR_CORE_NAME} \
> ${DEPLOYMENT_CONFIG}
echo "Generated ${DEPLOYMENT_CONFIG} ..."
echo

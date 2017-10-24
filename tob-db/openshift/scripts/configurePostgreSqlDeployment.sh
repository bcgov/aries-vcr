#!/bin/bash

USER_ID="$(id -u)"
SCRIPT_DIR=$(dirname $0)
OUTPUT_DIR="${SCRIPT_DIR}/../"

# ===========================================================================
# Configure Deployment
# ===========================================================================
NAME=${1}
MEMORY_LIMIT=${2}
PERSISTENT_VOLUME_SIZE=${3}
POSTGRESQL_DATABASE_NAME=${4}
POSTGRESQL_USER=${5}
POSTGRESQL_PASSWORD=${6}
DEPLOYMENT_CONFIG_TEMPLATE=${7}

DEPLOYMENT_CONFIG_POST_FIX=${8}
# -----------------------------------------------------------------------------------
#DEBUG_MESSAGES=1
# -----------------------------------------------------------------------------------
if [ -z "$NAME" ]; then
	echo "You must supply NAME."
	MissingParam=1
fi

if [ -z "$MEMORY_LIMIT" ]; then
	echo "You must supply MEMORY_LIMIT."
	MissingParam=1
fi

if [ -z "$PERSISTENT_VOLUME_SIZE" ]; then
	echo "You must supply PERSISTENT_VOLUME_SIZE."
	MissingParam=1
fi

if [ -z "$POSTGRESQL_DATABASE_NAME" ]; then
	echo "You must supply POSTGRESQL_DATABASE_NAME."
	MissingParam=1
fi

if [ -z "$POSTGRESQL_USER" ]; then
	echo "You must supply POSTGRESQL_USER."
	MissingParam=1
fi

if [ -z "$POSTGRESQL_PASSWORD" ]; then
	echo "POSTGRESQL_PASSWORD will be auto generated ..."
	POSTGRESQL_PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9_@#=;:|' | fold -w 16 | head -n 1)
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
	echo "NAME[{1}]: ${1}"
	echo "MEMORY_LIMIT[{2}]: ${2}"
	echo "PERSISTENT_VOLUME_SIZE[{3}]: ${3}"
	echo "POSTGRESQL_DATABASE_NAME[{4}]: ${4}"
	echo "POSTGRESQL_USER[{5}]: ${5}"
	echo "POSTGRESQL_PASSWORD[{6}]: ${6}"
	echo "DEPLOYMENT_CONFIG_TEMPLATE[{7}]: ${7}"
	echo "DEPLOYMENT_CONFIG_POST_FIX[{8}]: ${8}"
    echo "============================================"
	echo
	exit 1
fi
# -----------------------------------------------------------------------------------
DEPLOYMENT_CONFIG=${OUTPUT_DIR}${NAME}${DEPLOYMENT_CONFIG_POST_FIX}
# ===================================================================================

echo "Generating deployment configuration for ${NAME} ..."

if [ ! -z "$DEBUG_MESSAGES" ]; then
	echo
	echo "------------------------------------------------------------------------"
	echo "Parameters for call to 'oc process' for ${NAME} ..."
	echo "------------------------------------------------------------------------"
	echo "Template=${DEPLOYMENT_CONFIG_TEMPLATE}"
	echo "NAME=${NAME}"
	echo "MEMORY_LIMIT=${MEMORY_LIMIT}"
	echo "PERSISTENT_VOLUME_SIZE=${PERSISTENT_VOLUME_SIZE}"
	echo "POSTGRESQL_DATABASE_NAME=${POSTGRESQL_DATABASE_NAME}"
	echo "POSTGRESQL_USER=${POSTGRESQL_USER}"
	echo "POSTGRESQL_PASSWORD=${POSTGRESQL_PASSWORD}"
	echo "Output File=${DEPLOYMENT_CONFIG}"
	echo "------------------------------------------------------------------------"
	echo
fi

POSTGRESQL_USER=$(echo -n "${POSTGRESQL_USER}"|base64)
POSTGRESQL_PASSWORD=$(echo -n "${POSTGRESQL_PASSWORD}"|base64)

oc process \
-f ${DEPLOYMENT_CONFIG_TEMPLATE} \
-p NAME=${NAME} \
-p MEMORY_LIMIT=${MEMORY_LIMIT} \
-p PERSISTENT_VOLUME_SIZE=${PERSISTENT_VOLUME_SIZE} \
-p POSTGRESQL_DATABASE_NAME=${POSTGRESQL_DATABASE_NAME} \
-p POSTGRESQL_USER=${POSTGRESQL_USER} \
-p POSTGRESQL_PASSWORD=${POSTGRESQL_PASSWORD} \
> ${DEPLOYMENT_CONFIG}
echo "Generated ${DEPLOYMENT_CONFIG} ..."
echo

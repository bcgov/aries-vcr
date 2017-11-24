#!/bin/bash

SCRIPT_DIR=$(dirname $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"

_component_name=${1}
if [ -z "${_component_name}" ]; then
  echo -e \\n"Missing parameter!"\\n
  exit 1
fi

if [ -f ${SCRIPTS_DIR}/commonFunctions.inc ]; then
  . ${SCRIPTS_DIR}/commonFunctions.inc
fi
loadComponentSettings

# Turn on debugging if asked
if [ ! -z "${DEBUG}" ]; then
  set -x
fi

# Get list of JSON files - could be in multiple directories below
# To Do: Remove the change into TEMPLATE_DIR - just find all deploy templates
pushd ${TEMPLATE_DIR} >/dev/null
DEPLOYS=$(find . -name "*.json" -exec grep -l "DeploymentConfig" '{}' \; | sed "s/.json//" | xargs | sed "s/\.\///g")
popd >/dev/null

# Switch to Tools Project
oc project ${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME} >/dev/null
exitOnError

for deploy in ${DEPLOYS}; do
    echo -e "Processing deployment configuration; ${deploy} ..."\\n

    JSONFILE="${TEMPLATE_DIR}/${deploy}.json"
    JSONTMPFILE=$( basename ${deploy}_DeploymentConfig.json )
	PARAMFILE=$( basename ${deploy}.param )
	ENVPARAM=$( basename ${deploy}.${DEPLOYMENT_ENV_NAME}.param )
	LOCALPARAM=${LOCAL_DIR}/$( basename ${deploy}.local.param )

	if [ -f "${PARAMFILE}" ]; then
		PARAMFILE="--param-file=${PARAMFILE}"
	else
		PARAMFILE=""
	fi

	if [ -f "${ENVPARAM}" ]; then
		ENVPARAM="--param-file=${ENVPARAM}"
	else
		ENVPARAM=""
	fi

	if [ -f "${LOCALPARAM}" ]; then
		LOCALPARAM="--param-file=${LOCALPARAM}"
	else
		LOCALPARAM=""
	fi

  oc process --filename=${JSONFILE} ${SPECIALDEPLOYPARM} ${LOCALPARAM} ${ENVPARAM} ${PARAMFILE} > ${JSONTMPFILE}
  exitOnError
  if [ -z ${GEN_ONLY} ]; then
    oc ${OC_ACTION} -f ${JSONTMPFILE}
	exitOnError
  fi
  
  # Delete the tempfile if the keep command line option was not specified
  if [ -z "${KEEPJSON}" ]; then
    rm ${JSONTMPFILE}
  fi
done

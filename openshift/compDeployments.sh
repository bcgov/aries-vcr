#!/bin/bash

# Set project and local environment variables
if [ -f settings.sh ]; then
  . settings.sh
fi

# Turn on debugging if asked
if [ ${DEBUG} = "${YES}" ]; then
	set -x
fi

# Get list of JSON files - could be in multiple directories below
# To Do: Remove the change into TEMPLATE_DIR - just find all deploy templates
pushd ${TEMPLATE_DIR} >/dev/null
DEPLOYS=$(find . -name "*.json" -exec grep -l "DeploymentConfig" '{}' \; | sed "s/.json//" | xargs | sed "s/\.\///g")
echo -e "Files: ${DEPLOYS}"
popd >/dev/null

# Switch to Tools Project
oc project ${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME}

for deploy in ${DEPLOYS}; do
	JSONFILE="${TEMPLATE_DIR}/${deploy}.json"
  JSONTMPFILE=$( basename ${deploy}.local.json )
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

  oc process --filename=${JSONFILE} ${SPECIALDEPLOYPARM} ${LOCALPARAM} ${ENVPARAM} ${PARAMFILE} >${JSONTMPFILE}
  oc ${OC_ACTION} -f ${JSONTMPFILE}

  # Delete the tempfile if the keep command line option was not specified
  if [ "${KEEPJSON}" = "${NO}" ]; then
    rm ${JSONTMPFILE}
  fi
done

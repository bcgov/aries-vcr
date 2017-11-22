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
pushd ${TEMPLATE_DIR} >/dev/null
BUILDS=$(find . -name "*.json" -exec grep -l "BuildConfig" '{}' \; | sed "s/.json//" | xargs | sed "s/\.\///g")
popd >/dev/null

# Switch to Tools Project
oc project ${TOOLS} >/dev/null

# for build in "${${COMPONENT}-builds[@]}"; do
for build in ${BUILDS}; do
  echo -e "Processing build ${build}..."\\n

	JSONFILE="${TEMPLATE_DIR}/${build}.json"
  JSONTMPFILE=$( basename ${build}.local.json )
	PARAMFILE=$( basename ${build}.param )
	LOCALPARAM=${LOCAL_DIR}/$( basename ${build}.local.param )

	if [ -f "${PARAMFILE}" ]; then
    PARAMFILE="--param-file=${PARAMFILE}"
  else
		PARAMFILE=""
	fi

	if [ -f "${LOCALPARAM}" ]; then
    LOCALPARAM="--param-file=${LOCALPARAM}"
  else
		LOCALPARAM=""
	fi

  oc process --filename=${JSONFILE} ${LOCALPARAM} ${PARAMFILE} >${JSONTMPFILE}
  oc ${OC_ACTION} -f ${JSONTMPFILE}

  # Delete the tempfile if the keep command line option was not specified
  if [ "${KEEPJSON}" = "${NO}" ]; then
    rm ${JSONTMPFILE}
  fi

  echo -e "Review the results of generating the build for ${build}"\\n
  read -n1 -s -r -p "Press a key to continue..." key
  echo -e \\n\\n
done

# If necessary, process the Jenkins pipeline
if [ -f "${COMPONENT_JENKINSFILE}" ]; then
  if [ -f ${PIPELINEPARAM} ]; then
    PIPELINEPARAM="--param-file=${PIPELINEPARAM}"
  else
    PIPELINEPARAM=""
  fi
  echo -e "Generating Jenkins Pipeline for component ${component}"
  oc process --filename=${PIPELINE_JSON} ${PIPELINEPARAM} | \
    oc ${OC_ACTION} -f -

else
  echo -e "No Jenkinsfile (${COMPONENT_JENKINSFILE}) found, so no pipeline created"\\n
fi

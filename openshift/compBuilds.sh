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
pushd ${TEMPLATE_DIR} >/dev/null
BUILDS=$(find . -name "*.json" -exec grep -l "BuildConfig" '{}' \; | sed "s/.json//" | xargs | sed "s/\.\///g")
popd >/dev/null

# Switch to Tools Project
oc project ${TOOLS} >/dev/null
exitOnError

# for build in "${${COMPONENT}-builds[@]}"; do
for build in ${BUILDS}; do
  echo -e "Processing build configuration; ${build}..."\\n

  JSONFILE="${TEMPLATE_DIR}/${build}.json"
  JSONTMPFILE=$( basename ${build}_BuildConfig.json )
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

  oc process --filename=${JSONFILE} ${LOCALPARAM} ${PARAMFILE} > ${JSONTMPFILE}
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

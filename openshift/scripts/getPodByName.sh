#!/bin/bash

# ==============================================================================================================================
usage () {
  echo "========================================================================================"
  echo "Gets the name of a running pod instance by name and optionally by index."
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <PodName> [PodIndex]"
  echo "Where <PodName> is the name of the pod, and [PodIndex] is the index of the pod instance."
  echo
  echo "Example: ${0} django"
  echo "========================================================================================"
  exit 1
}

exitOnError () {
  rtnCd=$?
  if [ ${rtnCd} -ne 0 ]; then
	echo "An error has occurred while getting the name of the pod!  Please check the previous output message(s) for details."
    exit ${rtnCd}
  fi
}
# ==============================================================================================================================

if [ -z "${1}" ]; then
  usage
fi

POD_INSTANCE_NAME=`oc get pods -l "name=${1}" --template "{{ with index .items ${2:-0} }}{{ .metadata.name }}{{ end }}"`
exitOnError
echo ${POD_INSTANCE_NAME}



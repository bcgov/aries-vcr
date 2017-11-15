#!/bin/bash

# ==============================================================================================================================
usage () {
  echo "========================================================================================"
  echo "Scales the number of pods for a deployment to the set number."
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <deploymentConfigName> <scaleToCount>"
  echo "Where <deploymentConfigName> is the name of the deployment configuration, and <scaleToCount>"
  echo "is the number of pods to scale to."
  echo
  echo "Example: ${0} django 0"
  echo "To scale to 0 pods."
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

if [ -z "${2}" ]; then
  usage
fi

if [ ! -z "${3}" ]; then
  usage
fi

oc scale --replicas=${2} dc ${1}
exitOnError

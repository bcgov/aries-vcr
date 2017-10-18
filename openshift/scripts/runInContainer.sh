#!/bin/bash
SCRIPT_DIR=$(dirname $0)

# ==============================================================================================================================
usage () {
  echo "========================================================================================"
  echo "Runs one-off commands inside the container of a pod."
  echo
  echo "You can accomplish the same results by using regular commands from OpenShift."
  echo "This script is just wrapping calls to 'oc exec' to make it a little more"
  echo "convenient to use. In the future, the 'oc' cli tool might incorporate changes"
  echo "that make this script obsolete."
  echo
  echo "Related GitHub issues:"
  echo "- https://github.com/GoogleCloudPlatform/kubernetes/issues/8876"
  echo "- https://github.com/openshift/origin/issues/2001"
  echo
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <PodName> [PodIndex] \"<command>\""
  echo
  echo "Where:"
  echo " - <PodName> is the name of the pod."
  echo " - [PodIndex] is the index of the pod instance, and is optional."
  echo " - '<command>' is the command to run on the pod."
  echo "   It's a good idea to wrap the command in quotes as shown."
  echo "   You may need to use single or double quotes depending on the command."
  echo "   Any additional quotes in the command may need to be escaped."
  echo "   See examples for details."
  echo
  echo "Examples:"
  echo "${0} postgresql 'psql -c \"\l\"'"
  echo "${0} postgresql 'psql -c \"\du\"'"
  echo "${0} postgresql \"psql -c 'DROP DATABASE \"TheOrgBook_Database\";'\""
  echo "${0} postgresql \"psql -c 'CREATE DATABASE \"TheOrgBook_Database\";'\""
  echo "${0} postgresql \"psql -c 'GRANT ALL ON DATABASE \"TheOrgBook_Database\" TO \"TheOrgBook_User\";'\""
  echo
  echo "${0} django './manage.py migrate'"
  echo "${0} django './manage.py createsuperuser'"
  echo "${0} django './manage.py shell'"
  echo "========================================================================================"
  exit 1
}

exitOnError () {
  rtnCd=$?
  if [ ${rtnCd} -ne 0 ]; then
	echo "An error has occurred while attempting to run a command in a pod!  Please check the previous output message(s) for details."
    exit ${rtnCd}
  fi
}
# ==============================================================================================================================

if [ -z "${1}" ]; then
  usage  
elif [ -z "${2}" ]; then
  usage  
elif [ ! -z "${4}" ]; then
  usage
else
  POD_NAME=${1}
fi

if [ ! -z "${3}" ]; then
  POD_INDEX=${2}
  COMMAND=${3}
else
  POD_INDEX="0"
  COMMAND=${2}
fi

# Get name of a currently deployed pod by label and index
POD_INSTANCE_NAME=$(${SCRIPT_DIR}/getPodByName.sh ${POD_NAME} ${POD_INDEX})
exitOnError

echo
echo "Executing command on ${POD_INSTANCE_NAME}:"
echo -e "\t${COMMAND:-echo}"
echo

# Run command in a container of the specified pod:
oc exec "$POD_INSTANCE_NAME" -- bash -c "${COMMAND:-echo}"
exitOnError

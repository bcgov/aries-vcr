#!/bin/bash
SCRIPT_DIR=$(dirname $0)

# ==============================================================================================================================
usage () {
  echo "========================================================================================"
  echo "Drops and recreates the database for a given environment."
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <ProjectName> <DatabasePodName> <DatabaseName> <DatabaseUserName>"
  echo
  echo "Where:"
  echo " - <ProjectName> is the project namespace containing the database pod."
  echo " - <DatabasePodName> is the name of the database pod."
  echo " - <DatabaseName> is the name of the database."
  echo " - <DatabaseUserName> is the name of the database user."
  echo
  echo "Examples:"
  echo "${0} devex-von-dev postgresql TheOrgBook_Database TheOrgBook_User"
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
else
  PROJECT_NAME=${1}
fi

if [ -z "${2}" ]; then
  usage
else
  DATABASE_POD_NAME=${2}
fi

if [ -z "${3}" ]; then
  usage
else
  DATABASE_NAME=${3}
fi

if [ -z "${4}" ]; then
  usage
else
  DATABASE_USER_NAME=${4}
fi

echo "============================================================================="
echo "Switching to project ${PROJECT_NAME} ..."
echo "-----------------------------------------------------------------------------"
oc project ${PROJECT_NAME}
echo "============================================================================"
echo

echo "============================================================================="
echo "Recreating database ..."
echo "-----------------------------------------------------------------------------"
${SCRIPT_DIR}/runInContainer.sh \
${DATABASE_POD_NAME} \
"psql -c 'DROP DATABASE \"${DATABASE_NAME}\";'"

${SCRIPT_DIR}/runInContainer.sh \
${DATABASE_POD_NAME} \
"psql -c 'CREATE DATABASE \"${DATABASE_NAME}\";'"

${SCRIPT_DIR}/runInContainer.sh \
${DATABASE_POD_NAME} \
"psql -c 'GRANT ALL ON DATABASE \"${DATABASE_NAME}\" TO \"${DATABASE_USER_NAME}\";'"
echo "============================================================================"
echo

echo "============================================================================="
echo "Listing databases ..."
echo "-----------------------------------------------------------------------------"
${SCRIPT_DIR}/runInContainer.sh \
${DATABASE_POD_NAME} \
'psql -c "\l"'
echo "============================================================================"
echo

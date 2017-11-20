#!/bin/bash
SCRIPT_DIR=$(dirname $0)

# ===================================================================================================
# Funtions
# ---------------------------------------------------------------------------------------------------
usage (){
  echo "========================================================================================"
  echo "Updates the permissions (policy bindings) on an OpenShift project set."
  echo
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <role> <user> <project_namespace>"
  echo
  echo "Where:"
  echo " - <role> is the role to grant to the user; edit, admin, etc."
  echo " - <user> is GitHub userId of the user who will be granted the permissions."
  echo " - <project_namespace> the root namespace for the project set."
  echo
  echo "Examples:"
  echo "${0} edit mrDeveloper devex-von"
  echo "========================================================================================"
  exit 1
}

exitOnError (){
  rtnCd=$?
  if [ ${rtnCd} -ne 0 ]; then
	echo "An error has occurred.!  Please check the previous output message(s) for details."
    exit ${rtnCd}
  fi
}

assignRole (){
  role=$1
  user=$2
  project=$3
  
  echo "Assigning role [${role}], to user [${user}], in project [${project}] ..."
  oc policy add-role-to-user ${role} ${user} -n ${project}

  echo
  echo "Resulting policy bindings for project; [$project] ..."
  oc describe policyBindings --namespace=${project}

  echo
  echo
}

projectExists (){
  project=$1
  rtnVal=$(oc projects | grep ${project})
  if [ -z "$rtnVal" ]; then
    # Project does not exist ..."
	return 1
  else
    # Project exists ..."
	return 0
  fi
}
# ===================================================================================================

# ===================================================================================================
# Setup
# ---------------------------------------------------------------------------------------------------
if [ -z "${1}" ]; then
  usage  
elif [ -z "${2}" ]; then
  usage  
elif [ -z "${3}" ]; then
  usage
elif [ ! -z "${4}" ]; then
  usage  
else
  ROLE=$1
  USERNAME=$2
  PROJECT_NAMESPACE=$3
fi

if [ -z "$TOOLS_PROJECT_NAME" ]; then
	TOOLS_PROJECT_NAME="tools"
fi

if [ -z "$DEV_PROJECT_NAME" ]; then
	DEV_PROJECT_NAME="dev"
fi

if [ -z "$TEST_PROJECT_NAME" ]; then
	TEST_PROJECT_NAME="test"
fi

if [ -z "$PROD_PROJECT_NAME" ]; then
	PROD_PROJECT_NAME="prod"
fi
# ---------------------------------------------------------------------------------------------------
TOOLS_PROJECT="${PROJECT_NAMESPACE}-${TOOLS_PROJECT_NAME}"
DEV_PROJECT="${PROJECT_NAMESPACE}-${DEV_PROJECT_NAME}"
TEST_PROJECT="${PROJECT_NAMESPACE}-${TEST_PROJECT_NAME}"
PROD_PROJECT="${PROJECT_NAMESPACE}-${PROD_PROJECT_NAME}"
# ===================================================================================================

if projectExists ${TOOLS_PROJECT}; then
  assignRole ${ROLE} ${USERNAME} ${TOOLS_PROJECT}
fi
 
if projectExists ${DEV_PROJECT}; then
  assignRole ${ROLE} ${USERNAME} ${DEV_PROJECT}
fi

if projectExists ${TEST_PROJECT}; then
  assignRole ${ROLE} ${USERNAME} ${TEST_PROJECT}
fi

if projectExists ${PROD_PROJECT}; then
  assignRole ${ROLE} ${USERNAME} ${PROD_PROJECT}
fi

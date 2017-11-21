#!/bin/bash

usage() { #Usage function
  cat <<-EOF
  Tool to initialize a set of BC Government standard OpenShift projects.

  Usage: ${0} [ -h -x ]

  OPTIONS:
  ========
    -h prints the usage for the script
    -x run the script in debug mode to see what's happening

    Update settings.sh and settings.local.sh files to set defaults

EOF
exit
}

# Set project and local environment variables
if [ -f settings.sh ]; then
  . settings.sh
fi

# Script-specific variables to be set

# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts xh FLAG; do
  case $FLAG in
    x ) DEBUG=${YES} ;;
    h ) usage ;;
    \?) #unrecognized option - show help
      echo -e \\n"Invalid script option"\\n
      usage
      ;;
  esac
done

# Shift the parameters in case there any more to be used
shift $((OPTIND-1))
# echo Remaining arguments: $@

if [ "${DEBUG}" = "${YES}" ]; then
  set -x
fi

# ===================================================================================

# Iterate through Dev, Test and Prod projects granting permissions, etc.
for project in ${PROJECT_NAMESPACE}-${DEV} ${PROJECT_NAMESPACE}-${TEST} ${PROJECT_NAMESPACE}-${PROD}; do
	echo -e \\n"Granting project ${project} image puller permissions from ${TOOLS}"
	oc policy add-role-to-user \
	system:image-puller \
	system:serviceaccount:${project}:default \
	-n ${TOOLS}

	echo -e \\n"Granting ${JENKINS_SERVICE_ACCOUNT_ROLE} role to Jenkins Service Account in ${project}"
  oc policy add-role-to-user ${JENKINS_SERVICE_ACCOUNT_ROLE} ${JENKINS_SERVICE_ACCOUNT_NAME} -n ${project}

	echo -e \\n"Creating GLUSTER endpoints and services in ${project} "
	oc create -f ${GLUSTER_ENDPOINT_CONFIG} -n ${project}
	oc create -f ${GLUSTER_SVC_CONFIG} -n ${project}
done

echo -e \\n"Creating GLUSTER endpoints and services in ${TOOLS} "\\n
oc create -f ${GLUSTER_ENDPOINT_CONFIG} -n ${TOOLS}
oc create -f ${GLUSTER_SVC_CONFIG} -n ${TOOLS}

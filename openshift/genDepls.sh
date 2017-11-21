#!/bin/bash

usage() {
  cat <<-EOF
  Tool to process OpenShift deployment config templates using local and project settings

  Usage: ./genDepls.sh [ -h -e <Environment> -c <component> -k -u -x ]

  OPTIONS:
  ========
    -h prints the usage for the script
    -e <Environment> the environment (dev/test/prod) into which you are deploying (default: ${DEPLOYMENT_ENV_NAME})
    -c <component> to generate parameters for templates of a specific component
    -k keep the json produced by processing the template
    -u update OpenShift deployment configs instead of creating the configs
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
COMP="no"
RUN_SCRIPT="no"

# Process the command line arguments
# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts c:e:ukxh FLAG; do
  case $FLAG in
    c ) export COMP=$OPTARG ;;
    e ) export DEPLOYMENT_ENV_NAME=$OPTARG ;;
    u ) export OC_ACTION=replace ;;
    k ) export KEEPJSON=${YES} ;;
    x ) export DEBUG=${YES} ;;
    h ) usage ;;
    \? ) #unrecognized option - show help
      echo -e \\n"Invalid script option: -${OPTARG}"\\n
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

# ==============================================================================

for component in "${components[@]}"; do

  if [ ! "${COMP}" = "no" ] && [ ! "${COMP}" = ${component} ]; then
    # Only process named component if -c option specified
    continue
  fi

  echo -e \\n"Deploying component ${component} to the ${DEPLOYMENT_ENV_NAME} environment..."\\n
	pushd ../${component}/openshift >/dev/nul
	${LOCAL_DIR}/compDeployments.sh
	popd >/dev/nul
  cat <<-EOF

Use the OpenShift Console to monitor the deployment in the ${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME} project.
Pause here until the component deploys, and then hit a key to continue the script.

If a deploy hangs take these steps:
 - cancel the instance of the deployment
 - edit the Deployment Config Resources and remove any values
 - click the Deploy button to restart the deploy

EOF
  read -n1 -s -r -p "Press a key to continue..." key
  echo -e \\n
done

# ==============================================================================
# Post Build processing

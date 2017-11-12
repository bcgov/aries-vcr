#!/bin/bash

# git bash hack on windows - deals with pathname conversions from dos to unix-style
export MSYS_NO_PATHCONV=1

PROJECT_NAMESPACE="devex-von"
DEPLOYMENT_ENV_NAME="dev"
BUILD_ENV_NAME="tools"
FIX_ROUTES="no"
LOAD_DATA_SERVER="no"
RUN_SCRIPT="no"
# The components to be deployed in order
declare -a components=("tob-db" "tob-api" "tob-solr" "tob-web")
# The routes to be fixed in order
declare -a routes=("angular-on-nginx" "django" "solr" "schema-spy")

#Usage function
function USAGE {
  echo -e "Usage: $0 [ -h -g -f -r -p <ProjectNameSpace> -d <DeploymentEnv> -t <ToolEnv> -l <server>]"
	echo -e Where:
	echo -e "-h prints the usage for the script"
  echo -e "-g run the script - go. Must be specified for the script to be executed"
  echo -e "-f fix the routes specified in the json for local usage (default: leave routes as is)"
  echo -e "-l <server> load data into the specified server after deployment is complete (default: No Loading, Options: local/dev/test/prod/URL)"
	echo -e "-p <ProjectNameSpace> sets the prefix OpenShift Project namespace (default: ${PROJECT_NAMESPACE})"
	echo -e "-d <DeploymentEnv> sets the environment into which you are deploying (default: ${DEPLOYMENT_ENV_NAME})"
	echo -e "-t <ToolEnv> sets the tools environment from which you are deploying (default: ${BUILD_ENV_NAME})"
  exit 1
}

# Process the command line arguments
# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts p:d:t:fl:gh FLAG; do
  case $FLAG in
    p)
      PROJECT_NAMESPACE=$OPTARG
      ;;
    d)
      DEPLOYMENT_ENV_NAME=$OPTARG
      ;;
    t)
      BUILD_ENV_NAME=$OPTARG
      ;;
    f)
      FIX_ROUTES="yes"
      ;;
    l)
      LOAD_DATA_SERVER=$OPTARG
      ;;
    g)
      RUN_SCRIPT="yes"
      ;;
    h)
      USAGE
      ;;
    \?) #unrecognized option - show help
      echo -e \\n"Invalid script option: -${OPTARG}"\\n
      USAGE
      ;;
  esac
done

# Shift the parameters in case there any more to be used
shift $((OPTIND-1))
echo Remaining arguments: $@

if [ "${RUN_SCRIPT}" != "yes" ]; then
  echo -e \\n"The -g parameter was not specified - not running script. Exiting..."
  USAGE
fi

# ==============================================================================

for component in "${components[@]}"; do
  echo -e \\n"Deploying component ${component}..."\\n
	pushd ../${component}/openshift
	./generateDeployments.sh ${PROJECT_NAMESPACE} ${DEPLOYMENT_ENV_NAME} ${BUILD_ENV_NAME}
	popd
  echo -e "Use the OpenShift Console to monitor the deployment in the ${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME} project."
  echo -e "Pause here until the component deploys, and then hit a key to continue the script."
  echo -e \\n
  echo -e "If a deploy hangs take these steps:"
  echo -e " - cancel the instance of the deployment"
  echo -e " - edit the Deployment Config Resources and remove any values"
  echo -e " - click the Deploy button to restart the deploy"
  echo -e \\n
  read -n1 -s -r -p "Press a key to continue..." key
  echo -e \\n
done

# ==============================================================================
# Post Build processing

# Fix routes
if [ "${FIX_ROUTES}" = "yes" ]; then
  echo -e "Fixing routes for this environment"
  oc project ${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME}
  for route in "${routes[@]}"; do
    oc delete route ${route}
    oc create route edge --service=${route}
    sleep 5
  done
fi

# Load Test Data
if [ "${LOAD_DATA_SERVER}" != "yes" ]; then
  echo -e "Loading data into TheOrgBook Server: ${LOAD_DATA_SERVER}"
  pushd ../APISpec/TestData
  ./load-all.sh ${LOAD_DATA_SERVER}
  popd
fi

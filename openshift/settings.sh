# bash script to be sourced to set environment variables for OpenShift scripts

# git bash hack on windows - deals with pathname conversions from dos to unix-style
MSYS_NO_PATHCONV=1

# Project Variables
# export YES=Yes
# export NO=No
# export DEBUG=${NO}
export LOCAL_DIR=../../openshift
export OC_ACTION=create
#export KEEPJSON=${NO}
export DEV=dev
export TEST=test
export PROD=prod

export PROJECT_NAMESPACE="devex-von"
export GIT_URI="https://github.com/bcgov/TheOrgBook.git"
export TOOLS=${PROJECT_NAMESPACE}-tools
export DEPLOYMENT_ENV_NAME="${DEV}"
export BUILD_ENV_NAME="tools"
export GIT_REF="master"
export LOAD_DATA_SERVER="dev"
export TEMPLATE_DIR=templates
export PIPELINE_JSON=https://raw.githubusercontent.com/BCDevOps/openshift-tools/master/provisioning/pipeline/resources/pipeline-build.json
export COMPONENT_JENKINSFILE=../Jenkinsfile
export PIPELINEPARAM=pipeline.param

# Jenkins account settings for initialization
export JENKINS_ACCOUNT_NAME="jenkins"
export JENKINS_SERVICE_ACCOUNT_NAME="system:serviceaccount:${TOOLS}:${JENKINS_ACCOUNT_NAME}"
export JENKINS_SERVICE_ACCOUNT_ROLE="edit"

# Gluster settings for initialization
export GLUSTER_ENDPOINT_CONFIG=https://raw.githubusercontent.com/BCDevOps/openshift-tools/master/resources/glusterfs-cluster-app-endpoints.yml
export GLUSTER_SVC_CONFIG=https://raw.githubusercontent.com/BCDevOps/openshift-tools/master/resources/glusterfs-cluster-app-service.yml
export GLUSTER_SVC_NAME=glusterfs-cluster-app

# The project components
declare -a components=("tob-db" "tob-solr" "tob-api" "tob-web")

# The builds to be triggered after buildconfigs created (not auto-triggered)
declare -a builds=("nginx-runtime" "angular-builder")

# The images to be tagged after build
declare -a images=("angular-on-nginx" "django" "solr" "schema-spy")

# The routes for the project
declare -a routes=("angular-on-nginx" "django" "solr" "schema-spy")

# Load in any overrides
if [ -f ./settings.local.sh ]; then
  echo -e \\n"Overriding default settings, loading local project settings from $PWD/settings.local.sh ..."\\n
  . ./settings.local.sh
fi

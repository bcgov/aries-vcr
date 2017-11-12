#!/bin/bash

# git bash hack on windows - deals with pathname conversions from dos to unix-style
export MSYS_NO_PATHCONV=1

#Script variables to be set
PROJECT_NAME="devex-von-tools"
GIT_REF="master"
GIT_URI="https://github.com/bcgov/TheOrgBook.git"
RUN_SCRIPT="no"
# The components to be built
declare -a components=("tob-api" "tob-solr" "tob-web")
# The builds to be triggered after buildconfigs created (not auto-triggered)
declare -a builds=("nginx-runtime" "angular-builder")
# The images to be tagged after build
declare -a images=("angular-on-nginx" "django" "solr" "schema-spy")

#Usage function
function USAGE {
  echo -e "Usage: $0 [ -h -g -p <ToolsProject> -r <gitRepo> -b <gitBranch> ]"
	echo -e Where:
	echo -e "-h prints the usage for the script"
  echo -e "-g run the script - go. Must be specified for the script to be executed"
	echo -e "-p <ToolsProject> sets the OpenShift Project you are using for tools (default: ${PROJECT_NAME})"
	echo -e "-r <gitRepo> sets the source code repo to use (default: ${GIT_URI})"
	echo -e "-b <gitBranch> sets the branch in the git repo (default: ${GIT_REF})"
  exit 1
}

# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts p:r:b:gh FLAG; do
  case $FLAG in
    p)
      PROJECT_NAME=$OPTARG
      ;;
    r)
      GIT_URI=$OPTARG
      ;;
    b)
      GIT_REF=$OPTARG
      ;;
    g)
      RUN_SCRIPT="yes"
      ;;
    h)
      USAGE
      ;;
    \?) #unrecognized option - show help
      echo -e \\n"Invalid script option"\\n
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

# Run the initialize script to set Permissions
./initializeProjects.sh devex-von

for component in "${components[@]}"; do
	pushd ../${component}/openshift
	./generateBuilds.sh ${PROJECT_NAME} ${GIT_REF} ${GIT_URI}
	popd
done

# ==============================================================================
# Post Build processing
echo -e "Builds created. Use the OpenShift Console to monitor the progress in the ${PROJECT_NAME} project."
echo -e "Pause here until the started builds complete, and then hit a key to continue the script."
read -n1 -s -r -p "Press a key to continue..." key
echo -e \\n

oc project ${PROJECT_NAME}
for build in "${builds[@]}"; do
  echo -e \\n"Building component ${build}..."\\n
  oc start-build ${build}
  echo -e "Use the OpenShift Console to monitor the build in the ${PROJECT_NAME} project."
  echo -e "Pause here until the build completes, and then hit a key to continue the script."
  echo -e \\n
  echo -e "If a build hangs take these steps:"
  echo -e " - cancel the instance of the build"
  echo -e " - edit the Build Config YAML and remove the resources section"
  echo -e " - click the Start Build button to restart the build"
  echo -e \\n
  read -n1 -s -r -p "Press a key to continue..." key
  echo -e \\n
done

for image in "${images[@]}"; do
  echo -e \\n"Tagging image ${image} for dev environment deployment..."\\n
  oc tag ${image}:latest ${image}:dev
done

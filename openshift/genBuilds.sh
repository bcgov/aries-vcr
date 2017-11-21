#!/bin/bash

usage() {
  cat <<-EOF
  Tool to create or update OpenShift build config templates and Jenkins pipeline deployment using
  local and project settings. Also triggers builds that aren't auto-triggered ("builds"
  variable in settings.sh) and tags the images ("images" variable in settings.sh).

  Usage: $0 [ -h -u -c <comp> -k -x ]

  OPTIONS:
  ========
    -h prints the usage for the script
    -c <component> to generate parameters for templates of a specific component
    -u update OpenShift build configs vs. creating the configs
    -k keep the json produced by processing the template
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
COMP=${NO}

# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts c:ukxh FLAG; do
  case $FLAG in
    c ) export COMP=$OPTARG ;;
    u ) export OC_ACTION=replace ;;
    k ) export KEEPJSON=${YES} ;;
    x ) export DEBUG=${YES} ;;
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

# ==============================================================================

for component in "${components[@]}"; do

  echo -e \\n"Deploying component ${component} to the ${DEPLOYMENT_ENV_NAME} environment..."\\n

  if [ ! "${COMP}" = "${NO}" ] && [ ! "${COMP}" = ${component} ]; then
    # Only process named component if -c option specified
    continue
  fi

	pushd ../${component}/openshift >/dev/null
  ${LOCAL_DIR}/compBuilds.sh
	popd >/dev/null
done

if [ ! "${COMP}" = "${NO}" ]; then
  # If only processing one component, don't do the post build steps
  exit
fi

# ==============================================================================
# Post Build processing
echo -e \\n"Builds created. Use the OpenShift Console to monitor the progress in the ${PROJECT_NAME} project."
echo -e \\n"Pause here until the started builds complete, and then hit a key to continue the script."
read -n1 -s -r -p "Press a key to continue..." key
echo -e \\n

oc project ${TOOLS}
for build in "${builds[@]}"; do
  echo -e \\n"Manually triggering build of ${build}..."\\n
  oc start-build ${build}
  echo -e \\n"Use the OpenShift Console to monitor the build in the ${PROJECT_NAME} project."
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

echo -e \\n"Tagging images for dev environment deployment..."\\n
for image in "${images[@]}"; do
  oc tag ${image}:latest ${image}:dev
done

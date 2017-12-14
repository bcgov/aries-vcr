#!/bin/bash

usage() { #Usage function
  cat <<-EOF
  Delete and recreate with defaults the routes in an environment.

  Usage: ${0} [ -h -e <environment> -x ]

  OPTIONS:
  ========
    -h prints the usage for the script
    -e <environment> recreate routes in the named environment (dev/test/prod) (default: ${DEPLOYMENT_ENV_NAME})
    -x run the script in debug mode to see what's happening

    Update settings.sh and settings.local.sh files to set defaults

EOF
exit
}

# Set project and local environment variables
if [ -f settings.sh ]; then
  echo -e \\n"Loading default project settings from settings.sh ..."\\n
  . settings.sh
fi

# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts e:xh FLAG; do
  case $FLAG in
    e ) DEPLOYMENT_ENV_NAME=$OPTARG ;;
    x ) export DEBUG=1 ;;
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

if [ ! -z "${DEBUG}" ]; then
  set -x
fi

# ===================================================================================
# Fix routes
echo -e "Update routes to default in the project: ${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME}"
oc project ${PROJECT_NAMESPACE}-${DEPLOYMENT_ENV_NAME}
for route in "${routes[@]}"; do
  oc delete route ${route}
  oc create route edge --service=${route}
  sleep 3 # Allow the creation of the route to complete
done

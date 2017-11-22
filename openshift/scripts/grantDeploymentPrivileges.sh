#!/bin/bash

SCRIPT_DIR=$(dirname $0)

# ==============================================================================
usage() {
cat <<EOF

================================================================================
Grants deployment configurations access to the images in the tools project.
--------------------------------------------------------------------------------
Usage: 
  ${0} [ -h -x ] -p <TARGET_PROJECT> -t <TOOLS_PROJECT>

Options:
  -h prints the usage for the script
  -x run the script in debug mode to see what's happening
================================================================================
EOF
exit 1
}

if [ -f ${SCRIPT_DIR}/commonFunctions.inc ]; then
  . ${SCRIPT_DIR}/commonFunctions.inc
fi

# ------------------------------------------------------------------------------
# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts p:t:xh FLAG; do
  case $FLAG in
    p ) TARGET_PROJECT_NAME=$OPTARG ;;
    t ) TOOLS_PROJECT_NAME=$OPTARG ;;
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

if [ -z "${TARGET_PROJECT_NAME}" ] || [ -z "${TOOLS_PROJECT_NAME}" ]; then
  echo -e \\n"Missing parameters!"  
  usage
fi
# ==============================================================================

echo "Granting deployment configuration access from ${TARGET_PROJECT_NAME}, to ${TOOLS_PROJECT_NAME} ..."
assignRole \
  system:image-puller \
  system:serviceaccount:${TARGET_PROJECT_NAME}:default \
  ${TOOLS_PROJECT_NAME}
echo

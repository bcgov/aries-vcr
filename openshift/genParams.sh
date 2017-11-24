#!/bin/bash

SCRIPT_DIR=$(dirname $0)
SCRIPTS_DIR="${SCRIPT_DIR}/scripts"

# =================================================================================================================
# Usage:
# -----------------------------------------------------------------------------------------------------------------
usage() {
  cat <<-EOF
  A wrapper tool to generate OpenShift template and pipeline parameters files for the application.

  Usage: ./genParams.sh [ -h -f -l -x -c <component> ]

  OPTIONS:
  ========
    -h prints the usage for the script
    -f force generation even if the file already exists
    -l generate local params files - with all parameters commented out
    -c <component> to generate parameters for templates of a specific component
    -x run the script in debug mode to see what's happening

    Update settings.sh and settings.local.sh files to set defaults

EOF
exit
}

# -----------------------------------------------------------------------------------------------------------------
# Initialization:
# -----------------------------------------------------------------------------------------------------------------
while getopts c:flxh FLAG; do
  case $FLAG in
    h ) usage ;;
    \?) #unrecognized option - show help
      echo -e \\n"Invalid script option"\\n
      usage
      ;;
  esac
done
# =================================================================================================================

# For this to work the two scripts must accept the same set of options.
${SCRIPT_DIR}/genTemplateParams.sh $@
${SCRIPT_DIR}/genPipelineParams.sh $@

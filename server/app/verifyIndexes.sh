#!/bin/bash
SCRIPT_DIR=$(dirname $0)
MANAGE_CMD=${SCRIPT_DIR}/runManageCmd.sh

# ==============================================================================================================================
usage() {
  cat <<-EOF
  ========================================================================================
  Verify indexes exist for all crenentials.
  ----------------------------------------------------------------------------------------
  Usage:
    ${0} [ -h ]
  
  Options:
    -h Prints the usage for the script
  ========================================================================================
EOF
exit
}

while getopts h FLAG; do
  case $FLAG in
    h ) usage
      ;;
    \? ) #unrecognized option - show help
      echo -e \\n"Invalid script option: -${OPTARG}"\\n
      usage
      ;;
  esac
done

shift $((OPTIND-1))
# ==============================================================================================================================

${MANAGE_CMD} verify_credential_index
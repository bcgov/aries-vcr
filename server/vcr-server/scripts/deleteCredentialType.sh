#!/bin/bash
SCRIPT_DIR=$(dirname $0)
MANAGE_CMD=${SCRIPT_DIR}/runManageCmd.sh

# ==============================================================================================================================
usage() {
  cat <<-EOF

========================================================================================
Delete all OrgBook data for the specified Credential Type.
----------------------------------------------------------------------------------------
Usage:
  ${0} <credential_type_id> [ -h ]

Options:
  <credential_type_id> is the ID of the Credential Type to delete, e.g. 123
  -h Prints the usage for the script
========================================================================================
EOF
}

while getopts h FLAG; do
  case $FLAG in
    h ) usage
        exit
      ;;
  esac
done

shift $((OPTIND-1))
# ==============================================================================================================================

_credential_type_id=${1}
if [ -z "${_credential_type_id}" ]; then
  usage
  echo -e \\n"deleteCredentialType; Missing required <credential_type_id> parameter."\\n
  exit 1
fi

${MANAGE_CMD} delete_credential_type "$@"

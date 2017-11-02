#!/bin/bash
SCRIPT_DIR=$(dirname $0)
MANAGE_CMD=${SCRIPT_DIR}/runManageCmd.sh
OUTPUT_DIR=${SCRIPT_DIR}/../tob-solr/cores/the_org_book/conf

# ==============================================================================================================================
usage () {
  echo "========================================================================================"
  echo "Builds the schema and configuration file(s) for Solr, based on your project's"
  echo "Haystack/Solr configuration."
  echo "The configuration files will be output to, ${OUTPUT_DIR}."
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0}"
  echo "========================================================================================"
  exit 1
}

if [ ! -z "${1}" ]; then
  usage
fi
# ==============================================================================================================================

${MANAGE_CMD} build_solr_schema -c ${OUTPUT_DIR}
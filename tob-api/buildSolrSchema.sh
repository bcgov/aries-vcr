#!/bin/bash
SCRIPT_DIR=$(dirname $0)
MANAGE_CMD=${SCRIPT_DIR}/runManageCmd.sh
OUTPUT_DIR=${SCRIPT_DIR}/../tob-solr/cores/the_org_book/conf

# Fake the Haystack configuration script into hooking up the solr backend
# Required for the Solr configuration to be updated.
export SOLR_SERVICE_NAME=django
export SOLR_CORE_NAME=the_org_book
export DJANGO_SERVICE_HOST=localhost
export DJANGO_SERVICE_PORT=80

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
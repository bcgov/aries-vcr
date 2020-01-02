#!/bin/bash
SCRIPT_DIR=$(dirname $0)
MANAGE_CMD=${SCRIPT_DIR}/runManageCmd.sh
SOLR_BATCH_SIZE=${SOLR_BATCH_SIZE:-500}

# ==============================================================================================================================
usage() {
  cat <<-EOF
  ========================================================================================
  Updates the Haystack indexes for the project.
  ----------------------------------------------------------------------------------------
  Usage:
    ${0} [ -h -x -u <SolrUrl/> -b <BatchSize/> -s <StartDate/> ]
  
  Options:
    -h Prints the usage for the script
    -x Enable debug output
    -u The URL to the Solr search engine instance 
    -b The batch size to use when performing the indexing.  Defaults to ${SOLR_BATCH_SIZE}.
    -s The date of where to start the update process.
  
  Example:
    ${0} -u http://localhost:8983/solr/the_org_book
    ${0} -b 200 -s 2019-06-01T00:00:00 
  ========================================================================================
EOF
exit

}
while getopts s:b:xh FLAG; do
  case $FLAG in
    u ) export SOLR_URL=$OPTARG
      ;;
    b ) SOLR_BATCH_SIZE=$OPTARG
      ;;
    s ) START_DATE=$OPTARG
      ;;
    x ) export DEBUG=1
      ;;
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

if [ -z "${START_DATE}" ]; then
  ${MANAGE_CMD} update_index -b ${SOLR_BATCH_SIZE}
else
  ${MANAGE_CMD} update_index -b ${SOLR_BATCH_SIZE} -s ${START_DATE}
fi


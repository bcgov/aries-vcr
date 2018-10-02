#!/bin/bash
SCRIPT_DIR=$(dirname $0)
SOLR_SERVICE_NAME=${SOLR_SERVICE_NAME:-solr}
SOLR_URL=${SOLR_URL:-http://$SOLR_SERVICE_NAME:8983/solr/the_org_book}

# ==============================================================================================================================
usage() {
  cat <<-EOF
  ========================================================================================
  Builds the Suggester on the Solr server which is used for auto-complete functionality.
  ----------------------------------------------------------------------------------------
  Usage:
    ${0} [ -h -x -s <SolrUrl/> ]
  
  Options:
    -h Prints the usage for the script
    -x Enable debug output
    -s The URL to the Solr search engine instance. Defaults to ${SOLR_URL}.
  
  Example:
    ${0} -s http://localhost:8983/solr/the_org_book
  ========================================================================================
EOF
exit

}
while getopts s:b:xh FLAG; do
  case $FLAG in
    s ) SOLR_URL=$OPTARG
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

curl "${SOLR_URL}/suggest/?q=&suggest.build=true&wt=json"
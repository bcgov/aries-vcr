#!/bin/bash
export MSYS_NO_PATHCONV=1

# ==============================================================================
# Script for loading test data into the TheOrgBook database
#
# * Requires curl
# ------------------------------------------------------------------------------
# Usage on Windows (using Git Bash):
#  ./load-all.sh <environment>
#
# Example:
#  ./load-all.sh dev
# ------------------------------------------------------------------------------
exitOnError () {
  rtnCd=$?
  if [ ${rtnCd} -ne 0 ]; then
	echo "An error has occurred while loading data!  Please check the previous output message(s) for details."
    exit ${rtnCd}
  fi
}

if [ -z "${1}" ]; then
  echo Incorrect syntax
  echo USAGE "${0}" "<environment>"
  echo Example: "${0}" dev
  echo "Where <environment> is one of local, dev, test, prod or a full URL"
  exit
fi

# ==============================================================================================
# The order of the loading is important - need to add independent files before dependent ones
# ==============================================================================================

echo Data for TheOrgBook is now loaded via the loading of claims. Details to come...

./loadClaims.py "${1}"
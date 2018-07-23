#!/bin/bash
# ===========================================================================================================
usage () {
  echo "========================================================================================"
  echo "Generates data from a Claims Excel File"
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <excelFile>"
  echo
  echo "Example: ${0} TOBV2DataFakeRestaurentsBusinessLicences.xlsx"
  echo
  echo "========================================================================================"
  exit 1
}

# ===========================================================================================================

if [ -z "${1}" ]; then
  usage
fi

# Prerequisites for running this script:
# Python 2 is installed - assumes it is /usr/bin/python2 - see top if xls2json.py file

echo Calling xls2json script on file: $1
./xls2json.py $1

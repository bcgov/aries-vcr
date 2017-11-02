#!/bin/bash
SCRIPT_DIR=$(dirname $0)
PYTHON_EXE=${SCRIPT_DIR}/env/Scripts/python

# ==============================================================================================================================
usage () {
  echo "========================================================================================"
  echo "Runs Python commands using the project's virtual python installation."
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <command>"
  echo
  echo "Where:"
  echo " - <command> is the Python command you wish to run."
  echo
  echo "Examples:"
  echo "${0} --version"
  echo "========================================================================================"
  exit 1
}

if [ -z "${1}" ]; then
  usage
fi
# ==============================================================================================================================

${PYTHON_EXE} ${@}
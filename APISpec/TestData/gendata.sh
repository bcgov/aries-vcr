#!/bin/bash
SCRIPT_DIR=$(dirname $0)
ENV_DIR=../../tob-api/env

# Prerequisites for running this script:
# 1. Python 3 is installed - assumes it is called python
# 2. Or an installed python environment

if [[ ! -d ${ENV_DIR} ]]; then
  PYTHONCMD=python
else
  PYTHONCMD=${ENV_DIR}/Scripts/python
fi

for file in in/*.csv
do
  echo Processing CSV file: $file
	$PYTHONCMD csv2json.py $file yes
done

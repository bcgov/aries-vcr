#!/bin/bash

# Prerequisites for running this script:
# 1.  Python 2.7 is installed - assumes it is called python

PYTHONCMD=python

for file in in/*.csv
do
  echo Processing CSV file: $file
	$PYTHONCMD csv2json.py $file yes
done

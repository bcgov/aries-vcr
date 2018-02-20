#!/bin/bash
EXCEL_FILE=TOBClaims.xlsm

# Prerequisites for running this script:
# Python 3 is installed - assumes it is /usr/bin/python3 - see top if xls2json.py file

echo Calling xls2json script on file: $EXCEL_FILE
./xls2json.py --csv Claims.csv $EXCEL_FILE

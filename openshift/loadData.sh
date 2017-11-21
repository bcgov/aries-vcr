#!/bin/bash

# Set project and local environment variables
if [ -f settings.sh ]; then
  . settings.sh
fi

#Usage function
function USAGE {
  echo -e "Usage: $0 [ -h -g -e <DataLoadEnv> ]"
	echo -e Where:
	echo -e "-h prints the usage for the script"
  echo -e "-g run the script - go. Must be specified for the script to be executed"
  echo -e "-e <server> load data into the specified server (default: ${LOAD_DATA_SERVER}, Options: local/dev/test/prod/URL)"
  exit 1
}

# Process the command line arguments
# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts e:gh FLAG; do
  case $FLAG in
    e ) LOAD_DATA_SERVER=$OPTARG ;;
    g ) RUN_SCRIPT="yes" ;;
    h ) USAGE ;;
    \? ) #unrecognized option - show help
      echo -e \\n"Invalid script option: -${OPTARG}"\\n
      USAGE
      ;;
  esac
done

# Shift the parameters in case there any more to be used
shift $((OPTIND-1))
# echo Remaining arguments: $@

if [ "${RUN_SCRIPT}" != "yes" ]; then
  echo -e \\n"The -g parameter was not specified - not running script. Exiting..."\\n
  USAGE
fi

# Load Test Data
echo -e "Loading data into TheOrgBook Server: ${LOAD_DATA_SERVER}"
pushd ../APISpec/TestData
./load-all.sh ${LOAD_DATA_SERVER}
popd

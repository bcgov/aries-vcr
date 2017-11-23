#!/bin/bash

usage() { #Usage function
  cat <<-EOF
  Tool to generate OpenShift template parameters files in expected places (project or local) for BC Gov applications.

  Usage: ./genParams.sh [ -h -f -l -x -c <component> ]

  OPTIONS:
  ========
    -h prints the usage for the script
    -f force generation even if the file already exists
    -l generate local params files - with all parameters commented out
    -c <component> to generate parameters for templates of a specific component
    -x run the script in debug mode to see what's happening

    Update settings.sh and settings.local.sh files to set defaults

EOF
exit
}

# Set project and local environment variables
if [ -f settings.sh ]; then
  . settings.sh
fi

# Uncomment if you want to check what command line args were entered
# echo "flags = $*"
while getopts c:flxh FLAG; do
  case $FLAG in
    c ) COMP=$OPTARG ;;
    f ) FORCE=1 ;;
    l ) LOCAL=1 ;;
    x ) export DEBUG=1 ;;
    h ) usage ;;
    \?) #unrecognized option - show help
      echo -e \\n"Invalid script option"\\n
      usage
      ;;
  esac
done

# Shift the parameters in case there any more to be used
shift $((OPTIND-1))
# echo Remaining arguments: $@

# Debug mode
if [ ! -z "${DEBUG}" ]; then
  set -x
fi

# What types of files to generate - regular+dev/test/prod or local
if [ ! -z "${LOCAL}" ]; then
  PARM_TYPES="l"
else
  PARM_TYPES="r d t p"
fi

# ==============================================================================
for component in "${components[@]}"; do
  if [ ! -z "${COMP}" ] && [ ! "${COMP}" = ${component} ]; then
    # Only process named component if -c option specified
    continue
  fi

    pushd ../${component}/openshift >/dev/null

  # Get list of JSON files - could be in multiple directories below
  pushd ${TEMPLATE_DIR} >/dev/null
  JSONFILES=$(find . -name "*json" | sed "s/.json//" | xargs | sed "s/\.\///g")
  # echo -e "JSON Files: ${JSONFILES}"
  popd >/dev/null

  # Iterate through each file and generate the params files
  for file in ${JSONFILES}; do
    TEMPLATE=${TEMPLATE_DIR}/${file}.json

    # Is this a deploy template? Don't generate dev/test/prod for Build templates
    ISDEPLOY=$( grep -l DeploymentConfig ${TEMPLATE} )

    for type in ${PARM_TYPES}; do
      unset SKIP
      case ${type} in
        r ) # Regular file
          OUTPUT=${OUTPUTPREFIX}$( basename ${file}.param )
          COMMENTFILTER=cat
          ;;
        d ) # Dev File
          OUTPUT=${OUTPUTPREFIX}$( basename ${file}.${DEV}.param )
          COMMENTFILTER="sed s/^/#/"
          if [ "${ISDEPLOY}" = "" ]; then SKIP=1; fi
          ;;
        t ) # Test File
          OUTPUT=${OUTPUTPREFIX}$( basename ${file}.${TEST}.param )
          COMMENTFILTER="sed s/^/#/"
          if [ "${ISDEPLOY}" = "" ]; then SKIP=1; fi
          ;;
        p ) # Prod
          OUTPUT=${OUTPUTPREFIX}$( basename ${file}.${PROD}.param )
          COMMENTFILTER="sed s/^/#/"
          if [ "${ISDEPLOY}" = "" ]; then SKIP=1; fi
          ;;
        l ) # Local Files
          OUTPUT=${LOCAL_DIR}/$( basename ${file}.local.param )
          COMMENTFILTER="sed s/^/#/"
          ;;
      esac

      # Don't create environment param files for Build Templates
      if [ ! -z "${SKIP}" ]; then
        continue
      fi

      if [ ! -f "${OUTPUT}" ] || [ ! -z "${FORCE}" ]; then
        echo -e "Generating parameters for template: ${file}.json to ${OUTPUT}"
        echo -e "# OpenShift template parameters for:" >${OUTPUT}
        echo -e "# Component: ${component}" >>${OUTPUT}
        echo -e "# JSON Template File: ${file}.json" >>${OUTPUT}
        echo -e "#=======================================" >>${OUTPUT}
        # Fancy sed handling below to convert parameters output to param file format
        #   Delete the first line of the oc process output
        #   Put "XXXX" in front of the parameter default value
        #   Remove all whitespace before the XXXX and change XXXX to =
        #   Use COMMENTFILTER to add (or not) a "#" in front of each line; comments it out the line
        oc process --parameters --filename=${TEMPLATE} | \
          sed "1d" | \
          sed 's/\([^ ]*$\)/XXXX\1/' |  \
          sed 's/\s.*XXXX/=/' | \
          ${COMMENTFILTER} | sed 's/^#/# /' \
          >>${OUTPUT}
      else
        echo -e "Skipping parameter generation for template: ${file}.json to ${OUTPUT}"
        FORCENOTE=1
      fi
    done
  done

  # Generating pipeline parameter file
  if [ -f "${COMPONENT_JENKINSFILE}" ]; then
    OUTPUT=${PIPELINEPARAM}
    if [ ! -f "${OUTPUT}" ] || [ ! -z "${FORCE}" ]; then
      echo -e "Generating parameters for Jenkins Pipeline to ${OUTPUT}"
      
      echo -e "# OpenShift Jenkins template parameters for:" > ${OUTPUT}
      echo -e "# Component: ${component}" >> ${OUTPUT}
      echo -e "# JSON Template File: ${PIPELINE_JSON}" >> ${OUTPUT}
      echo -e "#=======================================" >> ${OUTPUT}
      oc process --parameters --filename=${PIPELINE_JSON} | \
        sed "1d" | \
        sed 's/\([^ ]*$\)/XXXX\1/' |  \
        sed 's/\s.*XXXX/=/' | \
        sed 's/^#/# /' \
        >> ${OUTPUT}
    fi
  fi
  popd >/dev/null
done

if [ ! -z "${FORCENOTE}" ]; then
  echo -e \\n"One or more files to be generated already exist and were not overwritten"
  echo -e "Use the -f option to force the overwriting of existing files"
fi

if [ ! -z "${LOCAL}" ]; then
  echo -e "Local files generated with parmeters commented out. Edit the files to uncomment and set needed parameters"
fi

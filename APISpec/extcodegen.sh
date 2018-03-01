#!/bin/bash

# Comment out the tech stack for which you are generating
# NOTE: if you want to generate both the front and backend, you might want to
# setup two runs of the generator - the backend and frontend, with different tech stacks
TARGET_STACK="fuse"
TARGET_STACK="javascript-closure-angular"
TARGET_STACK="aspnetmvc"
TARGET_STACK="django"

# Adjust these lines to set the names and locations of the code generator jars
executable="swagger-codegen-extension-1.0.1-jar-with-dependencies.jar;swagger-codegen-cli.jar"

# Set the code elements to be generate
GEN_OPTIONS="-DapiTests=true -DmodelTests=true"

# Set the output path
OUTPUT="gen/"

# Set the Config File
CONFIG_FILE="swagger-codegen-config.json"

# Set the swagger file
SWAGGER_FILE="TOBswagger.yaml"

# Command line processing
# See Usage below.
# Use -gt 1 to consume two arguments per pass in the loop (e.g. each
# argument has a corresponding value to go with it).
# Use -gt 0 to consume one or more arguments per pass in the loop (e.g.
# some arguments don't have a corresponding value to go with it such
# as in the --default example).
# note: if this is set to -gt 0 the /etc/hosts part is not recognized ( may be a bug )

usage="0"
while [ $# -gt 0 ] && [ "$usage" == "0" ]
do
key="$1"

case $key in
    -h|--help)
    usage="1"
    ;;
    -f|--file)
    SWAGGER_FILE="$2"
    shift # past argument
    ;;
    -o|--output)
    OUTPUT="$2"
    shift # past argument
    ;;
    -c|--config)
    CONFIG_FILE="$2"
    shift # past argument
    ;;
    -s|--stack)
    TARGET_STACK="$2"
    shift # past argument
    ;;
    -j|--jars)
    executable="$2"
    shift # past argument
    ;;
    *)
    usage="1"        # unknown option
    ;;
esac
shift # past argument or value
done

echo Usage is $usage
if [ "$usage" == "1" ]; then
  echo Extended Swagger Code Generator
  echo USAGE $0 [args]
  echo where no args uses the defaults set in this file and runs the code generation
  echo Args:
  echo '  -h|--help - print usage information'
  echo '  -f|--file <swagger file> - specify the swagger file to use'
  echo '  -o|--output <output folder> - specify the output folder to output the generated code'
  echo '  -c|--config <config json> - specify the swagger code generator json file to use'
  echo '  -s|--stack <django|fuse|aspnetmvc> - specify the stack to generate - could also be one of the many supported by Swagger'
  echo Current options:
  echo ..Target Stack: $TARGET_STACK
  echo ..........JARs: $executable
  echo .Output Folder: $OUTPUT
  echo ...Config File: $CONFIG_FILE
  echo ..Swagger File: $SWAGGER_FILE
  exit 1
fi

# TODO - Convert this to bash
# Process required command line options to override defaults
# IF "%1."=="." GOTO :USAGE
# SWAGGER_FILE=%1
# SHIFT

# Process optional arguments
# :loop
# IF NOT "%1"=="" (
#     IF "%1"=="-output" (
#         SET OUTPUT=%2
#         SHIFT
#     )
#     IF "%1"=="-config" (
#         SET CONFIG_FILE=%2
#         SHIFT
#     )
#     IF "%1"=="-stack" (
#         SET TARGET_STACK=%2
#         SHIFT
#     )
#     IF "%1"=="-jars" (
#         SET executable=%2
#         SHIFT
#     )
#     SHIFT
#     GOTO :loop
# )
#
# :RUN

# Check if the jars list was set on the command line
# if NOT "%executable%."=="." GOTO :GO

# Adjust the JARs based on the tech stack chosen - possibly from the command line
# Adjust these lines to set the names and locations of the code generator jars
# executable=swagger-codegen-extension-1.0.1-jar-with-dependencies.jar;swagger-codegen-cli.jar

# :GO
JAVA_OPTS="-Dfile.encoding=UTF-8 $GEN_OPTIONS -Xmx1024M"
args="generate -i $SWAGGER_FILE -l $TARGET_STACK -c $CONFIG_FILE -o $OUTPUT"

echo Command to be run: java $JAVA_OPTS -cp $executable io.swagger.codegen.SwaggerCodegen $args
java $JAVA_OPTS -cp $executable io.swagger.codegen.SwaggerCodegen $args

# GOTO End1

# :USAGE
# echo ERROR: Arguments required for this script
# echo USAGE: %0 ^<Swagger file^> ^[-stack ^<aspnetmvc^|django^|fuse^|javascript-closure-angular^> -config ^<config file^> -output ^<output folder^> -jars ^<jar^;jar^>]
# echo The jars must support the tech stack selected.
# echo Default arguments:
# echo ^ ^ Target Stack: %TARGET_STACK%
# echo ^ ^ Code to Generate: %GEN_OPTIONS%
# echo ^ ^ Config File: %CONFIG_FILE%
# echo ^ ^ Output Location: %OUTPUT%

# :End1

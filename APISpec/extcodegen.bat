@ECHO OFF

REM Comment out the tech stack for which you are generating
REM NOTE: if you want to generate both the front and backend, you might want to
REM setup two runs of the generator - the backend and frontend, with different tech stacks
set TARGET_STACK=fuse
set TARGET_STACK=javascript-closure-angular
set TARGET_STACK=aspnetmvc
set TARGET_STACK=django

REM Set the code elements to be generate
set GEN_OPTIONS=-DapiTests=true -DmodelTests=true

REM Set the output path
set OUTPUT=gen/

REM Set the Config File
set CONFIG_FILE=swagger-codegen-config.json

REM Set the swagger file
set SWAGGER_FILE=TOBswagger.yaml

REM Uncomment this if no command line processing is needed - e.g. defaults are all set
GOTO :RUN


REM Process required command line options to override defaults
IF "%1."=="." GOTO :USAGE
set SWAGGER_FILE=%1
SHIFT

REM Process optional arguments
:loop
IF NOT "%1"=="" (
    IF "%1"=="-output" (
        SET OUTPUT=%2
        SHIFT
    )
    IF "%1"=="-config" (
        SET CONFIG_FILE=%2
        SHIFT
    )
    IF "%1"=="-stack" (
        SET TARGET_STACK=%2
        SHIFT
    )
    IF "%1"=="-jars" (
        SET executable=%2
        SHIFT
    )
    SHIFT
    GOTO :loop
)

:RUN

REM Check if the jars list was set on the command line
if NOT "%executable%."=="." GOTO :GO

REM Adjust the JARs based on the tech stack chosen - possibly from the command line
REM Adjust these lines to set the names and locations of the code generator jars
set executable=swagger-codegen-extension-1.0.1-jar-with-dependencies.jar;swagger-codegen-cli.jar

:GO
set JAVA_OPTS=-Dfile.encoding=UTF-8 %GEN_OPTIONS%
set JAVA_OPTS=%JAVA_OPTS% -Xmx1024M
set args=generate -i %SWAGGER_FILE% -l %TARGET_STACK% -c %CONFIG_FILE% -o %OUTPUT%

echo Command to be run^:
echo ^ ^ java %JAVA_OPTS% -cp %executable% io.swagger.codegen.SwaggerCodegen %args%
java %JAVA_OPTS% -cp %executable% io.swagger.codegen.SwaggerCodegen %args%

GOTO End1

:USAGE
ECHO ERROR: Arguments required for this script
ECHO USAGE: %0 ^<Swagger file^> ^[-stack ^<aspnetmvc^|django^|fuse^|javascript-closure-angular^> -config ^<config file^> -output ^<output folder^> -jars ^<jar^;jar^>]
ECHO The jars must support the tech stack selected.
ECHO Default arguments:
ECHO ^ ^ Target Stack: %TARGET_STACK%
ECHO ^ ^ Code to Generate: %GEN_OPTIONS%
ECHO ^ ^ Config File: %CONFIG_FILE%
ECHO ^ ^ Output Location: %OUTPUT%

:End1

@ECHO OFF

SET dev=http://tfrs-mem-tfrs-dev.pathfinder.gov.bc.ca
SET test=http://tfrs-mem-tfrs-test.pathfinder.gov.bc.ca
SET prod=http://tfrs-mem-tfrs-prod.pathfinder.gov.bc.ca

IF %3.==. GOTO USAGE

SET server=%3
IF %3==dev SET server=%dev%
IF %3==test SET server=%test%
IF %3==prod SET server=%prod%

REM Add call to authenticate when authentication is added to the application if the "cookie" file doesn't exist
REM If NOT Exist "cookie" {
REM   curl -c cookie %Tserver%/api/authentication/dev/token?userId=scurran
REM }

curl -b cookie -v -H "Content-Type: application/json" -X POST --data-binary "@%1" %server%/%2

GOTO End1

:USAGE
ECHO Incorrect syntax
ECHO USAGE load.bat ^<JSON filename^> ^<endpoint^> ^<server URL^>
ECHO Example: load.bat permissions/permissions_all.json permissions/bulk dev
ECHO Where server URL is one of dev, test, prod or a full URL
ECHO Note: Do not put a / before the endpoint
ECHO The dev server is: %dev%
ECHO The test server is: %test%
ECHO The prod server is: %prod%

:End1

#$/bin/bash

dev=http://devex-von-dev-django.pathfinder.gov.bc.ca
test=http://devex-von-test-django.pathfinder.gov.bc.ca
prod=http://devex-von-prod-django.pathfinder.gov.bc.ca

if [ -z "${3}" ]; then
  echo Incorrect syntax
  echo USAGE ${0} "<JSON filename> <endpoint> <server URL>"
  echo Example: ${0} permissions/permissions_all.json permissions/bulk dev
  echo "Where <server URL> is one of dev, test or a full URL"
  echo Note: Do not put a / before the endpoint
  echo The dev server is: ${dev}
  echo The test server is: ${test}
  echo The prod server is: ${prod}
  exit
fi

server=${3}
if [ ${3} = "dev" ]; then
   server=$dev
elif [ ${3} = "test" ]; then
   server=$test
elif [ ${3} = "prod" ]; then
   server=$prod
fi

# if [ ! -f cookie ]; then
#   curl -c cookie ${server}/api/authentication/dev/token?userId=scurran
# fi

echo Loading File ${1} using endpoint ${server}/${2}
if [ -z "${4}" ]; then
	curl -v -H "Content-Type: application/json" -X POST --data-binary "@${1}" ${server}/${2}
elif [ ${4} = "--test" ]; then
	echo "curl -b cookie -v -H \"Content-Type: application/json\" -X POST --data-binary \"@${1}\" ${server}/${2}"
fi
echo
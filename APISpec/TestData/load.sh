#$/bin/bash

dev=https://devex-von-dev-django.pathfinder.gov.bc.ca
test=https://devex-von-test-django.pathfinder.gov.bc.ca
prod=https://devex-von-prod-django.pathfinder.gov.bc.ca

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

echo "----------------------------------------------------------------------------------------------------------------------------"
echo "Posting data to endpoint ..."
echo
echo "Source File: ${1}"
echo "Endpoint: ${server}/${2}"
echo
if [ -z "${4}" ]; then
	curl --silent --show-error --fail -w "\n\nResponse Code: %{http_code}\t" -H "Content-Type: application/json" -X POST --data-binary "@${1}" ${server}/${2}
	rtnCd=$?
	if [ ${rtnCd} = 0 ]; then
		echo
	fi
elif [ ${4} = "--test" ]; then
	echo "Resolved curl call:"
	echo "curl --silent --show-error --fail -H "Content-Type: application/json" -X POST --data-binary "@${1}" ${server}/${2}"
fi
echo "----------------------------------------------------------------------------------------------------------------------------"
echo

if [ ${rtnCd} -ne 0 ]; then
	exit ${rtnCd}
fi
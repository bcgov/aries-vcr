# Special Deployment parameters needed for DB Deployment
POSTGRESQL_USER=USER$( cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 4 | head -n 1 )
POSTGRESQL_PASSWORD=$( cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9_' | fold -w 16 | head -n 1 )
POSTGRESQL_USER=$(echo -n "${POSTGRESQL_USER}"|base64)
POSTGRESQL_PASSWORD=$(echo -n "${POSTGRESQL_PASSWORD}"|base64)
SPECIALDEPLOYPARM="-p POSTGRESQL_USER=${POSTGRESQL_USER} -p POSTGRESQL_PASSWORD=${POSTGRESQL_PASSWORD}"

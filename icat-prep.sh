
mkdir starter-kits
mkdir starter-kits/credential-registry
mkdir starter-kits/credential-registry/server

rm .gitignore
rm .gitattributes

shopt -s extglob
mv !(starter-kits|icat-prep.sh) starter-kits/credential-registry/server/

mkdir credential-registry
mkdir credential-registry/server
mkdir credential-registry/server/django-icat-api
mkdir credential-registry/server/python-indy-api

mv starter-kits/credential-registry/server/tob-api/api_v2 credential-registry/server/django-icat-api
mv starter-kits/credential-registry/server/tob-api/api_indy credential-registry/server/python-indy-api

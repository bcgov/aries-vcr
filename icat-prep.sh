
mkdir starter-kits
mkdir starter-kits/credential-registry
mkdir starter-kits/credential-registry/client
mkdir starter-kits/credential-registry/server

rm .gitignore
rm .gitattributes

shopt -s extglob
mv !(starter-kits|icat-prep.sh) starter-kits/credential-registry/server/

mkdir credential-registry
mkdir credential-registry/client
mkdir credential-registry/server
mkdir credential-registry/server/django-icat-api
mkdir credential-registry/server/python-indy-api

mv starter-kits/credential-registry/server/tob-api/api_v2 credential-registry/server/django-icat-api/
mv starter-kits/credential-registry/server/tob-api/api_indy credential-registry/server/python-indy-api/
#mv starter-kits/credential-registry/server/tob-web starter-kits/credential-registry/client/

rm starter-kits/credential-registry/server/Deploy*
rm -rf starter-kits/credential-registry/server/openshift
rm -rf starter-kits/credential-registry/server/sonar-runner
rm -rf starter-kits/credential-registry/server/tob-backup

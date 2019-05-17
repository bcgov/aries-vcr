# This script re-orgs the OrgBook repo in preparation for merge into indy-catalyst
#
# Before running this script:
# - create a new branch (e.g. merge_test) so a to not screw up master
#
# Run this script from TheOrgBook root
#
# After running this script:
# - commit into github (into the new branch)
#
# In the indy-catalyst repo:
# - start on a new branch (for safety)
# - git remote add orgbook https://github.com/bcgov/TheOrgBook.git
# - git fetch orgbook
# - git merge orgbook/merge-test --allow-unrelated-histories (or whatever you called your branch)
#
# To build the starter kit (server):
# - cd to credential-registry/server
# - ./icat-py-build.sh # builds packages for tob-api
# - cd to starter-kits/credential-registry/server/docker
# - update manage script (see README files in the above credential-registry/server sub-directories)
# - ./manage build
# - ./manage start
#
# Note it requires a von network to be already running

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
mv starter-kits/credential-registry/server/tob-web credential-registry/client/
mkdir starter-kits/credential-registry/client/tob-web/
mkdir starter-kits/credential-registry/client/tob-web/themes/
cp -r credential-registry/client/tob-web/src/themes/ starter-kits/credential-registry/client/tob-web/themes/
mv starter-kits/credential-registry/server/docker starter-kits/credential-registry/

rm starter-kits/credential-registry/server/Deploy*
rm starter-kits/credential-registry/server/SonarQube-*
rm starter-kits/credential-registry/server/Zap-*
rm -rf starter-kits/credential-registry/server/openshift
rm -rf starter-kits/credential-registry/server/sonar-runner
rm -rf starter-kits/credential-registry/server/tob-backup
rm -rf starter-kits/credential-registry/client/tob-web/themes/default
rm -rf credential-registry/client/tob-web/src/themes/bcgov
rm -rf credential-registry/client/tob-web/src/themes/ongov

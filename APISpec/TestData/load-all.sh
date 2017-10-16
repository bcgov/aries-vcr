#$/bin/bash

# ==============================================================================
# Script for loading test data into the TheOrgBook database
#
# * Requires curl
# ------------------------------------------------------------------------------
# Usage on Windows (using Git Bash):
#  MSYS_NO_PATHCONV=1 ./load-all.sh <server URL>
#
# Example:
#  MSYS_NO_PATHCONV=1 ./load-all.sh dev
# ------------------------------------------------------------------------------
exitOnError () {
  rtnCd=$?
  if [ ${rtnCd} -ne 0 ]; then
	echo "An error has occurred while loading data!  Please check the previous output message(s) for details."
    exit ${rtnCd}
  fi
}
# ------------------------------------------------------------------------------
API_PREFIX=api/v1
BULK_PATH=bulk
# ==============================================================================

if [ -z "${1}" ]; then
  echo Incorrect syntax
  echo USAGE ${0} "<server URL>"
  echo Example: ${0} dev
  echo "Where <server URL> is one of dev, test, prod or a full URL"
  exit
fi

# Before starting, remove the cookie authentication file.
# The ./load.sh script will add it if needed for the remainder of the calls
if [ -e cookie ]; then
  rm cookie
fi

# ==============================================================================================
# The order of the loading is important - need to add independent files before dependent ones
# ==============================================================================================

# Users, Roles, and Permissions ...
./load.sh ./users/users_user.json ${API_PREFIX}/users/${BULK_PATH} "$@"
exitOnError
./load.sh ./roles/roles_Role.json ${API_PREFIX}/roles/${BULK_PATH} "$@"
exitOnError
./load.sh ./permissions/permissions_Perms.json ${API_PREFIX}/permissions/${BULK_PATH} "$@"
exitOnError
./load.sh ./userRole/userRole_userRole.json ${API_PREFIX}/userroles/${BULK_PATH} "$@"
exitOnError
./load.sh ./rolepermission/rolepermission_RP.json ${API_PREFIX}/rolepermissions/${BULK_PATH} "$@"
exitOnError

# Everything else ...
./load.sh ./InactiveClaimReason/InactiveClaimReason_DEAC.json ${API_PREFIX}/inactiveclaimreasons/${BULK_PATH} "$@"
exitOnError
./load.sh ./Jurisdiction/Jurisdiction_JUR.json ${API_PREFIX}/jurisdictions/${BULK_PATH} "$@"
exitOnError
./load.sh ./VOType/VOType_VOType.json ${API_PREFIX}/voorgtypes/${BULK_PATH} "$@"
exitOnError
./load.sh ./VOLocationType/VOLocationType_VLT.json ${API_PREFIX}/volocationtypes/${BULK_PATH} "$@"
exitOnError
./load.sh ./IssuerService/IssuerService_ISVC.json ${API_PREFIX}/issuerservices/${BULK_PATH} "$@"
exitOnError
./load.sh ./VOClaimType/VOClaimType_CT.json ${API_PREFIX}/voclaimtypes/${BULK_PATH} "$@"
exitOnError
./load.sh ./VerifiedOrg/VerifiedOrg_VO.json ${API_PREFIX}/verifiedorgs/${BULK_PATH} "$@"
exitOnError
./load.sh ./VOClaim/VOClaim_VOC.json ${API_PREFIX}/voclaims/${BULK_PATH} "$@"
exitOnError
./load.sh ./VODoingBusinessAs/VODoingBusinessAs_VODBA.json ${API_PREFIX}/vodoingbusinessas/${BULK_PATH} "$@"
exitOnError
./load.sh ./VOLocation/VOLocation_VOL.json ${API_PREFIX}/volocations/${BULK_PATH} "$@"
exitOnError

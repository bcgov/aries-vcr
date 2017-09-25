#$/bin/bash

if [ -z "$1" ]; then
  echo Incorrect syntax
  echo USAGE $0 "<server URL>"
  echo Example: $0 dev
  echo "Where <server URL> is one of dev, test, prod or a full URL"
  exit
fi

# Before starting, remove the cookie authentication file.
# The ./load.sh script will add it if needed for the remainder of the calls
if [ -e cookie ]; then
  rm cookie
fi

# The order of the loading is important - need to add independent files before dependent ones
./load.sh CreditTradeStatus/CreditTradeStatus_TCS.json api/credittradestatuses/bulk $1
./load.sh CreditTradeType/CreditTradeType_CTType.json api/credittradetypes/bulk $1
./load.sh FuelSupplierActionsType/FuelSupplierActionsType_FSActionType.json api/fuelsupplieractionstypes/bulk $1
./load.sh FuelSupplierStatus/FuelSupplierStatus_FSStatus.json api/fuelsupplierstatuses/bulk $1
./load.sh FuelSupplierType/FuelSupplierType_FSType.json api/fuelsuppliertypes/bulk $1
./load.sh NotificationType/NotificationType_NotType.json api/notificationtypes/bulk $1
./load.sh OpportunityStatus/OpportunityStatus_OppStatus.json api/opportunitystatuses/bulk $1

./load.sh permissions/permissions_Perms.json api/permissions/bulk $1
./load.sh roles/roles_Role.json api/roles/bulk $1
./load.sh rolepermission/rolepermission_RP.json api/rolepermissions/bulk $1

./load.sh FuelSupplier/FuelSupplier_FS.json api/fuelsuppliers/bulk $1
# ./load.sh FuelSupplierCCData/FuelSupplierCCData_FSCCD.json api/fuelsupplierccdata/bulk $1
./load.sh users/users_user.json api/users/bulk $1
./load.sh userRole/userRole_userRole.json api/userroles/bulk $1
./load.sh FuelSupplierContactRole/FuelSupplierContactRole_FSContactRole.json api/fuelsuppliercontactroles/bulk $1
./load.sh FuelSupplierContact/FuelSupplierContact_FSContact.json api/fuelsuppliercontacts/bulk $1

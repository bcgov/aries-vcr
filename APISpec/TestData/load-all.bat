@ECHO OFF

IF %1.==. GOTO USAGE

rem need to load FuelSupplierContacts before FuleSuppliers.

call load.bat CreditTradeStatus/CreditTradeStatus_TCS.json api/credittradestatuses/bulk %1%
call load.bat CreditTradeType/CreditTradeType_CTType.json api/credittradetypes/bulk %1%
call load.bat FuelSupplierActionsType/FuelSupplierActionsType_FSActionType.json api/fuelsupplieractionstypes/bulk %1%
call load.bat FuelSupplierStatus/FuelSupplierStatus_FSStatus.json api/fuelsupplierstatuses/bulk %1%
call load.bat FuelSupplierType/FuelSupplierType_FSType.json api/fuelsuppliertypes/bulk %1%
call load.bat NotificationType/NotificationType_NotType.json api/notificationtypes/bulk %1%
call load.bat OpportunityStatus/OpportunityStatus_OppStatus.json api/opportunitystatuses/bulk %1%

call load.bat permissions/permissions_Perms.json api/permissions/bulk %1%
call load.bat roles/roles_Role.json api/roles/bulk %1%
call load.bat rolepermission/rolepermission_RP.json api/rolepermissions/bulk %1%

call load.bat FuelSupplier/FuelSupplier_FS.json api/fuelsuppliers/bulk %1%
REM call load.bat FuelSupplierCCData/FuelSupplierCCData_FSCCD.json api/fuelsupplierccdata/bulk %1%
call load.bat users/users_user.json api/users/bulk %1%
call load.bat userRole/userRole_userRole.json api/userroles/bulk %1%
call load.bat FuelSupplierContactRole/FuelSupplierContactRole_FSContactRole.json api/fuelsuppliercontactroles/bulk %1%
call load.bat FuelSupplierContact/FuelSupplierContact_FSContact.json api/fuelsuppliercontacts/bulk %1%

GOTO End1

:USAGE
ECHO Incorrect syntax
ECHO USAGE load-all.bat ^<server URL^>
ECHO Example: load-all.bat dev
ECHO Where server URL is one of dev, test, prod or a full URL

:End1

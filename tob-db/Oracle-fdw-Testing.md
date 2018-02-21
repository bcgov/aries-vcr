Configuration:

POSTGRESQL_USER
POSTGRESQL_PASSWORD
* The credentials for the PostgreSQL database that will be hosting the foriegn schema.
* These should be differant than the credentials used for the Oracle database.

POSTGRESQL_DATABASE
* The name of the PostgreSQL database that will be hosting the foriegn schema.

FDW_NAME
* The name to give to the foreign server entry registered in the PostgreSQL database.  The name is a bit misleading.

FDW_FOREIGN_SCHEMA
* The name of the schema in the Oracle database.  The value is case sensitive.

FDW_FOREIGN_SERVER
* The connection string for the Oracle database, in the form <host>:<port>/<listener service name>.    The value is case sensitive.
* <host> can be the DNS or IP address for the server.
* <listener service name> comes from the listener service configuration on the Oracle server.
For example, the configuration from `inter:/dsk01/app/tnsadmin/listener.ora`, where the service name is `CUAT.bcgov`.
```
(SID_DESC =
  (GLOBAL_DBNAME = CUAT.bcgov)
  (ORACLE_HOME = /dsk01/app/oracle/product/rdbms/11.2.0.4)
  (SID_NAME = CUAT)
)
```

FDW_USER
FDW_PASS
* The credentials for the Oracle database.  These will be used by the oracle-fdw components to connect to the Oracle database.

FDW_SCHEMA
* The name of the schema in the PostgreSQL database.  The objects from the Oracle side will be created within this schema.


Testing:

Login to the database with your main database user account;
```
psql -UUSER_Rc4u -d BC_REGISTRIES
```

Ensure the expected schemas exist
```
BC_REGISTRIES=> \dn
     List of schemas
     Name      |  Owner
---------------+----------
 bc_registries | postgres
 public        | postgres
(2 rows)
```

Ensure the specified foreign server exists
```
BC_REGISTRIES=> \des
                 List of foreign servers
         Name          |  Owner   | Foreign-data wrapper
-----------------------+----------+----------------------
 bc_registries_wrapper | postgres | oracle_fdw
(1 row)
```

Ensure the roles are setup as expected.  Your main database user should have access to the `fdw_reader` role.
```
BC_REGISTRIES=> \du
                                     List of roles
 Role name  |                         Attributes                         |  Member of
------------+------------------------------------------------------------+--------------
 USER_Rc4u  |                                                            | {fdw_reader}
 fdw_reader | Cannot login                                               | {}
 postgres   | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

```

Ensure you can list the table details in the defined schema;
```
BC_REGISTRIES=> \det bc_registries.
                         List of foreign tables
    Schema     |             Table              |        Server
---------------+--------------------------------+-----------------------
 bc_registries | accession_number_vw            | bc_registries_wrapper
 bc_registries | account                        | bc_registries_wrapper
 bc_registries | address                        | bc_registries_wrapper
 bc_registries | address_civic_no_suffix_type   | bc_registries_wrapper
 bc_registries | address_format_country_vw      | bc_registries_wrapper
 bc_registries | address_format_type            | bc_registries_wrapper
 bc_registries | address_format_vw              | bc_registries_wrapper
 bc_registries | address_installation_type      | bc_registries_wrapper

...
```

Ensure you can list the table details in the defined schema;
```
BC_REGISTRIES=> \d bc_registries.
          Foreign table "bc_registries.accession_number_vw"
       Column       |         Type          | Modifiers | FDW Options
--------------------+-----------------------+-----------+-------------
 corp_num           | character varying(10) | not null  |
 orig_accession_num | character varying(10) |           |
 source             | character varying(11) |           |
 format_244_1       | character varying(2)  |           |
 format_244_2       | character varying(4)  |           |
 format_244_3       | character varying(4)  |           |
 display_244        | character varying(12) |           |
Server: bc_registries_wrapper
FDW Options: (schema 'COLIN_MGR_UAT', "table" 'ACCESSION_NUMBER_VW')

               Foreign table "bc_registries.account"
    Column     |          Type          | Modifiers | FDW Options
---------------+------------------------+-----------+--------------
 realm_id      | character varying(255) | not null  | (key 'true')
 user_id       | character varying(255) | not null  | (key 'true')
 password      | character varying(20)  |           |
 password_hint | character varying(100) |           |
 realm         | character varying(255) |           |
Server: bc_registries_wrapper
FDW Options: (schema 'COLIN_MGR_UAT', "table" 'ACCOUNT')

                   Foreign table "bc_registries.address"
         Column         |          Type          | Modifiers | FDW Options
------------------------+------------------------+-----------+--------------
 addr_id                | numeric                | not null  | (key 'true')
 province               | character(2)           |           |
 country_typ_cd         | character(2)           |           |
 postal_cd              | character varying(15)  |           |
 addr_line_1            | character varying(50)  |           |
 addr_line_2            | character varying(50)  |           |
 addr_line_3            | character varying(50)  |           |
 city                   | character varying(40)  |           |
 address_format_type    | character varying(10)  |           |
 address_desc           | character varying(300) |           |
 address_desc_short     | character varying(300) |           |
 delivery_instructions  | character varying(80)  |           |
 unit_no                | character varying(6)   |           |
 unit_type              | character varying(10)  |           |
 civic_no               | character varying(6)   |           |
 civic_no_suffix        | character varying(10)  |           |
 street_name            | character varying(30)  |           |
 street_type            | character varying(10)  |           |
 street_direction       | character varying(10)  |           |
 lock_box_no            | character varying(5)   |           |
 installation_type      | character varying(10)  |           |
 installation_name      | character varying(30)  |           |
 installation_qualifier | character varying(15)  |           |
 route_service_type     | character varying(10)  |           |
 route_service_no       | character varying(4)   |           |
 province_state_name    | character varying(30)  |           |
Server: bc_registries_wrapper
FDW Options: (schema 'COLIN_MGR_UAT', "table" 'ADDRESS')

...
```

Ensure you can select from a table;
```
BC_REGISTRIES=> select count(*) from bc_registries.xpro_type;
 count
-------
     3
(1 row)
```

Ensure you can get data from the table;
```
BC_REGISTRIES=> select * from bc_registries.xpro_type;
 xpro_typ_cd | short_desc  |         full_desc
-------------+-------------+---------------------------
 COR         | CORPORATION | Extraprovincial Company
 LLC         | LIM LIAB    | Limited Liability Company
 FED         | FEDERAL     | Federal Company
(3 rows)
```




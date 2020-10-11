# Fixing a Corrupt Wallet Index

## Scenario

Wallet backup fails with the following error:

```
Backing up 'wallet-indy-cat:5432/agent_indy_cat_wallet' to '/backups/weekly/2020-10-11/wallet-indy-cat-agent_indy_cat_wallet_2020-10-11_01-05-27.sql.gz.in_progress' ...
pg_dump: Dumping the contents of table "items" failed: PQgetResult() failed.
pg_dump: Error message from server: ERROR:  missing chunk number 0 for toast value 33780607 in pg_toast_10826517
pg_dump: The command was: COPY public.items (id, type, name, value, key) TO stdout;
removed '/backups/weekly/2020-10-11/wallet-indy-cat-agent_indy_cat_wallet_2020-10-11_01-05-27.sql.gz.in_progress'
[!!ERROR!!] - Failed to backup wallet-indy-cat:5432/agent_indy_cat_wallet.
```

## Listing `pg_toast` relationships

```
sh-4.2$ psql -d agent_indy_cat_wallet
psql (10.12)
Type "help" for help.

agent_indy_cat_wallet=# select r.relname, t.relname from pg_class r inner join pg_class t on t.reltoastrelid = r.oid;
      relname      |         relname         
-------------------+-------------------------
 pg_toast_10826525 | metadata
 pg_toast_10826533 | tags_encrypted
 pg_toast_2619     | pg_statistic
 pg_toast_10826517 | items
 pg_toast_10826539 | tags_plaintext
 pg_toast_1255     | pg_proc
 pg_toast_2604     | pg_attrdef
 pg_toast_2606     | pg_constraint
 pg_toast_3381     | pg_statistic_ext
 pg_toast_2618     | pg_rewrite
 pg_toast_2620     | pg_trigger
 pg_toast_2609     | pg_description
 pg_toast_2964     | pg_db_role_setting
 pg_toast_2396     | pg_shdescription
 pg_toast_3596     | pg_seclabel
 pg_toast_3592     | pg_shseclabel
 pg_toast_12150    | sql_parts
 pg_toast_12140    | sql_languages
 pg_toast_12130    | sql_features
 pg_toast_12135    | sql_implementation_info
 pg_toast_12145    | sql_packages
 pg_toast_12155    | sql_sizing
 pg_toast_12160    | sql_sizing_profiles
(23 rows)
```

*References:*
- *[Postgres pg_toast in autovacuum - which table?](https://stackoverflow.com/questions/18456026/postgres-pg-toast-in-autovacuum-which-table)*

## Getting Record Counts for the Affected Database

Using the `./manage` script from [bcgov/orgbook-configurations](https://github.com/bcgov/orgbook-configurations) you can get a list of the tables and record counts for a given database.

For example (Wallet record counts from `test`):
```
$ ./manage -p bc -e test getrecordcounts wallet agent_indy_cat_wallet

Loading settings ...
Loading settings from /c/orgbook-configurations/openshift/settings.sh ...
Loading settings from /c/orgbook-configurations/openshift/settings.bc.sh ...

 table_schema |   table_name   | count_rows | disk_usage
--------------+----------------+------------+------------
 public       | tags_encrypted |  165712916 | 75 GB
 public       | items          |    7172139 | 22 GB
 public       | metadata       |          1 | 48 kB
 public       | tags_plaintext |          0 | 40 kB
(4 rows)
```

## Reindexing the Affected Table

```
REINDEX table pg_toast.pg_toast_10826517;
```

`REINDEX` is a blocking process.  Some operations (read/write) will be blocked while the table is being reindexed.

`REINDEX` of 7,172,139 records (items table from `test` environment for example) takes ~13 minutes to process.

*References:*
- *[pg_dump and ERROR: missing chunk number 0 for toast value](https://dba.stackexchange.com/questions/31008/pg-dump-and-error-missing-chunk-number-0-for-toast-value)*
- *[REINDEX](https://www.postgresql.org/docs/10/sql-reindex.html)*
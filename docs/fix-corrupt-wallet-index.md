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

## Listing `pg_toast` Relationships

For a specific table:
```
select reltoastrelid::regclass from pg_class where relname = 'items';
```
```
sh-4.2$ psql -d agent_indy_cat_wallet
psql (10.12)
Type "help" for help.

agent_indy_cat_wallet=# select reltoastrelid::regclass from pg_class where relname = 'items';
       reltoastrelid        
----------------------------
 pg_toast.pg_toast_10826517
(1 row)
```

All:
```
select r.relname, t.relname from pg_class r inner join pg_class t on t.reltoastrelid = r.oid;
```

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
- *[postgres_recovery.md](https://gist.github.com/supix/80f9a6111dc954cf38ee99b9dedf187a)*

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

## Reindexing the Affected Table and Indexes

```
REINDEX table items;
REINDEX table pg_toast.pg_toast_10826517;
VACUUM analyze items;
```

`REINDEX` is a blocking process.  Some operations (read/write) will be blocked while the table is being reindexed.

`REINDEX` of 7,172,139 records (items table from `test` environment for example) takes ~13 minutes to process.

*References:*
- *[pg_dump and ERROR: missing chunk number 0 for toast value](https://dba.stackexchange.com/questions/31008/pg-dump-and-error-missing-chunk-number-0-for-toast-value)*
- *[REINDEX](https://www.postgresql.org/docs/10/sql-reindex.html)*
- *[postgres_recovery.md](https://gist.github.com/supix/80f9a6111dc954cf38ee99b9dedf187a)*

## When Reindexing Alone is Not Enough

In some cases the data itself may be corrupted, not just the indexes.  In this case you will need to scan the data in order to narrow down and locate the affected records.

The [locateBadRecord](https://github.com/bcgov/orgbook-configurations/blob/master/openshift/manage#L103) function in the `./manage` script from [bcgov/orgbook-configurations](https://github.com/bcgov/orgbook-configurations) automates this process.

Start with a full scan of the table.  In the following example the `items` table is being scanned beginning to end 5000 records at a time.
```
$ ./manage -p bc -e prod locateBadRecord wallet agent_indy_cat_wallet items 5000

Checking table for bad records:
  - Table: items
  - Database: agent_indy_cat_wallet
  - Pod: wallet-indy-cat
  - Begin: 0
  - End: 5923585
  - Step: 5000

Checking records 10000 to 14999 of 5923585 ...
```

This initial pass will identify corrupted records within a given set of 5000 records and report the offset where the issue was encountered.

```
Corrupted chunk read at offset 5915000.
```

Once you have all of the results from the initial scan you can narrow the range and limit incrementally until you've idenfified the offsets of all of the affected records.

```
$ ./manage -p bc -e prod locateBadRecord wallet agent_indy_cat_wallet items 1000 5915000 5920000

Checking table for bad records:
  - Table: items
  - Database: agent_indy_cat_wallet
  - Pod: wallet-indy-cat
  - Begin: 5915000
  - End: 5920000
  - Step: 1000

Checking records 5917000 to 5917999 of 5923589 ...
Corrupted chunk read at offset 5917000.
```
```
$ ./manage -p bc -e prod locateBadRecord wallet agent_indy_cat_wallet items 100 5917000 5918000

Checking table for bad records:
  - Table: items
  - Database: agent_indy_cat_wallet
  - Pod: wallet-indy-cat
  - Begin: 5917000
  - End: 5918000
  - Step: 100

Checking records 5917200 to 5917299 of 5923591 ...
Corrupted chunk read at offset 5917200.
```
```
$ ./manage -p bc -e prod locateBadRecord wallet agent_indy_cat_wallet items 1 5917200 5917300

Checking table for bad records:
  - Table: items
  - Database: agent_indy_cat_wallet
  - Pod: wallet-indy-cat
  - Begin: 5917200
  - End: 5917300
  - Step: 1

Checking record 5917204 ...
Corrupted chunk read at offset 5917204.
```

Once you have identified the offset of all of the affected records you can use the script to get the `id` of the affected records:

```
$ ./manage -p bc -e prod locateBadRecord wallet agent_indy_cat_wallet items 1 5917204 5917204

Checking table for bad records:
  - Table: items
  - Database: agent_indy_cat_wallet
  - Pod: wallet-indy-cat
  - Begin: 5917204
  - End: 5917204
  - Step: 1

select id from items order by id limit 1 offset 5917204;
    id
----------
 10474003
(1 row)
```

*References:*
- *[postgres_recovery.md](https://gist.github.com/supix/80f9a6111dc954cf38ee99b9dedf187a)*

### I've Identified the Affected Records - Now What?

Now that you've identified the affected records you need to delete them.  You will obviously loose the data contained in the record, but it's basically already gone at this point (it's corrupt).

Before you delete the records you may want to try to identify the record a bit more so you can firstly determine the impact of the data loss, and secondly provide yourself with some additional information that may help you replace the record (from a backup or by replacing the data some other way).  Try performing selects on the individual fields to collect what data you can about the record(s).

Delete the records.  For safety sake you may want to perform this operation one record at a time and confirm the record you are about to delete is corrupt by running a `select *` on the record before you delete it.

Replace or restore the data if you can.  How you do this will likely vary on what was corrupted and when it was corrupted.

Finally, re-index the table and indexes:
```
REINDEX table items;
REINDEX table pg_toast.pg_toast_10826517;
VACUUM analyze items;
```
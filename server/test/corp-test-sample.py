#!/usr/bin/python

#
# This script selects a representative set of companies from the orgbook search database
# to feed into an api test suite (to test the overall output results of a select set of
# api endpoints)
#
# The selected company set represents the bulk of the output data scenarios (although not
# necessarily the full coverage of bc registries business scenarios).
#
# To produce a list of corp nums for each orgbook environment, specify the ORGBOOK_ENV environment
# variable to "dev", "test", "prod", etc (default is "local") and the appropriate csv file will 
# be produced.
#

import os
import psycopg2
import datetime
import json


db = {}
db['host'] = os.environ.get('ORGBOOK_DB_HOST', 'localhost')
db['port'] = os.environ.get('ORGBOOK_DB_PORT', '5432')
db['database'] = os.environ.get('ORGBOOK_DB_DATABASE', 'THE_ORG_BOOK')
db['user'] = os.environ.get('ORGBOOK_DB_USER', 'DB_USER')
db['password'] = os.environ.get('ORGBOOK_DB_PASSWORD', 'DB_PASSWORD')

orgbook_env = os.environ.get('ORGBOOK_ENV', 'local')

sql_path = os.environ.get('SQL_PATH', './')
sql_file = os.environ.get('SQL_FILE', 'corp-test-sample.sql')
corp_num_file = os.environ.get('CORP_NUM_FILE', 'corp-test-sample-corps.csv')


def read_sql_file(path, filename):
    sqls = []
    with open(path + filename, "r") as sql_file:
        for line in sql_file:
            sqls.append(line.strip())
    return sqls


def write_corps_file(sqls, corp_path, corp_num_file):
    # Connect to the PostgreSQL database server
    conn = None
    cur = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**db)

        with open(corp_path + corp_num_file, "w") as corp_file:
            for sql in sqls:
                if sql.startswith("#"):
                    # it is a comment
                    corp_file.write(sql + "\n")
                else:
                    # create a cursor
                    cur = conn.cursor()
                    cur.execute(sql)
                    row = cur.fetchone()
                    corps = []
                    while row is not None:
                        corp_info = ""
                        for attr in row:
                            if 0 < len(corp_info):
                                corp_info = corp_info + ','
                            corp_info = corp_info + '"' + str(attr) + '"'
                        corp_file.write(corp_info + "\n")
                        row = cur.fetchone()

                    cur.close()
                    cur = None

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
            print('Cursor closed.')
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == "__main__":
    # read sqls to execute
    print("Reading sqls from: " + sql_path + sql_file)
    sqls = read_sql_file(sql_path, sql_file)

    # write corp nums to file
    print("Writing corps to: " + sql_path + orgbook_env + "-" + corp_num_file)
    write_corps_file(sqls, sql_path, orgbook_env + "-" + corp_num_file)


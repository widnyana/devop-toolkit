#!/usr/bin/env python
"""
Provide listing of Character Set for each schema and table inside your MySQL Server

(c) 2016 - widnyana.
"""

import json
import click
import pymysql
import pymysql.cursors
from datetime import datetime


QUERY_LISTDB = "SHOW DATABASES;"
QUERY_LISTTABLES = "SHOW TABLES;"
QUERY_CHARSET_SCHEMA = """
    SELECT default_character_set_name FROM information_schema.SCHEMATA 
    WHERE schema_name = %s;
    """
QUERY_CHARSET_TABLE = """
    SELECT CCSA.character_set_name FROM information_schema.`TABLES` T,
        information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA
    WHERE CCSA.collation_name = T.table_collation
    AND T.table_schema = %s
    AND T.table_name = %s;
    """

def _e(string):
    now = datetime.now()
    print "[%s]\t%s" % (now.strftime("%Y-%m-%d %H:%M:%S"), string)


def _connect(u, pw, h, p, **kwargs):
    con = pymysql.connect(
        host=h,
        user=u,
        password=pw,
        port=p,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    return con


def get_databases(con):
    _e("Getting databases ...")
    with con as cursor:
        cursor.execute(QUERY_LISTDB)
        result = cursor.fetchall()

    banned = ['information_schema', 'mysql', 'performance_schema', 'sys']
    result = [r for r in [r.get("Database") for r in result] if r not in banned]
    return result


def get_tables(con, dbname):
    _e("Getting table list on schema: %s ..." % (dbname,))
    keyname = "Tables_in_%s" % (dbname,)
    with con as cursor:
        query = "USE %s;" % (dbname,)
        cursor.execute(query)
        cursor.execute(QUERY_LISTTABLES)
        result = cursor.fetchall()

    result = [r.get(keyname) for r in result]
    return result


def _get_charset_schema(con, dbname):
    _e("Getting %s's Charset..." % (dbname,))
    with con as cursor:
        cursor.execute(QUERY_CHARSET_SCHEMA, (dbname,))
        charset = cursor.fetchone()

    return charset.get("default_character_set_name")


def _get_table_charset(con, dbname, tablelist):
    stack = []
    _e("Checking table' charset on schema: %s ..." % (dbname,))
    with con as cursor:
        for table in tablelist:
            cursor.execute(QUERY_CHARSET_TABLE, (dbname, table))
            res = cursor.fetchone()
            if res:
                res = res.get('character_set_name')
                stack.append({
                    "name": table, 
                    "charset": res
                })
    return stack


@click.command()
@click.option("-h", default="localhost", help="MySQL host address")
@click.option("-p", default=3306, help="MySQL Port")
@click.option("-u", default="root", help="MySQL Username")
@click.option("-pw", default="", help="MySQL Password")
@click.option("-o", default="checktable.dump.json", help="output filename")
def run(**kwargs):
    _e("Starting...")
    stack = []
    con = _connect(**kwargs)
    dbs = get_databases(con)
    for db in dbs:
        tablelist = get_tables(con, db)
        dbcharset = _get_charset_schema(con, db)
        charsets = _get_table_charset(con, db, tablelist)

        tmp = {
            "schema": db,
            "charset": dbcharset,
            "tables": charsets
        }
        stack.append(tmp)
    
    with open(kwargs.get("o"), 'w') as f:
        f.write(json.dumps(stack))

    _e("Done.")
    

    
if __name__ == '__main__':
    run()
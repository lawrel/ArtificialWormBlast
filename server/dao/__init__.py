"""dao"""
import sys
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool
from os.path import dirname, basename, isfile
import glob
from mysql.connector.errors import Error

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not
           f.endswith('__init__.py')]

_aval_cxns = []
_used_cxns = []

# Database login credentials
_config = {
    'user': 'MonsterCardsDev',
    'password': 'TSitMonsterCards',
    'host': '25.86.80.235',
    'database': 'MonsterCards'
}

cnxpool = MySQLConnectionPool(pool_name="daopool", pool_size=10,
                              **_config)


class SQLExecutionError(Error):
    pass


def execute(query_stmt, params, insert=False):
    """General purpose sql statement executor. Basically a wrapper around
    a MySQL connector. Grabs a connection from a connection pool,
    executes the statement, and returns all rows from the statement
    (if there are any).

    Args:
        query_stmt (str): SQL Statement to execute.
        params (tuple): Parameters to put into the statement using string
            formatting.
        insert (bool): Use this when executing an insert statement to get
            the last_insert_key value back.

    Returns:
        :obj:`list` of :obj:`tuple`: Rows retrieved from statement (if there
            are any).
    """

    conn = cnxpool.get_connection()
    conn.autocommit = False
    rows = []
    try:
        cursor = conn.cursor()
        cursor.execute(query_stmt, params)

        try:
            rows = cursor.fetchall()
        except mysql.connector.InterfaceError as err:
            if err.msg == 'No result set to fetch from.':
                # no problem, we were just at the end of the result set
                pass
            else:
                raise

        if (insert is True):
            cursor.execute("select last_insert_id();")
            rows = cursor.fetchall()

        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise SQLExecutionError from err
    finally:
        cursor.close()
        conn.close()
    return rows

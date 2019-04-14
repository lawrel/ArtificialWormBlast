"""dao"""
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool
from os.path import dirname, basename, isfile
import glob

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

_aval_cxns = []
_used_cxns = []

# Database login credentials
_config = {
    'user': 'MonsterCardsDev',
    'password': 'TSitMonsterCards',
    'host': '25.86.80.235',
    'database': 'MonsterCards'
}

cnxpool = MySQLConnectionPool(pool_name = "daopool", pool_size = 10,
                              **_config)
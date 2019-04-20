"""database"""
import sys
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool
from os.path import dirname, basename, isfile
import glob
from mysql.connector.errors import Error
from server.exceptions import SQLExecutionError

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not
           f.endswith('__init__.py')]
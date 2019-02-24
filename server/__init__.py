"""server"""
from flask import Flask
from os.path import dirname, basename, isfile
import glob
import mysql.connector
from mysql.connector import errorcode

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

app = Flask(__name__)

# This is a really goofy way to make the db_context global in the package
db_context = None

def connect_db():
    # Database login credentials
    config = {
        'user': 'MonsterCardsDev',
        'password': 'TSitMonsterCards',
        'host': '25.86.80.235',
        'database': 'MonsterCards'
    }

    try:
        db_context = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return db_context

db_context = connect_db()

"""server"""
from flask import Flask
from os.path import dirname, basename, isfile
import glob
import mysql.connector
from mysql.connector import errorcode
from flask_socketio import SocketIO


modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app,async_mode='threading')
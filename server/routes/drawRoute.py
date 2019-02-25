""" https://github.com/prabeesh/Paintapp-Javascript-Canvas-Flask/blob/master/test.py """

from flask import *
import mysql.connector
from mysql.connector import errorcode
import uuid
from datetime import date, datetime, timedelta


app = Flask(__name__)

@app.route("/monstereditor")
def sessions():
return render_template('drawMonster.html')

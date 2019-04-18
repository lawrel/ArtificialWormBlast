"""AWB

draw_route.py Handles all routes
for cards and drawing tools, and
decks/hands for players
"""

from flask import (Flask, render_template, request, jsonify, redirect, url_for,
                   send_file)
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import errorcode
import uuid
import io
from datetime import date, datetime, timedelta
from server import app
import server.dao as dao
import server.dao.accounts
import server.dao.cards
from server.exceptions import *
import base64
from werkzeug.exceptions import BadRequestKeyError


def allowed_file(filename):
    """Function checks if the file is in an acceptable format"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg'])


@app.route("/editor")
def editor():
    """Route to monster editor"""
    return render_template('drawMonster.html')

"""home_route.py Handles all routes of the navigator"""


from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from server import app


@app.route('/home/')
def home():
    """Route to home"""

    return render_template('home.html',
                           cardview=render_template("deck_view_home.html"))


@app.route('/instructions/')
def Instructions():
    """Rotue to instructions"""

    return render_template('instructions.html')


@app.route('/monstereditor/')
def monsterEditor():
    """Route to monster editior from navigator"""

    return render_template('draw_monster.html')


@app.route("/")
def index():
    """Route to index/pre-login"""

    return render_template('index.html')

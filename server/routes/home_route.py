"""
AWB

home_route.py Handles all routes of the navigator

"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from server import app

"""
Route to home
"""
@app.route('/home/')
def home():
    return render_template('home.html', cardview=render_template("deck_view_home.html"))


"""
Rotue to instructions
"""
@app.route('/instructions/')
def Instructions():
    return render_template('instructions.html')


"""
Route to monster editior from navigator
"""
@app.route('/monstereditor/')
def monsterEditor():
    return render_template('draw_monster.html')


"""
Route to index/pre-login
"""
@app.route("/")
def index():
    return render_template('index.html')

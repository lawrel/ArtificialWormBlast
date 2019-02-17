from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import errorcode
from server import app
from server import db_context

#Functions defining the pages
@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/lobby/')
def lobby():
    return render_template('lobby.html')

@app.route('/instructions/')
def Instructions():
    return render_template('Instructions.html')

@app.route('/monstereditor/')
def monsterEditor():
    return render_template('drawMonster.html')

@app.route("/")
def hello_name():
    return render_template('welcome.html')

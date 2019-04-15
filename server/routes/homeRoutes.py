from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from server import app
from server.routes import accountRoute

#Functions defining the pages
@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/Instructions/')
def Instructions():
    return render_template('Instructions.html')

@app.route('/monstereditor/')
def monsterEditor():
    return render_template('drawMonster.html')

@app.route("/")
def index():
    return render_template('index.html')

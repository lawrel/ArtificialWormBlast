from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from server import app

#Functions defining the pages
@app.route('/home/')
def home():
    return render_template('home.html', cardview=render_template("deck_view.html"))


@app.route('/instructions/')
def Instructions():
    return render_template('Instructions.html')

@app.route('/monstereditor/')
def monsterEditor():
    return render_template('drawMonster.html')

@app.route("/")
def index():
    return render_template('index.html')

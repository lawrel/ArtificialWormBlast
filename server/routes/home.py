from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from server import app
from server.routes import accounts

#Functions defining the pages
@app.route('/home/')
def home():
    # login_token = request.args.get("login_token")

    # db_context = connect_db()
    # if (accounts.is_valid_token(login_token, db_context) == False):
    #     return redirect(url_for("login", redir_url=url_for("home")))

    print("HERE TO OPEN HOME")

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

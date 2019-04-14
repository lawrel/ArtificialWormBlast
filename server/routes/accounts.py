from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
import uuid
from datetime import date, datetime, timedelta
from validate_email import validate_email

import urllib.parse

from server.routes.emailSending import email_reset

from server import app
from server.dao import login as l
from server.dao.login import signup, login_user, logout_user, get_session_data
from server.dao.login import (Error, BadEmailError, BadLoginError,
                              BadTokenError, EmailInUseError,
                              ShortPasswordError, UsernameInUseError)

# @app.route("/api/users")
# def users_list():
#     db_context = connect_db()

#     if (db_context == None):
#         return "Can't connect to database. See logs..."

#     cursor = db_context.cursor(dictionary=True)

#     query = ("select ID, First, MidInit, Last, Email from MonsterCards.Users;");

#     cursor.execute("begin")
#     cursor.execute(query)
#     rows = cursor.fetchmany(size=10)

#     cursor.close()

#     return jsonify(rows);


@app.route("/logout", methods=['POST'])
def logout():
    if request.method == "POST":
        token = request.form["login-token"]
        logout_user(token)
        return jsonify({"msg": "user logout succesful."})


@app.route("/login/session-data", methods=['POST'])
def session_data():
    if request.method == "POST":
        token = request.form["login-token"]
     
        try:
            sesh_data = get_session_data(token)
            return jsonify(sesh_data)
        except BadTokenError:
            return jsonify({"error": "BadTokenError"})
        except Error:
            return jsonify({"error": "OtherError"})


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        # Form input fields
        email = request.form["input-email"]
        if (email is None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password is None):
            return "Password is empty"

        try:
            token = login_user(email, password)
            return jsonify({"login-token": token})
        except BadLoginError:
            return jsonify({"error": "BadLoginError"})
        except Error:
            return jsonify({"error": "OtherError"})


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        # Did we get inputs (as strings)?
        username = request.form["input-username"]
        if (username == None):
            return "Username is empty"
        email = request.form["input-email"]
        if (email is None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password is None):
            return "Password is empty"

        try:
            l.signup(username, email, password)
            if (not l.email_taken(email)):
                raise Error
            else:
                return jsonify({"success":""})
        except UsernameInUseError:
            return jsonify({"error":"UsernameInUseError"})
        except EmailInUseError:
            return jsonify({"error": "EmailInUseError"})
        except ShortPasswordError:
            return jsonify({"error": "ShortPasswordError"})
        except Error:
            return jsonify({"error":"OtherError"})


@app.route("/forgotpassword", methods=['POST'])
def forgotpassword():
    email = request.form["send-email"]
    domain = request.url_root
    link = urllib.parse.urljoin(domain, (url_for("changepassword", newlink = str(uuid.uuid4()))))
    if (not validate_email(email)):
        return jsonify({"error":"BadEmailError"})
    else:
        email_reset(email, link)
        return jsonify({"success":""})


@app.route("/changepassword/<newlink>", methods=['GET'])
def changepassword(newlink):
    return render_template("changepassword.html")



@app.route("/changepass", methods=['POST'])
def changepass():
    username = request.form["input-username"]
    if (username == None):
        return "Username is empty"
    email = request.form["input-email"]
    if (email is None):
        return "Email is empty"
    password = request.form["input-password"]
    if (password == None):
        return "Password is empty"

    try:
        l.change_password(username, email, password)
        if (not l.email_taken(email)):
            raise Error
        else:
            return jsonify({"success":""})
    except ShortPasswordError:
        return jsonify({"error":"ShortPasswordError"})
    except Error:
        return jsonify({"error":"OtherError"})


@app.route("/changesettings", methods=['POST'])
def changesettings():
    username = request.form["input-username"]
    if (username == None):
        return "Username is empty"
    email = request.form["input-email"]
    if (email is None):
        return "Email is empty"
    password = request.form["input-password"]
    
    old_u = request.form["curr-username"]
    old_e = request.form["curr-email"]

    try:

        if (username != old_u):
            l.change_username(username, old_e)
        if (email != old_e):
            l.change_email(username, email)
        if (password != "You should know."):
            l.change_password(username, email, password)


        return jsonify({"success":""})
    except UsernameInUseError:
        return jsonify({"error":"UsernameInUseError"})
    except EmailInUseError:
        return jsonify({"error": "EmailInUseError"})
    except ShortPasswordError:
        return jsonify({"error":"ShortPasswordError"})
    except Error:
        return jsonify({"error":"OtherError"})


    


@app.route('/myaccount')
def myAccount():
    return render_template('Account.html')

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
from server.dao.login import signup, login_user, logout_user, get_session_data, change_password, change_email, change_username
from server.dao.login import Error, BadEmailError, BadLoginError, BadTokenError, EmailInUseError, ShortPasswordError

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
        return jsonify({"msg":"user logout succesful."})


@app.route("/login/session-data", methods=['POST'])
def session_data():
    if request.method == "POST":
        token = request.form["login-token"]
        
        try:
            sesh_data = get_session_data(token)
            return jsonify(sesh_data)
        except BadTokenError:
            return jsonify({"error":"BadTokenError"})
        except Error:
            return jsonify({"error":"OtherError"})


@app.route("/login", methods=['GET', 'POST'])
def login():
    print("HERE TO OPEN LOGIN")
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        # Form input fields
        email = request.form["input-email"]
        if (email == None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password == None):
            return "Password is empty"

        try:
            token = login_user(email, password)
            return jsonify({"login-token" : token})
        except BadLoginError:
            return jsonify({"error":"BadLoginError"})
        except Error:
            return jsonify({"error":"OtherError"})


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        # Did we get inputs (as strings)?
        email = request.form["input-email"]
        if (email is None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password == None):
            return "Password is empty"

        try:
            l.signup(email, password)
            if (not l.email_taken(email)):
                raise Error
            else:
                return jsonify({"success":""})
        except EmailInUseError:
            return jsonify({"error":"EmailInUseError"})
        except ShortPasswordError:
            return jsonify({"error":"ShortPasswordError"})
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
        
@app.route("/changepassword/<newlink>", methods=['GET', 'POST'])
def changepassword(newlink):
    if request.method == "GET":
        return render_template("changepassword.html")
    if request.method == "POST":
        email = request.form["input-email"]
        if (email is None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password == None):
            return "Password is empty"

        try:
            l.change_password(email, password)
            if (not l.email_taken(email)):
                raise Error
            else:
                return jsonify({"success":""})
        except EmailInUseError:
            return jsonify({"error":"EmailInUseError"})
        except ShortPasswordError:
            return jsonify({"error":"ShortPasswordError"})
        except Error:
            return jsonify({"error":"OtherError"})

    


@app.route('/myaccount')
def myAccount():
    return render_template('Account.html')
    


    

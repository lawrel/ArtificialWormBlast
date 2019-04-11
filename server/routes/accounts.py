from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
import uuid
from datetime import date, datetime, timedelta

from server import app
from server.dao import login as l
from server.dao.login import Error, BadEmailError, BadLoginError, BadTokenError

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

@app.route("/login/token-valid", methods=['POST'])
def login_valid_token():
    if request.method == "POST":
        token = request.form["login-token"]
        return jsonify({"valid":l.is_valid_token(token)})

@app.route("/login/session-data", methods=['POST'])
def login_session_data():
    if request.method == "POST":
        token = request.form["login-token"]
        try:
            sesh_data = l.get_session_data(token)
            return jsonify(sesh_data)
        except BadTokenError:
            return jsonify({"error":"BadTokenError"})
        except Error:
            return jsonify({"error":"OtherError"})

@app.route("/login", methods=['GET', 'POST'])
def login():
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
            token = l.login_user(email, password)
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
        # Do we have a database context?
        db_context = connect_db()
        if (db_context == None):
            return "Can't connect to database."

        # Did we get inputs (as strings)?
        email = request.form["input-email"]
        if (email is None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password == None):
            return "Password is empty"

        # Is the email already in use
        if (get_userid(email, db_context) is not None):
            return "This email is already in use."

        # We use the cursor object to execute queries, parse, store their results
        query = ("""
                    INSERT INTO MonsterCards.Users (Email, Password)
                    VALUES (%s, sha2(%s, 256));
                    """);
        cursor = db_context.cursor()
        cursor.execute("BEGIN;")
        cursor.execute(query, (email, password))
        cursor.execute("COMMIT;")
        cursor.close()

        # Did we successfully add the user?
        if (get_user(email, password) is not None):
            return redirect(url_for('login'))
        else:
            return "Error occurred."

@app.route('/myaccount')
def myAccount():
    return render_template('Account.html')

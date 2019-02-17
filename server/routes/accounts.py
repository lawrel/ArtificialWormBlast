from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
import uuid
from datetime import date, datetime, timedelta

from server import app, db_context, connect_db

print("Something")

def validate_request_token(request):
    db_context = connect_db()
    # return true if the token is a valid login request_token_valid
    # query the database
    if (db_context == None):
        return "Can't connect to database. See logs..."

    # cursor handles execution sql transactions
    cursor = db_context.cursor(dictionary=True)

    query = ("select AuthToken from MonsterCards.Users;");

    cursor.execute("begin")
    cursor.execute(query)
    rows = cursor.fetchmany(size=10)

@app.route("/api/users")
def users_list():
    db_context = connect_db()

    if (db_context == None):
        return "Can't connect to database. See logs..."

    cursor = db_context.cursor(dictionary=True)

    query = ("select ID, First, MidInit, Last, Email from MonsterCards.Users;");

    cursor.execute("begin")
    cursor.execute(query)
    rows = cursor.fetchmany(size=10)

    cursor.close()

    return jsonify(rows);

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        db_context = connect_db()

        if (db_context == None):
            return "Can't connect to database. See logs..."


        # Form input fields
        email = request.form["input-email"]
        if (email == None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password == None):
            return "Password is empty"

        cursor = db_context.cursor()
        user_entry = ("""SELECT ID, Email, Password FROM MonsterCards.Users
                            WHERE Email = %s AND Password = sha2(%s,256);
                         """);
        cursor.execute(user_entry, (email, password))

        user_row = cursor.fetchmany(size=1)
        print(user_row)
        if (len(user_row) != 1):
            return "bad credentials"

        ID, Email, Password = user_row[0];
        token = str(uuid.uuid4())
        exp_date = datetime.now().date() + timedelta(seconds=1)

        # Add to UserLogins
        update_UserLogins = ("""BEGIN;
                                INSERT INTO MonsterCards.UserLogins (AccountID, AuthToken, ExpirationDate)
                                VALUES (%s, %s, %s)
                                ON DUPLICATE KEY UPDATE
                                    AuthToken = %s,
                                    ExpirationDate = %s;
                                COMMIT;""");

        cursor.execute(update_UserLogins, (ID, token, exp_date, token, exp_date))

        cursor.close()
        return token;
        return redirect(url_for('home'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        db_context = connect_db()

        email = request.form["input-email"]
        if (email == None):
            return "Email is empty"

        password = request.form["input-password"]
        if (password == None):
            return "Password is empty"


        # Check that query exists
        # Do we have a database context?
        if (db_context == None):
            return "Can't connect to database. See logs..."

        # We use the cursor object to execute queries, parse, store their results
        cursor = db_context.cursor(dictionary=True)

        query = ("""insert into MonsterCards.Users (Email, Password)
                    values (%s, sha2(%s, 256))""");

        #cursor.execute("begin")
        cursor.execute(query, (email, password))

        # Grab the next 10 results of the query
        rows = cursor.fetchmany(size=10)

        cursor.close()

        return redirect(url_for('login'))

@app.route('/myaccount/')
def myAccount():
    return render_template('Account.html')

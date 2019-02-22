from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
import uuid
from datetime import date, datetime, timedelta

from server import app, db_context, connect_db

print("Something")
def get_userid(email, db_context=connect_db()):
    if (db_context == None):
        return None
    if (email == None):
        return None

    print(str(email))
    cursor = db_context.cursor()
    user_entry = ("""SELECT ID, Email FROM MonsterCards.Users
                        WHERE Email = %s;""");

    cursor.execute(user_entry, (email,))

    user_row = cursor.fetchmany(size=1)
    print(user_row)
    if (len(user_row) != 1):
        return None

    return user_row[0][0]

def get_user(email, pw, db_context=connect_db()):
    if (db_context == None):
        return None
    if (email == None):
        return None
    if (pw == None):
        return None

    cursor = db_context.cursor()
    user_entry = ("""SELECT ID, Email, Password FROM MonsterCards.Users
                        WHERE Email = %s AND Password = sha2(%s,256);
                     """);
    cursor.execute(user_entry, (email, pw))

    user_row = cursor.fetchmany(size=1)
    print(user_row)
    if (len(user_row) != 1):
        return None

    return user_row[0]


def validate_request_token(request, db_context=connect_db()):
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

# This route is not really used
@app.route("/api/users")
def users_list():
    db_context = connect_db()
    if (db_context == None):
        return "Can't connect to database. See logs..."

    cursor = db_context.cursor(dictionary=True)
    query = ("select ID, First, MidInit, Last, Email from MonsterCards.Users;");
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

        # We will try to get the user record from database
        ID, Email, Password = get_user(email, password, db_context);
=======
        # We will try to get the user record from database
        ID, Email, Password = get_user(email, password, db_context);
>>>>>>> Stashed changes
        token = str(uuid.uuid4())
        exp_date = datetime.now().date() + timedelta(seconds=1)

        # Add to UserLogins
        cursor = db_context.cursor()
        update_UserLogins = ("""BEGIN;
                                INSERT INTO MonsterCards.UserLogins (AccountID, AuthToken, ExpirationDate)
                                VALUES (%s, %s, %s)
                                ON DUPLICATE KEY UPDATE
                                    AuthToken = %s,
                                    ExpirationDate = %s;
                                COMMIT;""");
        cursor.execute(update_UserLogins, (ID, token, exp_date, token, exp_date))
        cursor.close()

        # Return token, let the view handle redirect.
        return token;
        # return redirect(url_for('home'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":

=======

>>>>>>> Stashed changes
        # Do we have a database context?
        db_context = connect_db()
        if (db_context == None):
            return "Can't connect to database. See logs..."

        # Did we get inputs
        email = request.form["input-email"]
        if (email == None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password == None):
            return "Password is empty"

        # Is the email already in use
        if (get_userid(email, db_context) is not None):
            return "This email is already in use."

        # We use the cursor object to execute queries, parse, store their results
        cursor = db_context.cursor()
=======

        # We use the cursor object to execute queries, parse, store their results
        cursor = db_context.cursor()
>>>>>>> Stashed changes
        query = ("""begin;
                    insert into MonsterCards.Users (Email, Password)
                    values (%s, sha2(%s, 256));
                    commit;""");
        cursor.execute(query, (email, password))
        cursor.close()

        # Did the user get added to db?
=======
        cursor.execute(query, (email, password))
        cursor.close()

        # Did the user get added to db?
>>>>>>> Stashed changes
        if (get_user(email, password) is not None):
            return redirect(url_for('login'))
        else:
            return "Error occurred."

@app.route('/myaccount/')
def myAccount():
    return render_template('Account.html')

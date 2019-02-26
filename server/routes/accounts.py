from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
import uuid
from datetime import date, datetime, timedelta

from server import app, db_context, connect_db

# Input:    Email string
# Changes:  nothing
# Return:   integer number
def get_userid(email, db_context=connect_db()):
    # Did we get inputs (as strings)?
    if (db_context == None):
        return None
    if (email == None):
        return None

    # Query database
    user_entry = ("""SELECT ID, Email FROM MonsterCards.Users
                        WHERE Email = %s;""");
    cursor = db_context.cursor()
    cursor.execute(user_entry, (email,))

    # Is the user in the db?
    user_row = cursor.fetchmany(size=1)
    if (len(user_row) != 1):
        return None

    return user_row[0][0]

# Input:    Email string, password string
# Changes:  nothing
# Return:   (ID, Email, Password) or None
def get_user(email, pw, db_context=connect_db()):
    if (db_context == None):
        return None
    if (email == None):
        return None
    if (pw == None):
        return None

    user_entry = ("""SELECT ID, Email, Password FROM MonsterCards.Users
                        WHERE Email = %s AND Password = sha2(%s,256);
                     """);
    cursor = db_context.cursor()
    cursor.execute(user_entry, (email, pw))

    user_row = cursor.fetchmany(size=1)
    print(user_row)
    if (len(user_row) != 1):
        return None

    return user_row[0]

def is_valid_token(token, db_context=connect_db()):
    if (db_context == None):
        return False;

    print("Token: ", token)

    curr_date = datetime.now().date()

    query = ("""select AuthToken, AccountID, ExpirationDate from MonsterCards.UserLogins
                    WHERE AuthToken = %s;""");
    # cursor handles execution sql transactions
    cursor = db_context.cursor()
    cursor.execute(query, (token,))
    rows = cursor.fetchmany(size=1)
    cursor.close()

    # Is the user logged in?
    if (len(rows) != 1):
        return False
    return True

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
        # Do we have a database context?
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

        # Retrieve userid from email
        row =  get_user(email, password, db_context);
        print(row)
        if (row is None):
            return redirect(url_for("login"))
        ID,_,_ = row

        # Create our login credential and update the expiration date
        token = str(uuid.uuid4())
        exp_date = datetime.now().date() + timedelta(seconds=1800)

        update_UserLogins = ("""BEGIN;
                                INSERT INTO MonsterCards.UserLogins (AccountID, AuthToken, ExpirationDate)
                                VALUES (%s, %s, %s)
                                ON DUPLICATE KEY UPDATE
                                    AuthToken = %s,
                                    ExpirationDate = %s;
                                COMMIT;""");
        cursor = db_context.cursor()
        cursor.execute(update_UserLogins, (ID, token, exp_date, token, exp_date))
        cursor.close()

        redir_url = request.args.get("redir_url")
        if (redir_url is not None):
            return redirect(redir_url + "?login_token=" + token)
        else:
            return redirect(url_for('home', login_token=token))

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
        query = ("""BEGIN;
                    INSERT INTO MonsterCards.Users (Email, Password)
                    VALUES (%s, sha2(%s, 256));
                    COMMIT;""");
        cursor = db_context.cursor()
        cursor.execute(query, (email, password))
        cursor.close()

        # Did we successfully add the user?
        if (get_user(email, password) is not None):
            return redirect(url_for('login'))
        else:
            return "Error occurred."

@app.route('/myaccount/')
def myAccount():
    return render_template('Account.html')

"""account_route.py Handles all routes for accounts and account managements"""

from flask import render_template, request, jsonify, url_for
import uuid
from validate_email import validate_email
import urllib.parse
from server import app


import database.dao as dao
import database.dao.accounts
import database.dao.cards
import objects.email_helper
from server.exceptions import (UsernameInUseError, BadTokenError, Error,
                               BadLoginError, EmailInUseError,
                               ShortPasswordError)


@app.route("/logout", methods=['POST'])
def logout():
    """Route to logout"""

    if request.method == "POST":
        token = request.form["login-token"]
        dao.accounts.logout_user(token)
        return jsonify({"msg": "user logout succesful."})


@app.route("/login/session-data", methods=['POST'])
def session_data():
    """Route to retrieve session data"""

    if request.method == "POST":
        token = request.form["login-token"]

        try:
            sesh_data = dao.accounts.get_session_data(token)
            return jsonify(sesh_data)
        except BadTokenError:
            return jsonify({"error": "BadTokenError"})
        except Error:
            return jsonify({"error": "OtherError"})


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Route to login"""

    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form["input-email"]
        if (email is None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password is None):
            return "Password is empty"

        try:
            token = dao.accounts.login_user(email, password)
            return jsonify({"login-token": token})
        except BadLoginError:
            return jsonify({"error": "BadLoginError"})
        except Error:
            return jsonify({"error": "OtherError"})


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """Route to signup"""

    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        username = request.form["input-username"]
        if (username is None):
            return "Username is empty"
        email = request.form["input-email"]
        if (email is None):
            return "Email is empty"
        password = request.form["input-password"]
        if (password is None):
            return "Password is empty"

        try:
            dao.accounts.signup(username, email, password)
            if (not dao.accounts.email_taken(email)):
                raise Error
            else:
                return jsonify({"success": ""})
        except UsernameInUseError:
            return jsonify({"error": "UsernameInUseError"})
        except EmailInUseError:
            return jsonify({"error": "EmailInUseError"})
        except ShortPasswordError:
            return jsonify({"error": "ShortPasswordError"})
        except Error:
            return jsonify({"error": "OtherError"})


@app.route("/forgotpassword", methods=['POST'])
def forgotpassword():
    """Route to get link for forgotten password"""

    email = request.form["send-email"]
    domain = request.url_root
    link = urllib.parse.urljoin(domain, (url_for("changepassword",
                                                 newlink=str(uuid.uuid4()))))
    if (not validate_email(email)):
        return jsonify({"error": "BadEmailError"})
    else:
        objects.email_helper.email_reset(email, link)
        return jsonify({"success": ""})


@app.route("/changepassword/<newlink>", methods=['GET'])
def changepassword(newlink):
    """Route to unique password changer"""

    return render_template("changePassword.html")


@app.route("/changepass", methods=['POST'])
def changepass():
    """Route to update the changed password"""

    username = request.form["input-username"]
    if (username is None):
        return "Username is empty"
    email = request.form["input-email"]
    if (email is None):
        return "Email is empty"
    password = request.form["input-password"]
    if (password is None):
        return "Password is empty"

    try:
        dao.accounts.change_password(username, email, password)
        if (not dao.accounts.email_taken(email)):
            raise Error
        else:
            return jsonify({"success": ""})
    except ShortPasswordError:
        return jsonify({"error": "ShortPasswordError"})
    except Error:
        return jsonify({"error": "OtherError"})


@app.route("/changesettings", methods=['POST'])
def changesettings():
    """Route to update settings"""

    username = request.form["input-username"]
    if (username is None):
        return "Username is empty"
    email = request.form["input-email"]
    if (email is None):
        return "Email is empty"
    password = request.form["input-password"]

    old_u = request.form["curr-username"]
    old_e = request.form["curr-email"]

    try:

        if (username != old_u):
            dao.accounts.change_username(username, old_e)
        if (email != old_e):
            dao.accounts.change_email(username, email)
        if (password != "You should know."):
            dao.accounts.change_password(username, email, password)

        return jsonify({"success": ""})
    except UsernameInUseError:
        return jsonify({"error": "UsernameInUseError"})
    except EmailInUseError:
        return jsonify({"error": "EmailInUseError"})
    except ShortPasswordError:
        return jsonify({"error": "ShortPasswordError"})
    except Error:
        return jsonify({"error": "OtherError"})


@app.route('/myaccount')
def myAccount():
    """Route to account page"""

    return render_template('account.html')

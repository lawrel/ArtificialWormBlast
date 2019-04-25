"""games_route.py Handles are the roots for games"""


from flask_socketio import SocketIO
from flask import Flask, render_template, request, jsonify
from server import app, socketio
from validate_email import validate_email
import urllib.parse
from objects.email_helper import email_gamelink


@app.route('/game/')
def sessions():
    """Route for a general game"""

    return render_template('game.html',
                           cardview=render_template("deck_view.html"))


@app.route('/gameEnd/')
def gameEnd():
    """Route for a general game ending"""

    return render_template('gameEnd.html')


@app.route('/privategame/')
def session1():
    """Route for a private game"""

    return render_template('private_game.html',
                           cardview=render_template("deck_view.html"))


@app.route('/publicgame/')
def session2():
    """Route for a public game"""

    return render_template('game.html',
                           cardview=render_template("deck_view.html"))


@app.route('/sitedeck/')
def monsters():
    """Route for the site deck location"""

    return render_template('site_deck.html',
                           cardview=render_template("deck_view_site.html"))


@app.route('/sendinvites', methods=['POST'])
def invites():
    """Route to send emails invites"""

    newlink = request.form["game-id"]
    if (newlink is None):
        return "Link is empty"
    for i in range(1, 10):
        email = request.form["send-email" + str(i)]
        if (email is not None):
            domain = request.url_root
            link = urllib.parse.urljoin(domain, newlink)
            if (not validate_email(email)):
                return jsonify({"error": "BadEmailError"})
            else:
                email_gamelink(email, link)
    return jsonify({"success": ""})

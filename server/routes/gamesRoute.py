from flask_socketio import SocketIO
from flask import Flask, render_template, request, jsonify
from server import app, socketio
from validate_email import validate_email
import urllib.parse

from server.routes.emailObject import email_gamelink

# @app.route('/game/?game_id=<newlink>', methods=['GET'])
# def sesh(newlink):
#     print("helo wolrd =====================================================================")
#     return render_template('game.html', cardview=render_template('deck_veiw.html'))

@app.route('/game/')
def sessions():
    return render_template('game.html', cardview=render_template("deck_view.html"))


@app.route('/privategame/')
def session1():
    return render_template('private_game.html')


@app.route('/publicgame/')
def session2():
    return render_template('game.html', cardview=render_template("deck_view.html"))


@app.route('/sitedeck/')
def monsters():
    return render_template('site_deck.html', cardview=render_template("deck_view_site.html"))


@app.route('/sendinvites', methods=['POST'])
def invites():
    newlink = request.form["game-id"]
    if (newlink == None):
        return "Link is empty"
    for i in range(1, 10):
        email = request.form["send-email"+ str(i)]
        if (email is not None):
            domain = request.url_root
            link = urllib.parse.urljoin(domain, newlink)
            if (not validate_email(email)):
                return jsonify({"error":"BadEmailError"})
            else:
                email_gamelink(email, link)
                return jsonify({"success":""})







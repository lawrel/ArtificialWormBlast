from flask_socketio import SocketIO
from flask import Flask, render_template, request, jsonify
from server import app, socketio


@app.route('/game/')
def sessions():
    return render_template('game.html')


@app.route('/privategame/')
def session1():
    return render_template('private_game.html')


@app.route('/publicgame/')
def session2():
    return render_template('public_game.html')


@app.route('/sitedeck/')
def monsters():
    return render_template('site_deck.html')


@app.route('/sendinvites')
def invites():
    newlink = str(uuid.uuid4()
    for i in range(1,10):
        email = request.form["send-email"+ i]
        if (email is not None):
            domain = request.url_root
            link = urllib.parse.urljoin(domain, (url_for("changepassword", newlink))))
            if (not validate_email(email)):
                return jsonify({"error":"BadEmailError"})
            email_gamelink(email, link)
    else:
        upate_URL(newlink) # add url so can get for host
        return jsonify({"success":""})




"""
AWB

draw_route.py Handles all routes 
for cards and drawing tools, and 
decks/hands for players

"""

from flask import (Flask, render_template, request, jsonify, redirect, url_for,
                   send_file)
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import errorcode
import uuid
import io
from datetime import date, datetime, timedelta
from server import app
from server.dao import cards
from server.exceptions import exceptions
from server.dao import login
import base64
from werkzeug.exceptions import BadRequestKeyError


""" 
Function checks if the file is in an acceptable format
"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg'])


"""
Route to monster editor
"""
@app.route("/editor")
def editor():
    return render_template('drawMonster.html')


"""
Route to start editing new card
"""
@app.route("/cards/new-card", methods=["POST"])
@app.route("/editor/upload-img-b64", methods=["POST"])
def editor_new_card():
    try:
        token = request.form["token"]
        b64_file = request.form["img-data"]
        card_name = request.form.get("card-name")

        user_id = get_session_data(token)["userid"]

        if b64_file == '':
            raise NoFileUploadedError

        b64_f = b64_file.split(",")[-1]
        bin_file = base64.b64decode(b64_f)
        card_id = cards.new_card(bin_file, "{}", name=card_name)
        cards.addPlayerCard(user_id, card_id)

        return jsonify({"success": "", "card_id": card_id})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadRequestKeyError:
        return jsonify({"error": "BadRequestKeyError"})


"""
Route to edit existing card
"""
@app.route("/cards/edit-card", methods=["POST"])
def editor_edit_card():
    try:
        token = request.form["token"]
        b64_file = request.form["img-data"]
        card_id = request.form["card-id"]
        card_name = request.form.get("card-name")

        user_id = get_session_data(token)["userid"]

        if b64_file == '':
            raise NoFileUploadedError

        b64_f = b64_file.split(",")[-1]
        bin_file = base64.b64decode(b64_f)

        cards.edit_card(card_id, bin_file, "{}", name=card_name)

        return jsonify({"success": ""})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadFileExtError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadRequestKeyError:
        return jsonify({"error": "BadRequestKeyError"})


"""
Route to remove card
"""
@app.route("/cards/remove-card", methods=["POST"])
def remove_card():
    try:
        token = request.form["token"]
        card_id = request.form["card-id"]

        user_id = get_session_data(token)["userid"]

        cards.remove_player_card(user_id, card_id)

        return jsonify({"success": ""})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except BadRequestKeyError:
        return jsonify({"error": "BadRequestKeyError"})


"""
Route to preview card
"""
@app.route("/cards/preview/<card_id>", methods=["GET"])
def get_card_image(card_id):
    card_id, card_name, img_bin, attrs = get_card(card_id)
    return send_file(io.BytesIO(img_bin),
                     mimetype='image/png',
                     as_attachment=True,
                     attachment_filename='%s.png' % card_id)


"""
Route to get a player's hand
"""
@app.route("/cards/player_cards", methods=["POST"])
def get_player_cards():
    try:
        if ("token" not in request.form):
            return jsonify({"error": ""})
        token = request.form["token"]
        sesh_data = get_session_data(token)
        user_id = sesh_data["userid"]
        cards = getPlayerDeck(user_id)
        print(cards)
        return jsonify({"cards": cards})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadFileExtError:
        return jsonify({"error": "NoFileUploadedError"})


"""
Route to site deck
"""
@app.route("/cards/site_cards", methods=["POST"])
def get_site_cards():
    try:
        cards = getSiteDeck()
        return jsonify({"cards": cards})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadFileExtError:
        return jsonify({"error": "NoFileUploadedError"})


"""
Route to add card
"""
@app.route("/cards/add-card", methods=["POST"])
def add_site_cards():
    try:
        if ("token" not in request.form):
            return jsonify({"error": ""})
        token = request.form["token"]
        sesh_data = get_session_data(token)
        user_id = sesh_data["userid"]
        card_id = request.form["card-id"]
        print(user_id, card_id)
        if (card_id is None):
            return "No card to add"
        card = cards.addPlayerCard(user_id, card_id)
        return jsonify({"cards": card})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadFileExtError:
        return jsonify({"error": "NoFileUploadedError"})

"""cards.py Handles all routes
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
import database.dao as dao
import database.dao.accounts
import database.dao.cards
from server.exceptions import (BadEmailError, NoFileUploadedError,
                               BadTokenError, BadFileExtError,
                               SQLExecutionError)
import base64
from werkzeug.exceptions import BadRequestKeyError


@app.route("/cards/new-card", methods=["POST"])
@app.route("/editor/upload-img-b64", methods=["POST"])
def editor_new_card():
    """Route to start editing new card"""

    try:
        token = request.form["token"]
        b64_file = request.form["img-data"]
        card_name = request.form.get("card-name")

        user_id = dao.accounts.get_session_data(token)["userid"]

        if b64_file == '':
            raise NoFileUploadedError

        b64_f = b64_file.split(",")[-1]
        bin_file = base64.b64decode(b64_f)
        card_id = dao.cards.new_card(bin_file, "{}", name=card_name)
        dao.cards.add_player_card(user_id, card_id)

        return jsonify({"success": "", "card_id": card_id})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadRequestKeyError:
        return jsonify({"error": "BadRequestKeyError"})


@app.route("/cards/edit-card", methods=["POST"])
def editor_edit_card():
    """Route to edit existing card"""

    try:
        # token = request.form["token"]
        b64_file = request.form["img-data"]
        card_id = request.form["card-id"]
        card_name = request.form.get("card-name")
        # user_id = dao.accounts.get_session_data(token)["userid"]

        if b64_file == '':
            raise NoFileUploadedError

        b64_f = b64_file.split(",")[-1]
        bin_file = base64.b64decode(b64_f)

        dao.cards.edit_card(card_id, bin_file, "{}", name=card_name)

        return jsonify({"success": ""})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadFileExtError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadRequestKeyError:
        return jsonify({"error": "BadRequestKeyError"})


@app.route("/cards/remove-card", methods=["POST"])
def remove_card():
    """Route to remove card"""

    try:
        token = request.form["token"]
        card_id = request.form["card-id"]

        user_id = dao.accounts.get_session_data(token)["userid"]

        dao.cards.remove_player_card(user_id, card_id)

        return jsonify({"success": ""})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except BadRequestKeyError:
        return jsonify({"error": "BadRequestKeyError"})


@app.route("/cards/preview/<card_id>", methods=["GET"])
def get_card_image(card_id):
    """Route to preview card"""

    try:
        card_id, _, img_bin, _ = dao.cards.get_card(card_id)
        return send_file(io.BytesIO(img_bin),
                         mimetype='image/png',
                         as_attachment=True,
                         attachment_filename='%s.png' % card_id)
    except SQLExecutionError:
        return jsonify({"error": "SQLExecutionError"})


@app.route("/cards/player_cards", methods=["POST"])
def get_player_cards():
    """Route to get a player's hand"""

    try:
        if ("token" not in request.form):
            return jsonify({"error": ""})
        token = request.form["token"]
        sesh_data = dao.accounts.get_session_data(token)
        user_id = sesh_data["userid"]
        cards = dao.cards.get_player_deck(user_id)
        print(cards)
        return jsonify({"cards": cards})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadFileExtError:
        return jsonify({"error": "NoFileUploadedError"})


@app.route("/cards/site_cards", methods=["POST"])
def get_site_cards():
    """Route to site deck"""

    try:
        cards = dao.cards.get_site_deck()
        return jsonify({"cards": cards})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadFileExtError:
        return jsonify({"error": "NoFileUploadedError"})


@app.route("/cards/add-card", methods=["POST"])
def add_site_cards():
    """Route to add card"""

    try:
        if ("token" not in request.form):
            return jsonify({"error": ""})
        token = request.form["token"]
        sesh_data = dao.accounts.get_session_data(token)
        user_id = sesh_data["userid"]
        card_id = request.form["card-id"]
        print(user_id, card_id)
        if (card_id is None):
            return "No card to add"
        dao.cards.add_player_card(user_id, card_id)
        return jsonify({"cards": card_id})
    except BadTokenError:
        return jsonify({"error": "BadTokenError"})
    except NoFileUploadedError:
        return jsonify({"error": "NoFileUploadedError"})
    except BadFileExtError:
        return jsonify({"error": "NoFileUploadedError"})

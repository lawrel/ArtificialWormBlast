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
from server.dao.cards import (get_card, getPlayerDeck,
                              EmptyFileError, BadFileExtError,
                              FileTooLargeError, NoFileUploadedError)
from server.dao import login
from server.dao.login import get_session_data, BadTokenError
import base64
from werkzeug.exceptions import BadRequestKeyError


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/editor")
def editor():
    return render_template('drawMonster.html')


# @app.route("/cards/new-card", methods=["POST"])
# @app.route("/editor/upload-img", methods=["POST"])
# def editor_upload_img():
#     # print(request.files)
#     try:
#         if "monster-image" not in request.files:
#             raise NoFileUploadedError
#         img_file = request.files.get("monster-image")
#         if img_file.filename == '':
#             raise NoFileUploadedError
#         if (not allowed_file(img_file.filename)):
#             raise BadFileExtError

#         filename = secure_filename(img_file.filename)
#         card_id = cards.new_card(img_file.read(), "{}")

#         return jsonify({"success": "", "card_id": card_id})
#     except NoFileUploadedError:
#         return jsonify({"error": "NoFileUploadedError"})
#     except BadFileExtError:
#         return jsonify({"error": "NoFileUploadedError"})


@app.route("/cards/new-card", methods=["POST"])
@app.route("/editor/upload-img-b64", methods=["POST"])
def editor_new_card():
    print(request.files)
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


@app.route("/cards/edit-card", methods=["POST"])
def editor_edit_card():
    # print(request.files)
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


@app.route("/cards/remove-card", methods=["POST"])
def remove_card():
    # print(request.files)
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


@app.route("/cards/preview/<card_id>", methods=["GET"])
def get_card_image(card_id):
    card_id, card_name, img_bin, attrs = get_card(card_id)
    return send_file(io.BytesIO(img_bin),
                     mimetype='image/png',
                     as_attachment=True,
                     attachment_filename='%s.png' % card_id)


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
    except BadRequestKeyError:
        return jsonify({"error": "BadRequestKeyError"})

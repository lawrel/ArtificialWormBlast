"""AWB

draw_route.py Handles all routes
for cards and drawing tools, and
decks/hands for players
"""

from flask import render_template
from server import app


def allowed_file(filename):
    """Function checks if the file is in an acceptable format"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg'])


@app.route("/editor")
def editor():
    """Route to monster editor"""
    return render_template('drawMonster.html')

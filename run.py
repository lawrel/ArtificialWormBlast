from flask import Flask
from server import app, socketio
from server.routes import (account_route, cards, draw_route, games_route,
                           home_route)
# from server.routes.chatRoute import *

if __name__ == "__main__":
    Flask.run(app, host="0.0.0.0", port=8000, debug=True)

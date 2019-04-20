from server import app, socketio
from server import *
from server.routes import *
from flask import Flask
# from server.routes.chatRoute import *

if __name__ == "__main__":
    Flask.run(app, host="0.0.0.0", port=8000, debug=True)

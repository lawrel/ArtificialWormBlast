from server import app, socketio
from server import *
from server.routes import *
# from server.routes.chatRoute import *

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)

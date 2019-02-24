# from server import *
from server import app, db_context, connect_db, socketio
from server.routes import *
from server.routes.chatRoute import *



if __name__ == "__main__":
    connect_db();

    socketio.run(app, host="0.0.0.0", port=8000, debug=True)

    if (db_context != None):
        print("closing");
        db_context.close()

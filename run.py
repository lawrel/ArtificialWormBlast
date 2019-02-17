# from server import *
from server import app, db_context, connect_db
from server.routes import *


if __name__ == "__main__":
    connect_db();

    app.run(debug=True, host="0.0.0.0", port=8000)

    if (db_context != None):
        print("closing");
        db_context.close()

from flask import Flask, render_template
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

@app.route("/")
def hello_name():
    return "hello world"

@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    config = {
        'user': 'seanrice',
        'password': 'conman555',
        'host': '127.0.0.1',
        'database': 'employees'
    }

    db_context = None;
    try:
        db_context = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    app.run(debug=True, host="0.0.0.0", port=8000)

    if (db_context != None):
        print("closing");
        db_context.close()

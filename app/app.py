from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import errorcode
app = Flask(__name__)
db_context = None;



#Functions defining the pages
@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/lobby/')
def lobby():
    return render_template('lobby.html')

@app.route('/myAccount/')
def myAccount():
    return render_template('Account.html')

@app.route('/Instructions/')
def Instructions():
    return render_template('Instructions.html')

@app.route('/monsterEditor/')
def monsterEditor():
    return render_template('drawMonster.html')

@app.route("/")
def hello_name():
    return render_template('welcome.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        r_data = request.data
        print(r_data)

@app.route("/accounts/register-new-user", methods=['POST'])
def register_new_user():
    email = request.form["input-email"]
    if (email == None):
        return "Email is empty"

    password = request.form["input-password"]
    if (password == None):
        return "Password is empty"


    # Check that query exists
    # Do we have a database context?
    if (db_context == None):
        return "Can't connect to database. See logs..."

    # We use the cursor object to execute queries, parse, store their results
    cursor = db_context.cursor(dictionary=True)

    query = ("""insert into MonsterCards.Users (Email, Password)
                values (%s, %s)""");

    cursor.execute("begin")
    cursor.execute(query, (email, password))

    # Grab the next 10 results of the query
    rows = cursor.fetchmany(size=10)

    cursor.close()

    return render_template("user_list.html");

@app.route("/api/query", methods=['POST'])
def api_query():
    # Parse form data for query name
    query_name = request.form["query_name"]
    if (query_name == None):
        return """Please specify the query you wish to run
                with the query_name argument."""

    # Check that query exists
    # Do we have a database context?
    if (db_context == None):
        return "Can't connect to database. See logs..."

    # We use the cursor object to execute queries, parse, store their results
    cursor = db_context.cursor(dictionary=True)

    query = ("select ID, First, MidInit, Last, Email from MonsterCards.Users;");

    cursor.execute("begin")
    cursor.execute(query)

    # Grab the next 10 results of the query
    rows = cursor.fetchmany(size=10)

    cursor.close()

    return render_template("user_list.html");

@app.route("/api/users")
def users_list():
    if (db_context == None):
        return "Can't connect to database. See logs..."

    cursor = db_context.cursor(dictionary=True)

    query = ("select ID, First, MidInit, Last, Email from MonsterCards.Users;");

    cursor.execute("begin")
    cursor.execute(query)
    rows = cursor.fetchmany(size=10)

    cursor.close()

    return jsonify(rows);


if __name__ == "__main__":
    # Database login credentials
    config = {
        'user': 'MonsterCardsDev',
        'password': 'TSitMonsterCards',
        'host': '127.0.0.1',
        'database': 'MonsterCards'
    }

    try:
        db_context = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    app.run(debug=True)

    if (db_context != None):
        print("closing");
        db_context.close()
    
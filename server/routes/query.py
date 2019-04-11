# from server import db_context

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

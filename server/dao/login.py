import uuid
from server.dao import cnxpool
from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from datetime import date, datetime, timedelta


# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

class BadEmailError(Error):
   """Raised when email incorrect"""
   pass

class BadLoginError(Error):
   """Raised when login credentials are bad"""
   pass

class BadTokenError(Error):
   """Raised when a login token is bad"""
   pass


def execute(query_stmt, params):
    conn = cnxpool.get_connection()
    rows = []
    try:
        cursor = conn.cursor()
        cursor.execute(query_stmt, params)
        rows = cursor.fetchall()
        conn.commit()
    except Error:
        print("Error with sql execution")
    finally:
        cursor.close()
        conn.close()
        return rows


query = ("""SELECT ID FROM MonsterCards.Users
                 WHERE Email = %s;""")

# Input:    Email string, password string
# Changes:  nothing
# Return:   (ID, Email, Password) or None
def get_user(email=None, pw=None, ID=None):
    if (ID == None):
        if (email == None):
            return None
        if (pw == None):
            return None

        user_entry = ("""SELECT ID, Email, Password FROM MonsterCards.Users
                            WHERE Email = %s AND Password = sha2(%s,256);
                            """)
        cursor = db_context.cursor()
        cursor.execute(user_entry, (email, pw))

        user_row = cursor.fetchmany(size=1)
        print(user_row)
        if (len(user_row) != 1):
            return None

        return user_row[0]
    else:

        user_entry = ("""SELECT ID, Email, Password FROM MonsterCards.Users
                            WHERE ID = %s;
                        """);
        cursor = db_context.cursor()
        cursor.execute(user_entry, (ID,))

        user_row = cursor.fetchmany(size=1)
        print(user_row)
        if (len(user_row) != 1):
            return None

        return user_row[0]

def is_valid_token(token):
    curr_date = datetime.now().date()

    query = ("""select count(*) from MonsterCards.UserLogins
                    WHERE AuthToken = %s;""")
    count = execute(query, (token,))[0][0]
    print(count)
    return bool(count)

def get_session_data(token):
    curr_date = datetime.now().date()

    query = """select AccountID
            from MonsterCards.UserLogins
            WHERE AuthToken = %s;"""

    get_user =  """select Email
            from MonsterCards.Users
            where ID = %s;"""
    if (is_valid_token(token)):
        userid = execute(query, (token,))[0][0]
        email = execute(get_user, (userid,))[0][0]
    else:
        raise BadTokenError

    return {"email":email, "userid" : userid, "username" : ""}

def logout_user(token):
    curr_date = datetime.now().date()

    query = ("""
                DELETE FROM MonsterCards.UserLogins
                    WHERE AuthToken = %s;
            """)
    # cursor handles execution sql transactions
    cursor = db_context.cursor()
    cursor.execute("BEGIN;")
    cursor.execute(query, (token,))
    cursor.execute("BEGIN;")
    cursor.close()


def email_taken(email):
    query = """select count(*)
            from MonsterCards.Users
            where Email = %s;"""
    count = execute(query, (email,))[0][0]
    return bool(count)


def valid_creds(email, password):
    query = """select count(*)
        from MonsterCards.Users
        where Email = %s and Password = sha2(%s, 256);"""

    count = execute(query, (email, password))[0][0]
    return bool(count)


def get_userid(email):
    query = """
            select ID
            from MonsterCards.Users
            where Email = %s;"""

    userid = execute(query, (email,))[0][0]
    return userid


def login_user(email, password):
    update_userlogins = """
                        INSERT INTO MonsterCards.UserLogins
                            (AccountID, AuthToken, ExpirationDate)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY 
                            UPDATE AuthToken = %s, ExpirationDate = %s;
                        COMMIT;
                        """

    if (valid_creds(email, password)):
        userid = get_userid(email)
        token = str(uuid.uuid4())
        exp_date = datetime.now() + timedelta(seconds=1800)
        execute(update_userlogins, (userid, token, exp_date, token, exp_date))
        return token
    else:
        raise BadLoginError
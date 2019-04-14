import uuid
from server.dao import cnxpool, execute, SQLExecutionError
from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from datetime import date, datetime, timedelta

_min_pwd_len = 7


class Error(Exception):
    """Base class for other exceptions"""
    pass


class BadEmailError(Error):
    """Raised when email is malformed"""
    pass


class ShortPasswordError(Error):
    """Raised when password is too short"""
    pass


class EmailInUseError(Error):
    """Raised when email is already in use"""
    pass


class BadLoginError(Error):
    """Raised when login credentials are bad"""
    pass


class BadTokenError(Error):
    """Raised when a login token is bad"""
    pass


def signup(email, password):
    query = """
            INSERT INTO MonsterCards.Users (Email, Password)
            VALUES (%s, sha2(%s, 256));
            """

    if (len(str(password)) < _min_pwd_len):
        raise ShortPasswordError
    elif (email_taken(email)):
        raise EmailInUseError
    else:
        user_id = execute(query, (email, password), insert=True)
        return user_id


def get_session_data(token):
    curr_date = datetime.now().date()

    query = """select AccountID
            from MonsterCards.UserLogins
            WHERE AuthToken = %s;"""

    get_user = """select Email
            from MonsterCards.Users
            where ID = %s;"""
    if (is_valid_token(token)):
        userid = execute(query, (token,))[0][0]
        email = execute(get_user, (userid,))[0][0]
    else:
        raise BadTokenError

    return {"email": email, "userid": userid, "username": ""}


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


def login_user(email, password):
    update_userlogins = """
                        INSERT INTO MonsterCards.UserLogins
                            (AccountID, AuthToken, ExpirationDate)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY
                            UPDATE AuthToken = %s, ExpirationDate = %s;
                        """

    if (valid_creds(email, password)):
        userid = get_userid(email)
        token = str(uuid.uuid4())
        exp_date = datetime.now() + timedelta(seconds=1800)
        execute(update_userlogins, (userid, token, exp_date, token, exp_date))
        return token
    else:
        raise BadLoginError


##############################################################################
# Helper Funcs ###############################################################
##############################################################################

def is_valid_token(token):
    curr_date = datetime.now().date()

    query = ("""select count(*) from MonsterCards.UserLogins
                    WHERE AuthToken = %s;""")
    count = execute(query, (token,))[0][0]
    print(count)
    return bool(count)


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

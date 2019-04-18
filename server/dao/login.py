"""
AWB

login.py  Handles all Query Calls to the database for users

"""

import uuid
from server.dao import cnxpool, execute
from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from datetime import date, datetime, timedelta
from validate_email import validate_email
from server.exceptions import exceptions

# global min password length
_min_pwd_len = 7

"""
Function creates a user
"""
def signup(username, email, password):
    query = """
            INSERT INTO MonsterCards.Users (Email, Password, Username)
            VALUES (%s, sha2(%s, 256), %s);
            """

    if (len(str(password)) < _min_pwd_len):
        raise ShortPasswordError
    elif (username_taken(username)):
        raise UsernameInUseError
    elif (email_taken(email)):
        raise EmailInUseError
    elif (not validate_email(email)):
        raise BadEmailError
    else:
        execute(query, (email, password, username))


"""
Function changes a users password
"""
def change_password(username, email, password):
    query = """
        update MonsterCards.Users
        SET Password = sha2(%s, 256)
        WHERE UserName = %s and Email = %s;
        """

    if (len(str(password)) < _min_pwd_len):
        raise ShortPasswordError
    else:
        execute(query, (password, username, email))


"""
Function changes a users email
"""
def change_email(username, email):
    query = """
        update MonsterCards.Users
        SET Email = %s
        WHERE UserName = %s;
        """
    if (email_taken(email)):
        raise EmailInUseError
    elif (not validate_email(email)):
        raise BadEmailError
    else:
        user_id = execute(query, (email, username))


"""
Function changes a users username
"""
def change_username(username, email):
    query = """
        update MonsterCards.Users
        SET UserName = %s
        WHERE Email = %s;
        """

    if (username_taken(email)):
        raise UsernameInUseError
    else:
        user_id = execute(query, (username, email))


"""
Function gets a users session data
"""
def get_session_data(token):
    curr_date = datetime.now().date()

    query = """select AccountID
            from MonsterCards.UserLogins
            WHERE AuthToken = %s;"""

    get_user = """select Email
            from MonsterCards.Users
            where ID = %s;"""

    get_name = """ select UserName
            from MonsterCards.Users
            where ID = %s;"""

    if (is_valid_token(token)):
        userid = execute(query, (token,))[0][0]
        email = execute(get_user, (userid,))[0][0]
        username = execute(get_name, (userid,))[0][0]
    else:
        raise BadTokenError

    return {"email":email, "userid" : userid, "username" : username}


"""
Function logs a user out
"""
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


"""
Function gets a player's deck based on their ID
"""
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
        print("Right after: " + token)
        return token
    else:
        raise BadLoginError


"""
Function checks if login token is valid
"""
def is_valid_token(token):
    curr_date = datetime.now().date()
    query = """select count(*) from MonsterCards.UserLogins
                    WHERE AuthToken = %s;"""

    count = execute(query, (token,))[0][0]
    print(count)
    return bool(count)


"""
Function checks if the email is in use by another user
"""
def email_taken(email):
    query = """select count(*)
            from MonsterCards.Users
            where Email = %s;"""

    count = execute(query, (email,))[0][0]
    return bool(count)


"""
Function checks if the username is in use by another user
"""
def username_taken(username):
    query = """select count(*)
            from MonsterCards.Users
            where Username = %s;"""

    count = execute(query, (username,))[0][0]
    return bool(count)


"""
Function checks the credentials of a user (login)
"""
def valid_creds(email, password):
    query = """select count(*)
        from MonsterCards.Users
        where Email = %s and Password = sha2(%s, 256);"""

    count = execute(query, (email, password))[0][0]
    return bool(count)


"""
Function gets a user, userid
"""
def get_userid(email):
    query = """
            select ID
            from MonsterCards.Users
            where Email = %s;"""

    userid = execute(query, (email,))[0][0]
    return userid

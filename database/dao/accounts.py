"""login.py  Handles all Query Calls to the database for users"""

import uuid
from . import cnxpool, execute
from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from datetime import date, datetime, timedelta
from validate_email import validate_email
from server.exceptions import (UsernameInUseError, BadTokenError, Error,
                               BadLoginError, EmailInUseError,
                               ShortPasswordError, BadEmailError)


# global min password length
_min_pwd_len = 7


def signup(username, email, password):
    """Function creates a user"""

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


def change_password(username, email, password):
    """Function changes a users password"""
    query = """
        update MonsterCards.Users
        SET Password = sha2(%s, 256)
        WHERE UserName = %s and Email = %s;
        """

    if (len(str(password)) < _min_pwd_len):
        raise ShortPasswordError
    else:
        execute(query, (password, username, email))


def change_email(username, email):
    """Function changes a users email"""

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
        execute(query, (email, username))


def change_username(username, email):
    """Function changes a users username"""

    query = """
        update MonsterCards.Users
        SET UserName = %s
        WHERE Email = %s;
        """

    if (username_taken(email)):
        raise UsernameInUseError
    else:
        execute(query, (username, email))


def get_session_data(token):
    """Function gets a users session data"""

    # curr_date = datetime.now().date()

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

    return {"email": email, "userid": userid, "username": username}


def logout_user(token):
    """Function logs a user out"""

    # curr_date = datetime.now().date()

    query = ("""
                DELETE FROM MonsterCards.UserLogins
                    WHERE AuthToken = %s;
            """)

    execute(query, ())


def login_user(email, password):
    """Function gets a player's deck based on their ID"""

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


def is_valid_token(token):
    """Function checks if login token is valid"""

    # curr_date = datetime.now().date()

    query = """select count(*) from MonsterCards.UserLogins
                    WHERE AuthToken = %s;"""

    count = execute(query, (token,))[0][0]
    return bool(count)


def email_taken(email):
    """Function checks if the email is in use by another user"""

    query = """select count(*)
            from MonsterCards.Users
            where Email = %s;"""

    count = execute(query, (email,))[0][0]
    return bool(count)


def username_taken(username):
    """Function checks if the username is in use by another user"""

    query = """select count(*)
            from MonsterCards.Users
            where Username = %s;"""

    count = execute(query, (username,))[0][0]
    return bool(count)


def valid_creds(email, password):
    """Function checks the credentials of a user (login)"""

    query = """select count(*)
        from MonsterCards.Users
        where Email = %s and Password = sha2(%s, 256);"""

    count = execute(query, (email, password))[0][0]
    return bool(count)


def get_userid(email):
    """Function gets a user, userid"""

    query = """
            select ID
            from MonsterCards.Users
            where Email = %s;"""

    userid = execute(query, (email,))[0][0]
    return userid

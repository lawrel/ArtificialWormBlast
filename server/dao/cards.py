import sys
import uuid
from server.dao import cnxpool, execute
from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from datetime import date, datetime, timedelta
from mysql.connector.errors import Error


# class Error(Exception):
#     """Base class for other exceptions"""
#     pass


class NoFileUploadedError(Error):
    pass


class EmptyFileError(Error):
    pass


class FileTooLargeError(Error):
    pass


class BadFileExtError(Error):
    pass


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def new_card(file, attrs=None):
    insert_blob = """
                    INSERT INTO MonsterCards.Cards
                        (ImgData, Attributes)
                    VALUES (%s,%s);"""
    pic_bin = file.read()

    card_id = execute(insert_blob, (pic_bin, attrs), insert=True)[0][0]
    return card_id


def edit_card(card_id, file, attrs=None):
    insert_blob = """
                    update MonsterCards.Cards
                    set ImgData = %s, Attributes = %s
                    where ID = %s;"""
    pic_bin = file.read()

    card_id = execute(insert_blob, (pic_bin, attrs, card_id), insert=True)[0][0]
    return card_id


def get_card(card_id):
    query = """
            select ID, ImgData, Attributes
            from MonsterCards.Cards
            where ID = %s;
            """

    card = execute(query, (card_id, ))[0]
    return card

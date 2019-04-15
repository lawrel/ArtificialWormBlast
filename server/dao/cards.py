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


def getPlayerDeck(playerId):
    query = """
            select CardID, Name, Attributes from MonsterCards.UserCards
            inner join MonsterCards.Cards
            on CardID = ID
            where UserID = %s;
            """
    cards = execute(query, (playerId, ))
    dict_cards = []
    for card_id, card_name, card_attr in cards:
        card = {
            "id": card_id,
            "name": card_name,
            "attr": card_attr
        }
        dict_cards.append(card)
    return dict_cards


def getSiteDeck():
    query = """
            select ID, Name, Attributes from MonsterCards.Cards
            where ID > 0 and ID <= 18;
            """
    cards = execute(query, ())
    dict_cards = []
    for card_id, card_name, card_attr in cards:
        card = {
            "id": card_id,
            "name": card_name,
            "attr": card_attr
        }
        dict_cards.append(card)
    return dict_cards


def addPlayerCard(playerId, cardId):
    query = """
            INSERT INTO MonsterCards.UserCards (UserID, CardID) VALUES (%s, %s);
            """
    execute(query, (playerId, cardId))


def remove_player_card(player_id, card_id):
    query = """
            delete from MonsterCards.UserCards
            where CardID = %s and UserID = %s;
            """
    execute(query, (card_id, player_id))


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def new_card(pic_bin, attrs=None, name=None):
    insert_blob = """
                    INSERT INTO MonsterCards.Cards
                        (Name, ImgData, Attributes)
                    VALUES (%s, %s, %s);"""
    print(type(pic_bin))
    card_id = execute(insert_blob, (name, pic_bin, attrs), insert=True)[0][0]
    return card_id


def edit_card(card_id, pic_bin, attrs=None, name=None):
    if (name is None):
        insert_blob = """
                    update MonsterCards.Cards
                    set ImgData = %s, Attributes = %s
                    where ID = %s;"""
        card_id = execute(insert_blob, (pic_bin, attrs, card_id), insert=True)[0][0]
        return card_id
    else:
        insert_blob = """
                    update MonsterCards.Cards
                    set Name = %s, ImgData = %s, Attributes = %s
                    where ID = %s;"""
        card_id = execute(insert_blob, (name, pic_bin, attrs, card_id), insert=True)[0][0]
        return card_id


def get_card(card_id):
    query = """
            select ID, Name, ImgData, Attributes
            from MonsterCards.Cards
            where ID = %s;
            """

    card = execute(query, (card_id, ))[0]
    return card

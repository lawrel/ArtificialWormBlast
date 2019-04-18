"""
AWB

cards.py Handles all Query Calls to the database for cards 

"""

import sys
import uuid
from server.dao import cnxpool, execute
from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from datetime import date, datetime, timedelta
from mysql.connector.errors import Error


"""
Function gets a player's deck based on their ID
"""
def get_player_deck(playerId):
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


"""
Function gets the site's deck
"""
def get_site_deck():
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


"""
Function adds a card to a player's deck
"""
def add_player_card(playerId, cardId):
    query = """
            INSERT INTO MonsterCards.UserCards (UserID, CardID) VALUES (%s, %s);
            """
    execute(query, (playerId, cardId))


"""
Function removes a card from a player's deck
"""
def remove_player_card(player_id, card_id):
    query = """
            delete from MonsterCards.UserCards
            where CardID = %s and UserID = %s;
            """
    execute(query, (card_id, player_id))


"""
Function converts a file to binary data for storage
"""
def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


"""
Function creates a new card
"""
def new_card(pic_bin, attrs=None, name=None):
    insert_blob = """
                    INSERT INTO MonsterCards.Cards
                        (Name, ImgData, Attributes)
                    VALUES (%s, %s, %s);"""
    print(type(pic_bin))
    card_id = execute(insert_blob, (name, pic_bin, attrs), insert=True)[0][0]
    return card_id


"""
Function edits an existing card
"""
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


"""
Function gets a card
"""
def get_card(card_id):
    query = """
            select ID, Name, ImgData, Attributes
            from MonsterCards.Cards
            where ID = %s;
            """

    card = execute(query, (card_id, ))[0]
    return card

"""
AWB

player.py is the Player object in which
who plays a game

"""

from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio


"""
Class is the player, which is the user 
playing a game
"""
class Player:
    def __init__(self, userid, username, email):
        self.userid = userid
        self.username = username
        self.email = email
        self.vote = False
        self.vote_card = None
        self.numVotes = 0
        self.hand = []


    """
    Function serialized data
    """
    def serialize(self):
        return {
            "userid" : self.userid,
            "username" : self.username,
            "email" : self.email,
            "hand" : self.hand,
            "vote" : self.vote,
            "numVotes" : self.numVotes
        }
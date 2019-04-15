from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio

class GameList:
    def __init__(self):
        self.publicGames = {}
        self.privateGames = {}

    def getGame(self, gameid):
        return gameid
    
    def checkIfFull():

    def newPublic():

    def newPrivate():
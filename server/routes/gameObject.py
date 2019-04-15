from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio

class Game:
    def __init__(self):
        self.gameid = str(uuid.uuid4())
        self.public = True
        self.players = {}
        self.state = None
        self.round = 0
        self.attacker = None
        self.defender = None
        self.atk_card = None
        self.dfs_card = None
        self.winner = None
        self.newRound = None
        self.endgame = False
        self.endrule = 0
        self.set_state(WaitState(self))

    def new_round(self):
        self.attacker = None
        self.defender = None
        self.atk_card = None
        self.dfs_card = None
        self.winner = None
        self.round += 1
        for playerid, player in self.players.items():
            player.vote = False
            player.vote_card = None

    def swap_card(self, card, loserid, winnerid):
        loser = self.players[loserid]
        winner = self.players[winnerid]
        print(loser.hand)
        loser.hand.remove(card)
        winner.hand.append(card)
        self.update_clients()

    def check_end(self, winner, loser):
        if (self.endrule == 0 and loser.hand.length == 0):
            self.endgame = True
        elif (self.endrule > 0 and winner.hand.length >= self.endrule):
            self.endgame = True

    def addPlayer(self, player):
        self.players[player.userid] = player
        self.update()

    def set_player_hand(self, playerid, hand):
        if (playerid in self.players):
            self.players[playerid].hand = hand
            self.state.handle()

    def update(self):
        self.state.handle()
        self.update_clients()

    def set_state(self, state):
        self.state = state
        self.update()

    def vote(self, userid, card):
        self.players[userid].vote_card = card
        self.players[userid].vote = True
        self.update()

    def update_clients(self):
        socketio.emit('game-data', self.serialize(), room=self.gameid)

    def serialize(self):
        playersData = [player.serialize() for playerid, player in self.players.items()]
        gameData = {
                "gameid" : self.gameid,
                "public" : self.public,
                "players" : playersData,
                "state" : self.state.__str__(),
                "round" : self.round,
                "attacker": self.attacker,
                "atk_card": self.atk_card,
                "defender":self.defender,
                "dfs_card":self.dfs_card,
                "winner":self.winner,
                "endgame":self.endgame,
                "endrule":self.endrule,
                "newRound":self.newRound
            }
        return gameData


gameLst = {}

@app.route("/chat-ex")
def chat_ex():
    return render_template("chatRoomEx.html")
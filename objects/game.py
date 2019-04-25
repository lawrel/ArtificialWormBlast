"""
AWB

game.py is the Game object which is
the basis of our project

"""

from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio
from objects.player import Player
from objects.states import (GameState, WaitState, SelectHandState,
                            NewRoundState, AttackState, DefendState,
                            VoteState, WinnerState, EndState)

# Gloab States
currState = None
prevState = None


class Game:
    """Class is the Game class which manages its States and players along with
    the cards.
    """

    def __init__(self, public, maxplayers, endrule):
        self.gameid = str(uuid.uuid4())
        self.public = True
        self.maxplayers = 0
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

    def gameStatus(self):
        """Function gets game status on if it is open to join"""

        if (self.public and self.maxplayers < len(self.players) and
                WaitState != self.state.__str__()):
            return True
        else:
            return False

    def getSelf(self):
        """Function gets itself"""

        return self

    def new_round(self):
        """Function resets the round"""

        self.attacker = None
        self.defender = None
        self.atk_card = None
        self.dfs_card = None
        self.winner = None
        self.round += 1
        for _, player in self.players.items():
            player.vote = False
            player.vote_card = None

    def swap_card(self, card, loserid, winnerid):
        """Function swaps card of winner and loser"""

        loser = self.players[loserid]
        winner = self.players[winnerid]
        card_data = loser.hand.pop(card)
        winner.hand[card] = card_data
        self.update_clients()

    def check_end(self, winner, loser):
        """Function checks if end of game"""

        if (self.endrule == 0 and len(self.players[loser].hand) == 0):
            self.endgame = True
        elif (self.endrule > 0 and
              len(self.players[winner].hand) >= self.endrule):
            self.endgame = True

    def addPlayer(self, player):
        """Function adds player to game"""

        self.players[player.userid] = player
        self.update()

    def set_player_hand(self, playerid, hand):
        """Function sets a players hand"""

        if (playerid in self.players):
            self.players[playerid].hand = hand
            self.state.handle()

    def update(self):
        """Function updates the states and players"""

        self.state.handle()
        self.update_clients()

    def set_state(self, state):
        """Function sets the state"""

        self.state = state
        self.update()

    def vote(self, userid, card):
        """Function adds a players vote"""

        self.players[userid].vote_card = card
        self.players[userid].vote = True
        self.update()

    def update_clients(self):
        """Function updates clients/players on actions"""

        socketio.emit('game-data', self.serialize(), room=self.gameid)

    def serialize(self):
        """Function serialized data"""

        playersData = [player.serialize()
                       for playerid, player in self.players.items()]

        gameData = {
                "gameid": self.gameid,
                "public": self.public,
                "maxplayers": self.maxplayers,
                "players": playersData,
                "state": self.state.__str__(),
                "round": self.round,
                "attacker": self.attacker,
                "atk_card": self.atk_card,
                "defender": self.defender,
                "dfs_card": self.dfs_card,
                "winner": self.winner,
                "endgame": self.endgame,
                "endrule": self.endrule,
                "newRound": self.newRound
            }
        return gameData

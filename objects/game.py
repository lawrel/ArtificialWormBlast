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
from objects.states import GameState, WaitState, SelectHandState, NewRoundState, AttackState, DefendState, VoteState, WinnerState, EndState

## Gloab States
currState = None
prevState = None


"""
Class is the Game class which manages its
States and players along with the cards
"""
class Game:
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

    """
    Function gets game status on if it is open to join
    """
    def gameStatus(self):
        if (self.public and self.maxplayers < len(self.players) and WaitState != self.state.__str__()):
            return True
        else:
            return False


    """
    Function gets itself
    """
    def getSelf(self):
        return self


    """
    Function resets the round
    """
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


    """
    Function swaps card of winner and loser
    """
    def swap_card(self, card, loserid, winnerid):
        loser = self.players[loserid]
        winner = self.players[winnerid]
        print(loser.hand)
        l_card_name = loser.hand.pop(card)
        self.players[winnerid].edit_card(l_card_name)
        winner.hand[card] = l_card_name
        self.update_clients()


    """
    Function checks if end of game
    """
    def check_end(self, winner, loser):
        if (self.endrule == 0 and len(self.players[loser].hand) == 0):
            self.endgame = True
        elif (self.endrule > 0 and len(self.players[winner].hand) >= self.endrule):
            self.endgame = True


    """
    Function adds player to game
    """
    def addPlayer(self, player):
        self.players[player.userid] = player
        self.update()


    """
    Function sets a players hand
    """
    def set_player_hand(self, playerid, hand):
        if (playerid in self.players):
            self.players[playerid].hand = hand
            self.state.handle()


    """
    Function updates the states and players
    """
    def update(self):
        self.state.handle()
        self.update_clients()


    """
    Function sets the state
    """
    def set_state(self, state):
        self.state = state
        self.update()


    """
    Function adds a players vote
    """
    def vote(self, userid, card):
        self.players[userid].vote_card = card
        self.players[userid].vote = True
        self.update()


    """
    Function updates clients/players on actions
    """
    def update_clients(self):
        socketio.emit('game-data', self.serialize(), room=self.gameid)


    """
    Function serialized data
    """
    def serialize(self):
        playersData = [player.serialize() for playerid, player in self.players.items()]
        gameData = {
                "gameid" : self.gameid,
                "public" : self.public,
                "maxplayers":self.maxplayers,
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

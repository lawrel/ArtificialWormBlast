from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio
from server.routes.playerObject import Player


class GameState:
    def __init__(self):
        pass

    def handle(self, context):
        pass

    def next_state(self, context):
        pass

class WaitState(GameState):
    def __init__(self, context):
        print("Waiting for players to connect...")
        self.context = context
        self.timer = Timer(5, self.next_state)

    def handle(self):
        if (len(self.context.players) == 6):
            print("All players connected.")
            self.next_state()
        elif (len(self.context.players) >= 2 and not self.timer.is_alive()):
            print("Game begins in 60 seconds.")
            self.timer.start()
        elif(len(self.context.players) < 3 and self.timer.is_alive()):
            print("Aborting countdown.")
            self.timer.cancel()
            self.timer = Timer(5, self.next_state)

    def next_state(self):
        self.context.set_state(SelectHandState(self.context))

    def __str__(self):
        return "WaitState"

class SelectHandState(GameState):
    def __init__(self, context):
        print("Waiting for players to select hand...")
        self.context = context

    def handle(self):
        playerReady = [len(player.hand) == 5 for playerid, player in self.context.players.items()]
        if (False not in playerReady):
            self.next_state()

    def next_state(self):
        self.context.set_state(NewRoundState(self.context))

    def __str__(self):
        return "SelectHandState"

class NewRoundState(GameState):
    def __init__(self, context):
        print("Starting new round")
        self.context = context

    def handle(self):
        self.context.new_round()
        self.next_state()

    def next_state(self):
        self.context.set_state(AttackState(self.context))

class AttackState(GameState):
    def __init__(self, context):
        print("Attacker select an opponent and a card.")
        self.context = context
        ps = list(context.players)
        self.context.attacker = random.choice(ps)
        #self.context.update_clients()
    
    def handle(self):
        if (self.context.defender is not None and self.context.atk_card is not None):
            self.next_state()

    def next_state(self):
        self.context.update_clients()
        self.context.set_state(DefendState(self.context))

    def __str__(self):
        return "AttackState"

class DefendState(GameState):
    def __init__(self, context):
        print("Defender select a card.")
        self.context = context
    
    def handle(self):
        if (self.context.dfs_card is not None):
            self.next_state()

    def next_state(self):
        self.context.set_state(VoteState(self.context))

    def __str__(self):
        return "DefendState" 

class VoteState(GameState):
    def __init__(self, context):
        print("Vote on the winner.")
        self.context = context
    
    def handle(self):
        playerVoted = [player.vote for playerid, player in self.context.players.items()]
        if (False not in playerVoted):
            self.next_state()

    def next_state(self):
        self.context.set_state(WinnerState(self.context))

    def __str__(self):
        return "VoteState"

class WinnerState(GameState):
    def __init__(self, context):
        print("Announce the winner, give winner card, remove loser card.")
        self.context = context
    
    def handle(self):
        votelist = [player.vote for playerid, player in self.context.players.items()]
        atk_cnt = 0
        dfs_cnt = 0
        for v in votelist:
            if (v == self.context.atk_card):
                atk_cnt += 1
            if (v == self.context.dfs_card):
                dfs_cnt += 1

        if (dfs_cnt >= atk_cnt):
            self.context.winner = self.context.defender
        else:
            self.context.winner = self.context.attacker

        winner = None
        loser = None
        card = None
        if (self.context.winner == self.context.defender):
            card = self.context.atk_card
            winner = self.context.defender
            loser = self.context.attacker
        else:
            card = self.context.dfs_card
            winner = self.context.attacker
            loser = self.context.defender

        self.context.swap_card(card, loser, winner)
        self.context.check_end(loser)
        self.next_state()

    def next_state(self):
        if (self.context.endgame):
            self.context.set_state(EndState(self.context))
        else:
            self.context.set_state(NewRoundState(self.context))

    def __str__(self):
        return "WinnerState"

class EndState(GameState):
    def __init__(self, context):
        print("Finish the game.")
        self.context = context

    def handle(self):
        pass

    def next_state(self):
        pass

    def __str__(self):
        return "EndState"
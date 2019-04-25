"""states.py holds all state objects
(from the abstract GameState to each indivdual state)
"""


from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio
from objects.player import Player


class GameState:
    """Class is the abstract class for each state which is a specific part of the
    round of a game.
    """

    def __init__(self):
        pass

    def handle(self, context):
        pass

    def next_state(self, context):
        pass


class WaitState(GameState):
    """Class is the wait state, waiting for player to connect to the game"""

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
    """Class is the select hand state, where players select their hand"""

    def __init__(self, context):
        print("Waiting for players to select hand...")
        self.context = context

    def handle(self):
        playerReady = [len(player.hand) == 5 for playerid, player
                       in self.context.players.items()]
        if (False not in playerReady):
            self.next_state()

    def next_state(self):
        self.context.set_state(NewRoundState(self.context))

    def __str__(self):
        return "SelectHandState"


class NewRoundState(GameState):
    """Class is the new round state, where a new round is initialized"""

    def __init__(self, context):
        print("Starting new round")
        self.context = context

    def handle(self):
        self.context.new_round()
        self.next_state()

    def next_state(self):
        self.context.set_state(AttackState(self.context))


class AttackState(GameState):
    """Class is the attact state, where anattacker chooses a target and a
    card
    """

    def __init__(self, context):
        print("Attacker select an opponent and a card.")
        self.context = context
        ps = list(context.players)
        self.context.attacker = random.choice(ps)

    def handle(self):
        if (self.context.defender is not None and
                self.context.atk_card is not None):
            self.next_state()

    def next_state(self):
        self.context.update_clients()
        self.context.set_state(DefendState(self.context))

    def __str__(self):
        return "AttackState"


class DefendState(GameState):
    """Class is the defend state, where the defender chooses a card to fight
    back with
    """

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
    """Class is the vote state, where players vote for the winning card"""

    def __init__(self, context):
        print("Vote on the winner.")
        self.context = context

    def handle(self):
        playerVoted = [player.vote for playerid, player
                       in self.context.players.items()]
        if (False not in playerVoted):
            self.next_state()

    def next_state(self):
        self.context.set_state(WinnerState(self.context))

    def __str__(self):
        return "VoteState"


class WinnerState(GameState):
    """Class is the winning state, where the winner is determined and card
    swaps occur
    """

    def __init__(self, context):
        print("Announce the winner, give winner card, remove loser card.")
        self.context = context

    def handle(self):
        votelist = [player.vote_card for playerid, player
                    in self.context.players.items()]
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
        self.context.check_end(winner, loser)
        self.next_state()

    def next_state(self):
        if (self.context.endgame):
            self.context.set_state(EndState(self.context))
        else:
            self.context.set_state(NewRoundState(self.context))

    def __str__(self):
        return "WinnerState"


class EndState(GameState):
    """Class is the end state, marking the end of the game"""

    def __init__(self, context):
        print("Finish the game.")
        self.context = context

    def handle(self):
        pass

    def next_state(self):
        pass

    def __str__(self):
        return "EndState"

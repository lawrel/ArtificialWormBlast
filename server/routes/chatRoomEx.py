from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio

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
        self.next_state()

    def next_state(self):
        if (self.context.round == 3):
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
        self.set_state(WaitState(self))

    def new_round(self):
        self.attacker = None
        self.defender = None
        self.atk_card = None
        self.dfs_card = None
        self.winner = None
        self.round += 1
        for playerid, player in self.players.items():
            print(playerid)
            print(player)
            player.vote = False
            player.vote_card = None

    def swap_card(self, card, loserid, winnerid):
        loser = self.players[loserid]
        winner = self.players[winnerid]
        print(loser.hand)
        loser.hand.remove(card)
        winner.hand.append(card)
        self.update_clients()

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
                "newRound":self.newRound
            }
        return gameData

class Player:
    def __init__(self, userid, username, email):
        self.userid = userid
        self.username = username
        self.email = email
        self.vote = False
        self.vote_card = None
        self.numVotes = 0
        self.hand = []


    def serialize(self):
        return {
            "userid" : self.userid,
            "username" : self.username,
            "email" : self.email,
            "hand" : self.hand,
            "vote" : self.vote,
            "numVotes" : self.numVotes
        }

gameLst = {}

@app.route("/chat-ex")
def chat_ex():
    return render_template("chatRoomEx.html")

@socketio.on('player-data')
def player_data(msg):
    if ("player" in msg):
        if ("userid" in msg["player"]):
            for gameid, game in gameLst.items():
                if (msg["player"]["userid"] in game.players):
                    print(request.sid)
                    emit('player-data', game.serialize(),room=request.sid)
                    break

@socketio.on('player-hand')
def player_hand(msg):
    gameid = msg['gameid']
    userid = msg['userid']
    hand = msg['hand']

    gameLst[gameid].set_player_hand(userid, hand)

@socketio.on('create-game')
def createGame(data):
    username = data['player']['username']
    email = data['player']['email']
    userid = data['player']['userid']
    player = Player(userid, username, email)

    game = Game()
    gameLst[game.gameid] = game
    data['gameid'] = game.gameid
    joinGame(data)
    send(game.gameid, room=game.gameid)

@socketio.on('join-game')
def joinGame(data):
    print(request.sid, "Wants to join")
    username = data['player']['username']
    email = data['player']['email']
    userid = data['player']['userid']
    gameid = data['gameid']
    player = Player(userid, username, email)
    if(gameid in gameLst):
        if(player.userid in gameLst[gameid].players):
            emit('join-game', {"status":"success", "reason":"You are already in this game", "gameid": gameid}, room=request.sid)
            join_room(gameid)
            return
        else:
            join_room(gameid)
            gameLst[gameid].addPlayer(player)
            emit('join-game', {"status":"success", "gameid": gameid}, room=request.sid)
    else:
        print("Not a valid gameid: " + gameid)
        emit('join-game', {"status":"failure", "reason":"Not a valid gameid"}, room=request.sid)
        return

#############################################################################

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('game-data')
def give_data(msg):
    gameid = msg["gameid"]
    if (gameid in gameLst):
        print(request.sid)
        emit('game-data', gameLst[gameid].serialize(),room=request.sid)

@socketio.on('atk-card-update')
def atk_card(msg):
    gameid = msg["gameid"]
    card = msg["card"]
    gameLst[gameid].atk_card = card
    gameLst[gameid].update()
    print(gameLst[gameid].serialize())
    # emit('atk-card-update', {"card":card}, room=gameid)

@socketio.on('dfs-card-update')
def dfs_card(msg):
    gameid = msg["gameid"]
    card = msg["card"]
    gameLst[gameid].dfs_card = card
    gameLst[gameid].update()
    print(gameLst[gameid].serialize())
    # emit('dfs-card-update', {"card":card}, room=gameid)

@socketio.on("set-defender")
def set_defender(msg):
    gameid = msg["gameid"]
    userid = msg["userid"]
    gameLst[gameid].defender = int(userid)
    gameLst[gameid].update()
    print(gameLst[gameid].serialize())

# @socketio.on("round-winner")
# def set_winner(msg):
#     print("HERRO")
#     print(msg)
#     gameid = msg["gameid"]
#     userid = msg["userid"]
#     gameLst[gameid].winner = int(userid)
#     gameLst[gameid].update()
#     print(gameLst[gameid].serialize())

# @socketio.on("new_Round")
# def set_winner(msg):
#     print("HERRO2")
#     print(msg)
#     gameid = msg["gameid"]
#     newRound = "here"
#     gameLst[gameid].update()
#     print(gameLst[gameid].serialize())

@socketio.on('submit-vote')
def reg_vote(msg):
    userid = msg["userid"]
    card = msg["card"]
    gameid = msg["gameid"]

    gameLst[gameid].vote(userid, card)

from threading import Timer
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
        if (len(self.context.players) == 5):
            print("All players connected.")
            self.next_state()
        elif (len(self.context.players) >= 3 and not self.timer.is_alive()):
            print("Game begins in 60 seconds.")
            self.timer.start()
        elif(len(self.context.players) < 3 and self.timer.is_alive()):
            print("Aborting countdown.")
            self.timer.cancel()
            self.timer = Timer(5, self.next_state)

    def next_state(self):
        self.context.set_state(SelectHandState(self.context))

    def __str__(self):
        return "Wait"

class SelectHandState(GameState):
    def __init__(self, context):
        print("Waiting for players to select hand...")
        self.context = context

    def handle(self):
        playerReady = [len(player.hand) == 5 for playerid, player in self.context.players.items()]
        if (False not in playerReady):
            self.next_state()

    def next_state(self):
        pass

    def __str__(self):
        return "SelectHand"

class Game:
    def __init__(self):
        self.gameid = str(uuid.uuid4())
        self.public = True
        self.players = {}
        self.state = None
        self.round = 0

        self.set_state(WaitState(self))

    def addPlayer(self, player):
        self.players[player.userid] = player
        self.update()

    def update(self):
        self.state.handle()
        self.update_clients()

    def set_state(self, state):
        self.state = state
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
                "round" : self.round
            }
        return gameData

class Player:
    def __init__(self, userid, username, email):
        self.userid = userid
        self.username = username
        self.email = email
        self.hand = []

    def serialize(self):
        return {
            "userid" : self.userid,
            "username" : self.username,
            "email" : self.email,
            "hand" : self.hand
        }

gameLst = {}

@app.route("/chat-ex")
def chat_ex():
    return render_template("chatRoomEx.html")

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
    username = data['player']['username']
    email = data['player']['email']
    userid = data['player']['userid']
    gameid = data['gameid']
    player = Player(userid, username, email)
    if(gameid in gameLst):
        if(player.userid in gameLst[gameid].players):
            emit('join-game', {"status":"failure", "reason":"You are already in this game"}, room=request.sid)
            return
        else:
            join_room(gameid)
            gameLst[gameid].addPlayer(player)
            emit('join-game', {"status":"success"}, room=request.sid)
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
    player = msg["player"]
    for gameid, game in gameLst.items():
        if (player["userid"] in game.players):
            print(request.sid)
            emit('game-data', game.serialize(),room=request.sid)
            break

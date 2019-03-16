import uuid
from flask import render_template, request
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio

class Game:
    def __init__(self):
        self.gameid = str(uuid.uuid4())
        self.public = True
        self.players = []
        self.state = None
        self.round = 0

    def addPlayer(self, player):
        self.players.append(player)

class Player:
    def __init__(self, userid, username, email):
        self.userid = userid
        self.username = username
        self.email = email

gameLst = {}

@app.route("/chat-ex")
def chat_ex():
    return render_template("chatRoomEx.html")

@socketio.on('create-game')
def create_game(data):
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
        gameLst[gameid].addPlayer(player)
    else:
        print("Not a valid gameid: " + gameid)
        send("Not a valid gameid: " + gameid, room=request.sid)
        return
    join_room(gameid)
    send(username + ' has entered the room.', room=gameid)

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

import uuid
from flask import render_template
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio

class Game:
    def __init__(self):
        self.gameid = str(uuid.uuid4())
        self.public = True
        self.players = []

        self.state = None
        self.round = 0

    def join_game(self, userid):
        self.players.append(userid)

class Player:
    def __init__(self, userid):
        self.userid = userid
        self.username = None
        self.email = None

games = {}

@app.route("/chat-ex")
def chat_ex():
    return render_template("chatRoomEx.html")

@socketio.on('join')
def on_join(data):
    print(data)
    username = data['player']['username']
    email = data['player']['email']
    userid = data['player']['userid']

    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('create-game')
def create_game(message):
    username = data['player']['username']
    email = data['player']['email']
    userid = data['player']['userid']

    game = Game()
    games[game.gameid] = game
    send()
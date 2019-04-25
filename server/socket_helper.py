"""socket_helper.py Handles all of the socket operations"""


from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio
from objects.game import Game
from objects.player import Player
from objects.states import (GameState, WaitState, SelectHandState,
                            NewRoundState, AttackState, DefendState,
                            VoteState, WinnerState, EndState)


# List of all active games
gameLst = {}


@socketio.on('player-data')
def player_data(msg):
    """Socker for player data"""

    if ("player" in msg):
        if ("userid" in msg["player"]):
            for _, game in gameLst.items():
                if (msg["player"]["userid"] in game.players):
                    emit('player-data', game.serialize(), room=request.sid)
                    break


@socketio.on('player-hand')
def player_hand(msg):
    """Socket for player hand"""

    gameid = msg['gameid']
    userid = msg['userid']
    hand = msg['hand']
    gameLst[gameid].set_player_hand(userid, hand)


@socketio.on('check-games')
def checkGames(data):
    """Socket for checking games"""

    # username = data['player']['username']
    # email = data['player']['email']
    # userid = data['player']['userid']
    # player = Player(userid, username, email)

    # game is running
    for gameid, game in gameLst.items():
        if (game.gameStatus()):
            data['gameid'] = gameid
            joinGame(data)
            send(gameid, room=gameid)
            return game.gameid

    # no games running, make new game
    game = Game(True, 5, 0)
    gameLst[game.gameid] = game
    data['gameid'] = game.gameid
    joinGame(data)
    send(game.gameid, room=game.gameid)
    return game.gameid


@socketio.on('create-game')
def createGame(data):
    """Socket for creating (Private) game"""

    # username = data['player']['username']
    # email = data['player']['email']
    # userid = data['player']['userid']
    # player = Player(userid, username, email)

    cards = data['cards']
    maxplayers = data['players']

    game = Game(False, cards, maxplayers)
    gameLst[game.gameid] = game
    data['gameid'] = game.gameid
    joinGame(data)
    send(game.gameid, room=game.gameid)
    return game.gameid


@socketio.on('join-game')
def joinGame(data):
    """Socket to join game"""

    print(request.sid, "Wants to join")
    username = data['player']['username']
    email = data['player']['email']
    userid = data['player']['userid']
    gameid = data['gameid']
    player = Player(userid, username, email)
    if(gameid in gameLst):
        if(player.userid in gameLst[gameid].players):
            emit('join-game', {"status": "success",
                               "reason": "You are already in this game",
                               "gameid": gameid},
                 room=request.sid)
            join_room(gameid)
            return
        else:
            join_room(gameid)
            gameLst[gameid].addPlayer(player)
            emit('join-game', {"status": "success", "gameid": gameid},
                 room=request.sid)
    else:
        print("Not a valid gameid: " + gameid)
        emit('join-game', {"status": "failure",
                           "reason": "Not a valid gameid"}, room=request.sid)
        return


@socketio.on('leave')
def on_leave(data):
    """Socket to leave"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


@socketio.on('message')
def handle_message(message):
    """Socket to message"""

    print('received message: ' + message)


@socketio.on('game-data')
def give_data(msg):
    """Socket for game data"""

    gameid = msg["gameid"]
    if (gameid in gameLst):
        print(request.sid)
        emit('game-data', gameLst[gameid].serialize(), room=request.sid)


@socketio.on('atk-card-update')
def atk_card(msg):
    """Socket for attacking card update"""

    gameid = msg["gameid"]
    card = msg["card"]
    gameLst[gameid].atk_card = card
    gameLst[gameid].update()
    print(gameLst[gameid].serialize())


@socketio.on('dfs-card-update')
def dfs_card(msg):
    """Socket for defending card update"""

    gameid = msg["gameid"]
    card = msg["card"]
    gameLst[gameid].dfs_card = card
    gameLst[gameid].update()
    print(gameLst[gameid].serialize())


@socketio.on("set-defender")
def set_defender(msg):
    """Socket for setting up defender"""

    gameid = msg["gameid"]
    userid = msg["userid"]
    gameLst[gameid].defender = int(userid)
    gameLst[gameid].update()
    print(gameLst[gameid].serialize())


@socketio.on('submit-vote')
def reg_vote(msg):
    """Socket for vote"""

    userid = msg["userid"]
    card = msg["card"]
    gameid = msg["gameid"]
    gameLst[gameid].vote(userid, card)


def messageReceived(methods=['GET', 'POST']):
    """Function for receiving message"""

    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    """Socket for event"""

    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

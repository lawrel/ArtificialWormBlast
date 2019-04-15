from threading import Timer
import random
import uuid
from flask import render_template, request, jsonify
from flask_socketio import join_room, leave_room, send, emit
from server import app, socketio
from server.routes.gameObject import Game
from server.routes.playerObject import Player
from server.routes.statesObject import GameState, WaitState, SelectHandState, NewRoundState, AttackState, DefendState, VoteState, WinnerState, EndState


gameLst = {}


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

@socketio.on('check-games')
def checkGames(data):
    username = data['player']['username']
    email = data['player']['email']
    userid = data['player']['userid']
    player = Player(userid, username, email)

    for gameid, game in gameLst.items():
        if (game.gameStatus()):
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++ " + game.gameid)
            #gameLst[game.gameid] = game
            data['gameid'] = gameid
            joinGame(data)
            send(gameid, room=gameid)
            return game.gameid

    game = Game(True, 5, 0)
    print("--------------------------------------------------------- " + game.gameid)
    gameLst[game.gameid] = game
    data['gameid'] = game.gameid
    joinGame(data)
    send(game.gameid, room=game.gameid)
    return game.gameid

@socketio.on('create-game')
def createGame(data):
    for key, value in data.items():
        print(key, value)
    username = data['player']['username']
    email = data['player']['email']
    userid = data['player']['userid']
    player = Player(userid, username, email)
    print("CARDSSSSSSSSSSSSSSSSSS: "+ data['cards'])
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

@socketio.on('dfs-card-update')
def dfs_card(msg):
    gameid = msg["gameid"]
    card = msg["card"]
    gameLst[gameid].dfs_card = card
    gameLst[gameid].update()
    print(gameLst[gameid].serialize())

@socketio.on("set-defender")
def set_defender(msg):
    gameid = msg["gameid"]
    userid = msg["userid"]
    gameLst[gameid].defender = int(userid)
    gameLst[gameid].update()
    print(gameLst[gameid].serialize())

@socketio.on('submit-vote')
def reg_vote(msg):
    userid = msg["userid"]
    card = msg["card"]
    gameid = msg["gameid"]
    gameLst[gameid].vote(userid, card)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

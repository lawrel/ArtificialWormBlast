from flask_socketio import SocketIO
from flask import Flask, render_template, request, jsonify
from server import app, socketio


@app.route('/game/')
def sessions():
    return render_template('game.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

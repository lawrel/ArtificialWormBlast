var socket;
var clientState = null;
var gameState = null;

$( document ).ready(function() {
    // Connect to game server over socketio
    connectGameSocket();

    // Check if the player is logged in
    handleLogin();

    document.addEventListener("logged-in", function() {
        //createGame_io();
        // Check if the game route is valid
        handleJoinGame();
    });
    
});

function connectGameSocket() {
    // Connect to game server
    socket = io.connect('ws://' + document.domain + ':' + location.port);

    // Event handlers with callback functions
    socket.on("join-game", joinGame_res);
    socket.on("state", )
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
        console.log(socket);
    });
    socket.on('message', function (msg) {
        console.log(msg);
    });
}

function handleJoinGame() {
    var params = getParams();
    if ("game_id" in params) {
        // Attempt to join game
        var gameid = params["game_id"];
        var playerData = getPlayerData();
        joinGame_io(gameid, playerData);

    } else {
        console.log("User didn't provide a game_id.");
    }
}

function getPlayerData() {
    var seshData = retrieveSessionData();
    return seshData;
}

// Strip the parameters from the URL
function getParams() {
    // Get the params in an array
    var url = window.location.href;
    var params = url.split('?');
    
    // Format into a dictionary/JSON object
    var data = {};
    for (var i = 1; i < params.length; i++) {
        var keyVal = params[i].split('=');
        var key = keyVal[0];
        var val = keyVal[1];
        data[key] = val;
    }

    return data;
}

function syncGameState() {

}

function doSomething() {
    io.to("game-01").emit('my event', {data: 'Doing something!!!'});
}

// SOCKET-IO Handlers ============================================================
function joinGame_io(gameid, playerData) {
    socket.emit('join-game', {player: playerData, gameid: gameid});
}

function joinGame_res(msg) {
    if ("status" in msg) {
        var status = msg["status"];
        if (status == "success") {
            console.log("Game successfully joined");
        } 
        else if (status == "failure") {
            console.log("Join game failed");
        }
    }
}


function createGame_io() {
    socket.emit('create-game', {player: {username:'seanrice', email:'seane.rice@gmail.com', userid: '17'}});
}

function createGame_res() {
   
}
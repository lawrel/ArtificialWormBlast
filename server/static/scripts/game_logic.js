var socket;
var clientState = null;
var gameState = null;
var gameData = null;
var attacker = null;
var atkCard = null;
var dfsCard = null;
var defender = null;
var attackVotes = 0;
var defendVotes= 0;
var stateUpdateEvent = new Event('game-update');
var playerDataEvent = new Event('player-data');

$( document ).ready(function() {
    // Connect to game server over socketio
    connectGameSocket();

    // Check if the player is logged in
    handleLogin();

    document.addEventListener("logged-in", function() {
        //playerData_io();
        handleJoinGame();
    });

    document.addEventListener("player-data", function () {
        handleJoinGame();
    });

    // document.addEventListener("game-update", function () {
    //     joinGame_io(gameData["gameid"], getPlayerData())
    // })
    
});

function connectGameSocket() {
    // Connect to game server
    socket = io.connect('ws://' + document.domain + ':' + location.port);

    // Event handlers with callback functions
    socket.on("join-game", joinGame_res);
    socket.on("game-data", gameData_res)
    socket.on('player-data', playerData_res);
    socket.on("attacker", attacker_res)
    socket.on("atkCard", attackCard_res)
    socket.on("dfsCard", defendCard_res)
    // socket.on("state", )
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
    } else if ("gameid" in gameData) {
        joinGame_io(gameData["gameid"], getPlayerData());
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

// SOCKET-IO Handlers ============================================================
function joinGame_io(gameid, playerData) {
    socket.emit('join-game', {player: playerData, gameid: gameid});
}

function joinGame_res(msg) {
    if ("status" in msg) {
        var status = msg["status"];
        if (status == "success") {
            console.log("Game successfully joined: " + msg["gameid"]);
            window.history.replaceState({}, document.title, "?game_id=" + msg["gameid"]);
            gameData_io(msg["gameid"]);
        } 
        else if (status == "failure") {
            console.log("Join game failed" + msg["reason"]);
        }
    }
}

function createGame_io() {
    socket.emit('create-game', {player: getPlayerData()});
}

function createGame_res() {
   
}

function playerData_io() {
    socket.emit('player-data', {player: getPlayerData()});
}

function playerData_res(msg) {
    gameData = msg;
    document.dispatchEvent(playerDataEvent);
}

function selectDefender_io(userid, gameid) {
    socket.emit('set-defender', {userid:userid, gameid:gameid});
}

function attackCard_io(gameid, card) {
    socket.emit('atk-card-update', { gameid: gameid, card: card});
}
function attackCard_res(msg) {
    atkCard = msg;
    document.dispatchEvent(playerDataEvent);
}

function defendCard_io(gameid, card) {
    socket.emit('dfs-card-update', { gameid: gameid, card: card});
}
function defendCard_res(msg) {
    dfsCard = msg;
    document.dispatchEvent(playerDataEvent);
}

function gameData_io(gameid) {
    socket.emit('game-data', {gameid:gameid});
}

function gameData_res(msg) {
    gameData = msg;
    document.dispatchEvent(stateUpdateEvent);
}

function sendHand_io(hand, playerData, gameid) {
    var data = {
        hand:hand,
        userid:playerData["userid"],
        gameid:gameid
    };
    socket.emit('player-hand', data)
}

function attacker_res(msg) {
    attacker = msg;
    document.dispatchEvent(stateUpdateEvent);
}

function winner_io(gameid, userid) {
    socket.emit('round-winner', { gameid: gameid, userid: userid});
}
function winner_res(msg) {
    winner = msg;
    document.dispatchEvent(playerDataEvent);
}

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

$(document).ready(function () {
    $("#waitingModal").modal({
        backdrop: "static", //remove ability to close modal with click
        keyboard: false, //remove option to close with keyboard
        show: false //Display loader!
    });
});

var card_id = -1;
var token = '';
var img = new Image(450, 630);
var deck = [];
var card_data;
getDeck_ajax();

function init() {
    params = getParams();
    if ("card_id" in params && params.card_id != '') {
        card_id = Number(params.card_id);
        var incl_id = false;
        for (var i = 0; i < deck.length; i++) {
            var c_id = deck[i]["id"];
            if (c_id == card_id) {
                incl_id = true;
                card_data = deck[i];
                break;
            }
        }

        if (incl_id) {
            console.log("Editing card: " + String(card_id));
            img.src = 'http://localhost:8000/cards/preview/' + String(card_id);
            $("#monster-name").val(card_data["name"]);

        } else {
            console.error("You don't own this card! " + String(card_id));
            card_id = -1;
        }
    }
}

function getDeck_ajax() {
    // ask for email
    var fd = new FormData();
    fd.append('token', retrieveLoginToken());

    $.ajax({
        url: '/cards/player_cards',
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data) {
            if ("error" in data) { }
            else {
                deck = data["cards"];
                console.log(data);
                init();
            }
        }
    });
}


function upload(name) {
    uploadImage_ajax(name);
}



function newCard_ajax() {
    var uploader = document.getElementById('uploader');
    var monsterName = document.getElementById('fname')
    var fd = new FormData();
    fd.append("img-data", canvas.toDataURL("image/png;base64"));
    fd.append("token", retrieveLoginToken());
    fd.append("card-name", $("#monster-name").val());
    $("#waitingModal").modal('show');
    $.ajax({
        url: '/cards/new-card',
        data: fd,
        cache: false,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data) {
            console.log(data);
            if ("error" in data) {

            }
            else if ("success" in data) {

            }
        },
        complete: function () {
            $("#waitingModal").modal('hide');
        }
    });
}


function editCard_ajax() {
    var uploader = document.getElementById('uploader');
    var fd = new FormData();
    fd.append("img-data", canvas.toDataURL("image/png;base64"));
    fd.append("token", retrieveLoginToken());
    fd.append("card-id", card_id);
    fd.append("card-name", $("#monster-name").val());
    $("#waitingModal").modal('show');
    $.ajax({
        url: '/cards/edit-card',
        data: fd,
        cache: false,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data) {
            console.log(data);
            if ("error" in data) {

            }
            else if ("success" in data) {

            }
        },
        complete: function () {
            $("#waitingModal").modal('hide');
        }
    });
}

function deleteCard_ajax(){
    var uploader = document.getElementById('uploader');
    var fd = new FormData();
    fd.append("img-data", canvas.toDataURL("image/png;base64"));
    fd.append("token", retrieveLoginToken());
    fd.append("card-id", card_id);
    fd.append("card-name", $("#monster-name").val());
    $("#waitingModal").modal('show');
    $.ajax({
        url: '/cards/remove-card',
        data: fd,
        cache: false,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data) {
            console.log(data);
            if ("error" in data) {

            }
            else if ("success" in data) {

            }
        },
        complete: function () {
            $("#waitingModal").modal('hide');
        }
    });
    window.location.href = "/home/";
}


function save() {
    if (card_id == -1) {
        newCard_ajax();
    } else {
        editCard_ajax();
    }
    //redirect to page that was on
}

function deleteCard()
{
    if (card_id != -1){
        deleteCard_ajax()
    }
}

function reload() {
}
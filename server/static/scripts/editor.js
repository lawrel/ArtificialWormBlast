/**
 *  Card editor 
 *  Especially ajax
 */


var card_id = -1;
var token = '';
var img = new Image(450, 630);
var deck = [];
var card_data;
getDeck_ajax();


// On ready call
$(document).ready(function () {
    $("#waitingModal").modal({
        backdrop: "static", //remove ability to close modal with click
        keyboard: false, //remove option to close with keyboard
        show: false //Display loader!
    });
    img.onload = function () {
        console.log("its")
        ctx.drawImage(img, 0, 0);
    }
});


// Initalizer
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
            img.src = '/cards/preview/' + String(card_id);
            $("#monster-name").val(card_data["name"]);

        } else {
            console.error("You don't own this card! " + String(card_id));
            card_id = -1;
            window.history.replaceState({}, document.title, "?card_id=-1");
        }
    }
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


// Gets the deck
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


// Function uploads
function upload(name) {
    uploadImage_ajax(name);
}


// Gets new card
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
                card_id = Number(data["card_id"]);
                window.history.replaceState({}, document.title, "?card_id=" + card_id);
            }
        },
        complete: function () {
            $("#waitingModal").modal('hide');
        }
    });
}


// Edits card
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


// Deletes card
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


// Function saves cards
function save() {
    if (card_id == -1) {
        newCard_ajax();
    } else {
        editCard_ajax();
    }
    //redirect to page that was on
}


// Function deletes cards
function deleteCard()
{
    if (card_id != -1){
        deleteCard_ajax()
    }
}


// Function reloads card
function reload() {
}
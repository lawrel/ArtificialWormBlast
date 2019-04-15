var loginToken = null;
var loggedInEvent = new Event("logged-in");

function retrieveSessionData() {
    //  Retrieve session data
    if (typeof(Storage) !== "undefined") {
        return JSON.parse(localStorage.getItem("MonsterInk_session_data"));
    } else {
        console.error("Cannot retrieve session data. No local storage defined.")
        return null;
    }
}

function saveSessionData(seshData) {
    if (typeof(Storage) !== "undefined") {
        localStorage.setItem("MonsterInk_session_data", JSON.stringify(seshData));
        console.log("saved session data");
    } else {
        console.error("Cannot save session data. No local storage defined.")
    }
}

function retrieveLoginToken() {
    //  Retrieve session data
    if (typeof(Storage) !== "undefined") {
        return localStorage.getItem("MonsterInk_login_token");
    } else {
        console.error("Cannot retrieve session data. No local storage defined.")
        return null;
    }
}

function saveLoginToken(loginToken) {
    if (typeof(Storage) !== "undefined") {
        localStorage.setItem("MonsterInk_login_token", loginToken);
        console.log("token stored locally");
    } else {
        console.error("Cannot save session data. No local storage defined.")
    }
}

// Get session data for a specific user login token
function getSessionData_ajax(loginToken) {
    var fd = new FormData();
    fd.append( 'login-token', loginToken);
    
    $.ajax({
        url: '/login/session-data',
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            if ("error" in data) {
                console.log(data)
                redirectLogin();
            } else {
                saveSessionData(data);
                document.dispatchEvent(loggedInEvent);
            }
        }
    });
}

function handleLogin() {
    $("#body-content").hide();
    loginStatus = 'logged-out';
    loginToken = retrieveLoginToken();
    console.log(loginToken);
    if (loginToken != null) {
        getSessionData_ajax(loginToken);
    } else {
        redirectLogin()
    }
}

function handleLogout() {
    saveLoginToken("");
    window.location.href = "/"
}

function redirectLogin() {
    window.location.href = "/login"
}

function redirectHome() {
    window.location.href = "/home"
}

$(document).ready(function () {
    
});
// This piece of logic handles the session data retrieval and login redirects
// var sessionData = {};
// $( document ).ready(function() {
//     handleLogin();
// });
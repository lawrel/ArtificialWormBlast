
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

var card_id = 0;
var token = '';
var img = new Image(450, 630);
var deck = [];
getDeck_ajax();

function init() {
    params = getParams();
    if ("card_id" in params && params.card_id != '') {
        card_id = Number(params.card_id);
        if (deck.includes(card_id)) {
            console.log("Editing card: " + String(card_id));
            img.src = 'http://localhost:8000/cards/preview/'+String(card_id);
            
        } else {
            console.error("You don't own this card! " + String(card_id));
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

var canvas = document.getElementById("paint");
var width;
var height;
var curX, curY, prevX, prevY;
var hold;
var fill_value;
var stroke_value;
var canvas_data;
var vert;
var horzt;
$(document).ready(function () {
    canvas = document.getElementById("paint");
    ctx = canvas.getContext("2d");
    width = canvas.width;
    height = canvas.height;
    hold = false;
    ctx.lineWidth = 2;
    fill_value = true;
    stroke_value = false;
    canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [], "text": [], "upload": [] }
    vert = (2 / 100) * 630;
    horzt = (1 / 100) * 450;
    
    reset();
    pencil();
    img.onload = function () {
        console.log("its")
        ctx.drawImage(img, 0, 0);
    }
});


function change(type) {
    if (type == "pencil") {
        pencil();
    }
    if (type == "line") {
        line();
    }
    if (type == "rectangle") {
        rectangle();
    }
    if (type == "circle") {
        circle();
    }
    if (type == "eraser") {
        eraser();
    }
    if (type == "upload") {
        //check if new design ...
        upload();
    }
    if (type == "fill") {
        fill();
    }
    if (type == "outline") {
        outline();
    }
}

function color(color_value) {
    ctx.strokeStyle = color_value;
    ctx.fillStyle = color_value;
}

function font(font_value) {
    ctx.font = font_value;
}

function changeVert(v) {
    vert = (v / 100) * 630;
}

function changeHorzt(h) {
    horzt = (h / 100) * 450;
}

function add_pixel() {
    ctx.lineWidth += 1;
}

function reduce_pixel() {
    if (ctx.lineWidth == 1) {
        ctx.lineWidth = 1;
    } else {
        ctx.lineWidth -= 1;
    }
}

function fill() {
    fill_value = true;
    stroke_value = false;
}

function outline() {
    fill_value = false;
    stroke_value = true;
}

function reset() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [], "text": [], "upload": [] }
    var oldcolor = ctx.strokeStyle;
    color("#FFFFFF");
    ctx.strokeRect(0, 0, 450, 630);
    if (fill_value) {
        ctx.fillRect(0, 0, 450, 630);
    }
    color(oldcolor);
    ctx.drawImage(img, 0, 0);
}

// pencil tool

function pencil() {

    canvas.onmousedown = function (e) {
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;

        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };

    canvas.onmousemove = function (e) {
        if (hold) {
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };

    canvas.onmouseup = function (e) {
        hold = false;
    };

    canvas.onmouseout = function (e) {
        hold = false;
    };

    function draw() {
        ctx.lineTo(curX, curY);
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }
}

function encode_canvas() {
    var dataURL = canvas.toDataURL("image/png;base64");
    uploadImageB64_ajax(dataURL);
}

// line tool

function line() {

    canvas.onmousedown = function (e) {
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft;
        prevY = e.clientY - canvas.offsetTop;
        hold = true;
    };

    canvas.onmousemove = function linemove(e) {
        if (hold) {
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            ctx.beginPath();
            ctx.moveTo(prevX, prevY);
            ctx.lineTo(curX, curY);
            ctx.stroke();
            canvas_data.line.push({ "starx": prevX, "starty": prevY, "endx": curX, "endY": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
            ctx.closePath();
        }
    };

    canvas.onmouseup = function (e) {
        hold = false;
    };

    canvas.onmouseout = function (e) {
        hold = false;
    };
}

// rectangle tool

function rectangle() {

    canvas.onmousedown = function (e) {
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft;
        prevY = e.clientY - canvas.offsetTop;
        hold = true;
    };

    canvas.onmousemove = function (e) {
        if (hold) {
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft - prevX;
            curY = e.clientY - canvas.offsetTop - prevY;
            ctx.strokeRect(prevX, prevY, curX, curY);
            if (fill_value) {
                ctx.fillRect(prevX, prevY, curX, curY);
            }
            canvas_data.rectangle.push({ "starx": prevX, "stary": prevY, "width": curX, "height": curY, "thick": ctx.lineWidth, "stroke": stroke_value, "stroke_color": ctx.strokeStyle, "fill": fill_value, "fill_color": ctx.fillStyle });
        }
    };

    canvas.onmouseup = function (e) {
        hold = false;
    };

    canvas.onmouseout = function (e) {
        hold = false;
    };
}

// circle tool

function circle() {

    canvas.onmousedown = function (e) {
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.clientX - canvas.offsetLeft;
        prevY = e.clientY - canvas.offsetTop;
        hold = true;
    };

    canvas.onmousemove = function (e) {
        if (hold) {
            ctx.putImageData(img, 0, 0);
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            ctx.beginPath();
            ctx.arc(Math.abs(curX + prevX) / 2, Math.abs(curY + prevY) / 2, Math.sqrt(Math.pow(curX - prevX, 2) + Math.pow(curY - prevY, 2)) / 2, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.stroke();
            if (fill_value) {
                ctx.fill();
            }
            canvas_data.circle.push({ "starx": prevX, "stary": prevY, "radius": curX - prevX, "thick": ctx.lineWidth, "stroke": stroke_value, "stroke_color": ctx.strokeStyle, "fill": fill_value, "fill_color": ctx.fillStyle });
        }
    };

    canvas.onmouseup = function (e) {
        hold = false;
    };

    canvas.onmouseout = function (e) {
        hold = false;
    };
}

// eraser tool

function eraser() {

    canvas.onmousedown = function (e) {
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;

        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };

    canvas.onmousemove = function (e) {
        if (hold) {
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };

    canvas.onmouseup = function (e) {
        hold = false;
    };

    canvas.onmouseout = function (e) {
        hold = false;
    };

    function draw() {
        ctx.lineTo(curX, curY);
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }
}

function text(words) {
    ctx.fillText(words, horzt, vert); //horzt, vert
    canvas_data.line.push({ "starx": horzt, "starty": vert, "text": words, "font": ctx.font, "color": ctx.strokeStyle })
}

function upload(name) {
    uploadImage_ajax(name);
    /**
    * UPLOAD SCRIPT
    * This script uses the UploadAtClick library to upload files on a webserver folder
    * using a PHP script ("upload/upload.php")
    * Project homepage: http://code.google.com/p/upload-at-click/
    */
    // upclick(
    // {
    //         element: uploader,
    //     action: 'upload/upload.php', //need to fix
    //     onstart:
    // function(filename)
    // {
    //         //alert('Start upload: '+filename);
    //     },
    //         oncomplete:
    //     function(response_data)
    // {
    // // Check upload Status
    // if (response_data != "FAIL") {
    //         // Draw the picture into Canvas
    //         // "response_data" contains the image file name returned from the PHP script
    //         displayPicture("upload/" + response_data);
    //     }
    // }
    //     });



}

// function uploadImage_ajax() {
//     var uploader = document.getElementById('uploader');
//     var fd = new FormData($("#upload-img-form")[0]);

//     $.ajax({
//         url: '/editor/upload-img',
//         data: fd,
//         cache: false,
//         processData: false,
//         contentType: false,
//         type: 'POST',
//         success: function (data) {
//             console.log(data);
//             if ("error" in data) {

//             }
//             else if ("success" in data) {

//             }
//         }
//     });
// }

function newCard_ajax() {
    var uploader = document.getElementById('uploader');
    var monsterName = document.getElementById('fname')
    var fd = new FormData();
    fd.append("img-data", canvas.toDataURL("image/png;base64"));
    fd.append("token", retrieveLoginToken());
    fd.append("card-name", monsterName);

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
        }
    });
}


function editCard_ajax() {
    var uploader = document.getElementById('uploader');
    var fd = new FormData();
    fd.append("img-data", canvas.toDataURL("image/png;base64"));
    fd.append("token", retrieveLoginToken());
    fd.append("card-id", card_id);

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
        }
    });
}



function save() {
    var filename = document.getElementById("fname").value;
    var data = JSON.stringify(canvas_data);
    var image = canvas.toDataURL();

    $.post("/", { save_fname: filename, save_cdata: data, save_image: image });
    alert(filename + " saved");

    newCard_ajax()
    //redirect to page that was on
}


function reload() {
}
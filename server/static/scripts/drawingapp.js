// JavaScript source code
// DRAWING APP FUNCTIONALITY

var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var width = canvas.width;
var height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
ctx.lineWidth = 2;
var fill_value = true;
var stroke_value = false;
var x = 0;
var y = 0;
var drag = false;
var rgbaColor = 'rgba(255,0,0,1)';
var canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [], "text": [], "upload": [] }
var vert = (2 / 100) * 630;
var horzt = (1 / 100) * 450;
reset();

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
function update(color_value) {
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
    update("#FFFFFF");
    ctx.strokeRect(0, 0, 450, 630);
    if (fill_value) {
        ctx.fillRect(0, 0, 450, 630);
    }
    update(oldcolor);
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
//bucket tool tba
//add text
function text(words) {
    ctx.fillText(words, horzt, vert); //horzt, vert
    canvas_data.line.push({ "starx": horzt, "starty": vert, "text": words, "font": ctx.font, "color": ctx.strokeStyle })
}
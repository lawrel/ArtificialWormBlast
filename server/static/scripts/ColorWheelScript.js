
var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var width = canvas.width;
var height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
ctx.lineWidth = 2;
var fill_value = true;
var stroke_value = false;
var colorBlock = document.getElementById('color-block');
var ctx1 = colorBlock.getContext('2d');
var width1 = colorBlock.width;
var height1 = colorBlock.height;
var colorStrip = document.getElementById('color-strip');
var ctx2 = colorStrip.getContext('2d');
var width2 = colorStrip.width;
var height2 = colorStrip.height;
var colorLabel = document.getElementById('color-label');
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
function color(color_value) {
    ctx.strokeStyle = color_value;
    ctx.fillStyle = color_value;
}
ctx1.rect(0, 0, width1, height1);
fillGradient();
ctx2.rect(0, 0, width2, height2);
var grd1 = ctx2.createLinearGradient(0, 0, 0, height1);
grd1.addColorStop(0, 'rgba(255, 0, 0, 1)');
grd1.addColorStop(0.17, 'rgba(255, 255, 0, 1)');
grd1.addColorStop(0.34, 'rgba(0, 255, 0, 1)');
grd1.addColorStop(0.51, 'rgba(0, 255, 255, 1)');
grd1.addColorStop(0.68, 'rgba(0, 0, 255, 1)');
grd1.addColorStop(0.85, 'rgba(255, 0, 255, 1)');
grd1.addColorStop(1, 'rgba(255, 0, 0, 1)');
ctx2.fillStyle = grd1;
ctx2.fill();
function click(e) {
    x = e.offsetX;
    y = e.offsetY;
    var imageData = ctx2.getImageData(x, y, 1, 1).data;
    rgbaColor = 'rgba(' + imageData[0] + ',' + imageData[1] + ',' + imageData[2] + ',1)';
    fillGradient();
}
function fillGradient() {
    ctx1.fillStyle = rgbaColor;
    ctx1.fillRect(0, 0, width1, height1);
    var grdWhite = ctx2.createLinearGradient(0, 0, width1, 0);
    grdWhite.addColorStop(0, 'rgba(255,255,255,1)');
    grdWhite.addColorStop(1, 'rgba(255,255,255,0)');
    ctx1.fillStyle = grdWhite;
    ctx1.fillRect(0, 0, width1, height1);
    var grdBlack = ctx2.createLinearGradient(0, 0, 0, height1);
    grdBlack.addColorStop(0, 'rgba(0,0,0,0)');
    grdBlack.addColorStop(1, 'rgba(0,0,0,1)');
    ctx1.fillStyle = grdBlack;
    ctx1.fillRect(0, 0, width1, height1);
}
function mousedown(e) {
    drag = true;
    changeColor(e);
}
function mousemove(e) {
    if (drag) {
        changeColor(e);
    }
}
function mouseup(e) {
    drag = false;
}
function changeColor(e) {
    x = e.offsetX;
    y = e.offsetY;
    var imageData = ctx1.getImageData(x, y, 1, 1).data;
    rgbaColor = 'rgba(' + imageData[0] + ',' + imageData[1] + ',' + imageData[2] + ',1)';
    colorLabel.style.backgroundColor = rgbaColor;
    color(rgbaColor);
}
colorStrip.addEventListener("click", click, false);
colorBlock.addEventListener("mousedown", mousedown, false);
colorBlock.addEventListener("mouseup", mouseup, false);
colorBlock.addEventListener("mousemove", mousemove, false);
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
function text(words) {
    ctx.fillText(words, horzt, vert); //horzt, vert
    canvas_data.line.push({ "starx": horzt, "starty": vert, "text": words, "font": ctx.font, "color": ctx.strokeStyle })
}
function upload() {
    uploadImage_ajax();
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
function uploadImage_ajax() {
    var uploader = document.getElementById('uploader');
    var fd = new FormData($("#upload-img-form")[0]);
    $.ajax({
        url: '/editor/upload-img',
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
    //redirect to page that was on
}
function reload() {
}
</script >
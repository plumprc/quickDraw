let pink = document.getElementById("button-about");
let close = document.getElementById("close");
let play = document.getElementById("button-play");
let confirm = document.getElementById("button-newround-play");

pink.onclick = function () {
    $("#about-card").toggleClass("visible");
};

close.onclick = function () {
    $("#about-card").toggleClass("visible");
};

play.onclick = function () {
    $("#newround-card").toggleClass("visible");
};

confirm.onclick = function () {
    $("#newround-card").toggleClass("visible");
    $("#game").show();
    $("#splash").hide();
};

$("#game-close").click(function(){
    $("#game").hide();
    $("#splash").show();
});

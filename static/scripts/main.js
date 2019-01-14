


window.onload = function () {
    document.getElementById("input_keywords").addEventListener("keyup", function (event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("btn_chat_send").click();
        }
    });
    // Stuff to be executed on Load
}

function send_chat(){
    var utterance = document.getElementById("input_keywords").value;

    if (utterance.trim() == ''){
        prep_bubble_bot("Please type something...");
        return;
    }

    prep_bubble_user(utterance);

    $.post('/processText', {utterance: utterance}, function(resp) {
      prep_bubble_bot(resp);
    })
    .fail(function(exceptionType, exceptionCode) {
        alert( "Server side > " + exceptionCode + " : " + exceptionType.status);
    })
}

function getAvatar(entity){

    var avatar = document.createElement('img');
    avatar.src = "/static/images/" + entity + "_avatar.png";
    avatar.className = "imageIconMaker " + entity;
    // var temp = document.createElement('div');
    // temp.appendChild(avatar);
    return avatar;
}

function prep_bubble_bot(str){
    var bubble_bot = document.createElement('div');
    bubble_bot.className = "bubble bot";

    if (typeof str === 'string' || str instanceof String){
        var robotText = document.createElement('p');
        robotText.innerHTML = str;
    }
    else {
        robotText = str;
    }
    bubble_bot.appendChild(robotText);
    bubble_package = document.createElement('div');

    bubble_package.appendChild(getAvatar('bot'));
    bubble_package.appendChild(bubble_bot);
    update_chat(bubble_package);
}

function prep_bubble_user(str){

    document.getElementById("input_keywords").value = "";

    var bubble_user = document.createElement('div');
    bubble_user.className = "bubble user";

    var userText = document.createElement('p');
    userText.innerHTML = str;
    bubble_user.appendChild(userText);

    bubble_package = document.createElement('div');
    bubble_package.appendChild(getAvatar('user'));
    bubble_package.appendChild(bubble_user);
    update_chat(bubble_package);
}

function update_chat(elem){
    elem.appendChild(document.createElement("br"));
    $('#chat_window_div').append(elem);

    $('#chat_window_div').stop().animate({
      scrollTop: $('#chat_window_div')[0].scrollHeight}, 800)
}


function clearSearch() {
    document.getElementById("input_keywords").value = "";
    document.getElementById("div_resultList").innerHTML = "";
    document.getElementById("div_sol").innerHTML = "";
}

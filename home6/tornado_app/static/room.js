let online_count = 1;
let div = document.createElement('div');
let chat = document.getElementById('chat');

let after_alert = function () {
    ws.close();
    window.location.href = '/';
};

let online = function () {
    div.innerHTML = '<h3>Сейчас онлайн: ' + online_count + '</h3>';
    document.body.insertBefore(div, document.body.firstChild);
};

let send_msg_button = function () {
    let text = document.getElementById('text-msg').value;
    console.log(text);
    let msg = {'room': room, 'text': text, 'name': name};
    console.log(JSON.stringify(msg));
    ws.send(JSON.stringify(msg));
    document.getElementById('text-msg').value = '';
    return false;
};

let message_decode = function (event) {
    console.log(JSON.parse(event.data));
    if (JSON.parse(event.data)['type'] === 'message') {
        let new_msg = document.createElement('p');
        new_msg.innerHTML = JSON.parse(event.data)['name'] + ': ' + JSON.parse(event.data)['text'];
        chat.appendChild(new_msg);
    } else if (JSON.parse(event.data)['type'] === 'online') {
        online_count = JSON.parse(event.data)['value'];
        div.innerHTML = '<h3>Сейчас онлайн: ' + online_count + '</h3>';
    } else if (JSON.parse(event.data)['type'] === 'admin-clear') {
        chat.innerHTML = '';
    } else if (JSON.parse(event.data)['type'] === 'admin-kick') {
        alert('Поступил запрос на перезагрузку комнаты, извините за неудобства.');
        after_alert();
    }
    return false;
};

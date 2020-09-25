
var req = new XMLHttpRequest(); 
req.open('GET', 'chat/render_message', false); 
req.send({'chat':1});
const message = req.response


req = new XMLHttpRequest(); 
req.open('GET', '/chat/render_user_message', false); 
req.send({'chat':1});
const user_message = req.response



const queryString = window.location.search;

const urlParams = new URLSearchParams(queryString);

const roomName = JSON.parse(urlParams.get("room_pk"));

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    switch (data.type) {
        case "chat_message":
            var x = document.createElement('div')
            if(document.getElementById('user_id').textContent == data.userId){
                x.style.display= 'flex'
                x.style.justifyContent = 'flex-end'
                x.innerHTML = user_message
            }else{
                x.innerHTML = message
            }
            x.innerHTML = x.innerHTML.replace('__user__', data.userName)
            x.innerHTML = x.innerHTML.replace('__messagge__', data.message)
            document.querySelector('#chat-log').appendChild(x)
            break;
        case "chat_kick":
            if(document.getElementById('user_id').textContent == data.userId){
                    alert("You have been kicked out: "+ data.message)
                    window.location.replace("/");
            }
        default:
            break;
    }
    

};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message === ""){
        return
    }
    chatSocket.send(JSON.stringify({
        'type': 'chat_message',
        'message': message,
        'userId':document.getElementById('user_id').textContent,
        'userName':document.getElementById('user_name').textContent,
        'image':'',
        'file':'',
    }));
    messageInputDom.value = '';
};
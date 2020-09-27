
var req = new XMLHttpRequest(); 
req.open('GET', '/chat/render_message', false); 
req.send({});
const message = req.response


req = new XMLHttpRequest(); 
req.open('GET', '/chat/render_user_message', false); 
req.send({});
const user_message = req.response

const roomPk = document.getElementById('room_id').textContent;
let last_time = "0";

setInterval(function() {
    var req = new XMLHttpRequest(); 
    console.log(last_time)
    req.open('GET', '/chat/get_messages/'+roomPk+"/"+ last_time, true);
    req.overrideMimeType("application/json");
    console.log(req)
    req.onload  = function() {
        var jsonResponse = JSON.parse(req.responseText);
        
        console.log(jsonResponse)
            
        for (let index = 0; index < jsonResponse.length; index++) {
            const data = jsonResponse[index];
            last_time = data.last_time;
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
                    if(data.file){
                        x.querySelector("#fileLinkMessage").setAttribute("href", data.file)               
                    }else{
                        x.removeChild(x.querySelector("#fileLinkMessage"))                
                    }
                    if(data.image){
                        x.querySelector("#imageMessage").setAttribute("src", data.image)         
                    }else{
                        x.removeChild(x.querySelector("#imageMessage"))                
                    }
    
                    document.getElementById('chat-log').appendChild(x)
                    break;
                case "chat_kick":
                    if(document.getElementById('user_id').textContent == data.userId){
                            alert("You have been kicked out: "+ data.message)
                            window.location.replace("/");
                    }
                case "user_leave":
                    
                default:
                    break;
            }
        }
    }
    req.send();

}, 1000);

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message === ""){
        return
    }

    var req = new XMLHttpRequest(); 
    req.open('POST', '/chat/send_message', true); 
    req.overrideMimeType("application/json");
    formData = new FormData(document.querySelector('form'));
    formData.append("user",document.getElementById('user_id').textContent);
    formData.append("chatroom", roomPk);
    formData.append("message", message);
    req.onload  = function() {
        var jsonResponse = JSON.parse(req.responseText);

        console.log(jsonResponse)
        
        
        messageInputDom.value = '';

    }
    req.send(formData);
};
//document.querySelector('#chat-message-submit').onclick = function (e) {
//    )
//    req.open('GET', '/chat/send_message', false); 
//    req.send({
//        'type': 'chat_message',
//        'message': document.querySelector('#chat-message-input').value,
//        'userId':document.getElementById('user_id').textContent,
//        'userName':document.getElementById('user_name').textContent,
//        'image':document.querySelector('#id_image').value,
//        'file':document.querySelector('#id_file').value,
//    });
//    console.log('__________')
//}

var req = new XMLHttpRequest(); 
req.open('GET', '/chat/render_message', false); 
req.send({});
const message = req.response


req = new XMLHttpRequest(); 
req.open('GET', '/chat/render_user_message', false); 
req.send({});
const user_message = req.response

const room_id = document.getElementById('room_id').textContent;
const messages_per_minute = document.getElementById('messages_per_minute').textContent;
const time_between_messages = document.getElementById('time_between_messages').textContent;

let last_time = "0";
kickeableCount = 0 


document.addEventListener("DOMContentLoaded", function(event) {   
    
    var req = new XMLHttpRequest(); 
    req.open('GET', '/chat/get_messages/'+room_id+"/"+ last_time, true);
    req.overrideMimeType("application/json");
    req.onload  = function() {
        var jsonResponse = JSON.parse(req.responseText);
        
        var chatLog = document.getElementById('chat-log');
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
                    if(data.message != ""){
                        x.innerHTML = x.innerHTML.replace('__messagge__', data.message)
                    }else{                        
                        x.querySelector("#chat-message").remove();
                    }
                    if(data.file !== "/media/"){
                        x.querySelector("#fileLinkMessage").setAttribute("href", data.file)
                    }else{
                        x.querySelector("#fileLinkMessage").remove();       
                    }
                    if(data.image !== "/media/"){
                        x.querySelector("#imageMessage").setAttribute("src", data.image) 
                        x.querySelector("#imageMessageLink").setAttribute("href", data.image)
                                
                    }else{
                        x.querySelector("#imageMessage").remove();  
                        x.querySelector("#imageMessageLink").remove();
                    }
    
                    document.getElementById('chat-log').appendChild(x)
                    break;
                case "kick_message":
                        var x = document.createElement('div')
                        x.style.display= 'flex'
                        x.style.justifyContent = 'flex-end'
                        x.innerHTML = user_message
                        x.innerHTML = x.innerHTML.replace('__user__', data.userName)
                        x.innerHTML = x.innerHTML.replace('__messagge__', data.message)
                        x.querySelector("#fileLinkMessage").remove();    
                        x.querySelector("#imageMessage").remove();  
                        x.querySelector("#imageMessageLink").remove();
                        document.getElementById('chat-log').appendChild(x)  
                    break;
                case "ban_message":
                        var x = document.createElement('div')
                        x.style.display= 'flex'
                        x.style.justifyContent = 'flex-end'
                        x.innerHTML = user_message
                        x.innerHTML = x.innerHTML.replace('__user__', data.userName)
                        x.innerHTML = x.innerHTML.replace('__messagge__', data.message)
                        x.querySelector("#fileLinkMessage").remove();    
                        x.querySelector("#imageMessage").remove();  
                        x.querySelector("#imageMessageLink").remove();
                        document.getElementById('chat-log').appendChild(x)
                    
                default:
                    break;
            }
        }
        chatLog.scrollTop = chatLog.scrollHeight
        setInterval(getMessages, 1500);
    }
    req.send();
});


function getMessages() {
    console.log("_______")
    var req = new XMLHttpRequest(); 
    req.open('GET', '/chat/get_messages/'+room_id+"/"+ last_time, true);
    req.overrideMimeType("application/json");
    req.onload  = function() {
        var jsonResponse = JSON.parse(req.responseText);
        
        var chatLog = document.getElementById('chat-log');
        var scrollable = false;
        if (chatLog.scrollTop == (chatLog.scrollHeight - chatLog.offsetHeight)) {
            scrollable = true;
        }
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
                    if(data.message != ""){
                        x.innerHTML = x.innerHTML.replace('__messagge__', data.message)
                    }else{                        
                        x.querySelector("#chat-message").remove();
                    }
                    if(data.file !== "/media/"){
                        x.querySelector("#fileLinkMessage").setAttribute("href", data.file)
                    }else{
                        x.querySelector("#fileLinkMessage").remove();       
                    }
                    if(data.image !== "/media/"){
                        x.querySelector("#imageMessage").setAttribute("src", data.image) 
                        x.querySelector("#imageMessageLink").setAttribute("href", data.image)
                                
                    }else{
                        x.querySelector("#imageMessage").remove();  
                        x.querySelector("#imageMessageLink").remove();
                    }
    
                    document.getElementById('chat-log').appendChild(x)
                    break;
                case "kick_message":
                    if(document.getElementById('user_id').textContent == data.userId){
                            if(kickeableCount >= jsonResponse.length){
                                alert(data.message);
                                window.location.replace("/");
                            }
                    }else{
                        var x = document.createElement('div')
                        x.style.display= 'flex'
                        x.style.justifyContent = 'flex-end'
                        x.innerHTML = user_message
                        x.innerHTML = x.innerHTML.replace('__user__', data.userName)
                        x.innerHTML = x.innerHTML.replace('__messagge__', data.message)
                        x.querySelector("#fileLinkMessage").remove();    
                        x.querySelector("#imageMessage").remove();  
                        x.querySelector("#imageMessageLink").remove();
                        document.getElementById('chat-log').appendChild(x)                    
                    }
                    break;
                case "ban_message":
                    if(document.getElementById('user_id').textContent == data.userId){
                        if(kickeableCount >= jsonResponse.length){
                            alert(data.message)
                            window.location.replace("/");
                        }
                    }else{
                        var x = document.createElement('div')
                        x.style.display= 'flex'
                        x.style.justifyContent = 'flex-end'
                        x.innerHTML = user_message
                        x.innerHTML = x.innerHTML.replace('__user__', data.userName)
                        x.innerHTML = x.innerHTML.replace('__messagge__', data.message)
                        x.querySelector("#fileLinkMessage").remove();    
                        x.querySelector("#imageMessage").remove();  
                        x.querySelector("#imageMessageLink").remove();
                        document.getElementById('chat-log').appendChild(x)                    
                    }
                case "user_leave":
                    
                default:
                    break;
            }
            kickeableCount++
        }
        if(scrollable){
            chatLog.scrollTop = chatLog.scrollHeight
        }
    }
    req.send();
}
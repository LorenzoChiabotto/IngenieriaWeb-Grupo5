
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-submit').onclick = function (e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input');
    const messageFileInput = document.getElementById('file');
    const messageImageInput = document.getElementById('image');
    const message = messageInputDom.value;
    if (message === "" && messageImageInput.value == null && messageFileInput.value  == null){
        return
    }

    var req = new XMLHttpRequest(); 
    req.open('POST', '/chat/send_message', true); 
    req.overrideMimeType("application/json");
    formData = new FormData(document.querySelector('form'));
    formData.append("user",document.getElementById('user_id').textContent);
    formData.append("chatroom", room_id);
    formData.append("message", message);
    req.onload  = function() {
        messageInputDom.value = '';
        messageFileInput.value = null;
        messageImageInput.value = null;
    }
    req.send(formData);
};

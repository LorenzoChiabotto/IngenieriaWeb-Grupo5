
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-submit').onclick = function (e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input');
    const messageFileInput = document.getElementById('file');
    const messageImageInput = document.getElementById('image');
    const message = messageInputDom.value;
    if (message === "" && messageImageInput.value == "" && messageFileInput.value  == ""){
        return
    }

    var req = new XMLHttpRequest(); 
    req.open('POST', '/chat/send_message', true); 
    req.overrideMimeType("application/json");
    formData = new FormData(document.getElementById('formularioSendMessage'));
    formData.append("user",document.getElementById('user_id').textContent);
    formData.append("chatroom", room_id);
    formData.append("message", message);
    req.onload  = function() {
        messageInputDom.value = '';
        document.querySelectorAll(".custom-file-label")[0].innerHTML ="Select an image"
        document.querySelectorAll(".custom-file-label")[1].innerHTML ="Select a file"
    }
    req.send(formData);
};

$('#image').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})
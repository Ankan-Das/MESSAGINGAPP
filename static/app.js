document.addEventListener('DOMContentLoaded', function () {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    const messageContainer = document.getElementById('message-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    messageForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message !== '') {
            // Emit a 'send_message' event to the server
            socket.emit('send_message', { message: name + ": " + message });
            messageInput.value = '';
        }
    });

    // Listen for 'receive_message' events from the server
    socket.on('receive_message', function (data) {
        const messageElement = document.createElement('div');
        messageElement.innerText = data.message;
        messageContainer.appendChild(messageElement);
        
        // Scroll to the bottom to show the latest message
        messageContainer.scrollTop = messageContainer.scrollHeight;
    });
});

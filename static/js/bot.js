function sendData() {
    $.ajax({
        url: '/submit',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ message: 'Hello from JavaScript!' }),
        dataType: 'json',
        success: function(response) {
            alert('Server responded: ' + response.reply);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Load message history
    const conversation = document.getElementById('conversation');
    conversation.innerHTML = "";
    for (let i = message_history.length - 1; i >= 0; i--) {
        const message = message_history[i];
        displayMessage(message.sender, message.text);
    }
});

document.getElementById('chatForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const message = document.getElementById('message').value;
    sendMessage(message);
});

function sendMessage(message) {
    displayMessage('user', message);
    fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            displayMessage('bot', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    document.getElementById('message').value = '';
}

function displayMessage(sender, message) {
    
    const conversation = document.getElementById('conversation');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.classList.add('message');
    if (sender === 'user') {
        messageElement.classList.add('user-message');
    } else {
        messageElement.classList.add('bot-message');
    }
    conversation.appendChild(messageElement);
    conversation.scrollTop = conversation.scrollHeight;
}

const triggerIcon = document.getElementById('botIcon');
const chatBody = document.getElementById('botBody');
const openBot = document.getElementById('open');
const closeBot = document.getElementById('close');
let triggers = true;
triggerIcon.addEventListener('click', () => {

    if (triggers == true) {
        chatBody.style.display = 'flex';
        triggers = false;
        closeBot.style.display = 'block';
        openBot.style.display = 'none';
    } else {
        chatBody.style.display = 'none';
        triggers = true;
        closeBot.style.display = 'none';
        openBot.style.display = 'block';
    }
})
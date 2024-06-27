document.getElementById('upload-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const fileInput = document.getElementById('pdf-file');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('YOUR_NGROK_URL/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.success) {
        alert('PDF uploaded successfully.');
    } else {
        alert('Failed to upload PDF.');
    }
});

document.getElementById('chat-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message) {
        appendMessage('user', message);
        userInput.value = '';

        const response = await fetch('YOUR_NGROK_URL/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: message })
        });

        const result = await response.json();
        if (result.answer) {
            appendMessage('bot', result.answer);
        } else {
            appendMessage('bot', 'Sorry, I could not understand the question.');
        }
    }
});

function appendMessage(sender, message) {
    const messageContainer = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

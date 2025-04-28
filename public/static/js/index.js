document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== '') {
        const chatWindow = document.getElementById('chat-window');

        // Add user message
        const userMessage = document.createElement('div');
        userMessage.className = 'user-message';
        userMessage.textContent = `User: ${userInput}`;
        chatWindow.appendChild(userMessage);

        // Add bot response placeholder
        const botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.textContent = `DunderBot: Response to "${userInput}"`;
        chatWindow.appendChild(botMessage);

        // Clear input field
        document.getElementById('user-input').value = '';

        // Scroll to the bottom of the chat window
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});

document.getElementById('user-input').addEventListener('keypress', function(event) {
    console.log(event.key)
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission if inside a form
        document.getElementById('send-button').click();
    }
});
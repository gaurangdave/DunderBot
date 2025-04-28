document.addEventListener('DOMContentLoaded', function() {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const voiceResponseToggle = document.getElementById('voice-response');

    let voiceEnabled = false;

    voiceResponseToggle.addEventListener('change', function() {
        voiceEnabled = voiceResponseToggle.checked;
    });

    function addMessage(content, isUser = true) {
        const message = document.createElement('div');
        message.className = isUser ? 'user-message' : 'bot-message';

        if (!isUser) {
            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.textContent = '🤖'; // Use bot emoji as profile pic

            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.textContent = content;

            message.appendChild(avatar);
            message.appendChild(messageContent);
        } else {
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.textContent = content;

            message.appendChild(messageContent);
        }

        chatWindow.appendChild(message);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        if (!isUser && voiceEnabled) {
            const utterance = new SpeechSynthesisUtterance(content);
            window.speechSynthesis.speak(utterance);
        }
    }

    async function streamBotResponse(userMessage) {
        const response = await fetch('/api/stream-response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let botMessage = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            botMessage += decoder.decode(value, { stream: true });
            addMessage(botMessage, false);
        }
    }

    sendButton.addEventListener('click', async function() {
        const userMessage = userInput.value.trim();
        if (userMessage) {
            addMessage(userMessage, true);
            userInput.value = '';

            // Stream bot response
            await streamBotResponse(userMessage);
        }
    });

    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
        }
    });
});
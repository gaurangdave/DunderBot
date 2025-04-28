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

    async function streamBotResponse(user_input) {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');

        // Create a placeholder for the bot message
        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'bot-message';

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = '🤖';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        botMessageElement.appendChild(avatar);
        botMessageElement.appendChild(messageContent);

        chatWindow.appendChild(botMessageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Add typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.innerHTML = '<span></span><span></span><span></span> Thinking...';
        messageContent.appendChild(typingIndicator);

        let botMessage = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            botMessage += decoder.decode(value, { stream: true });
            messageContent.textContent = botMessage; // Update the same message content
        }

        // Remove typing indicator after response is complete
        typingIndicator.remove();
    }

    sendButton.addEventListener('click', async function() {
        const user_input = userInput.value.trim();
        if (user_input) {
            addMessage(user_input, true);
            userInput.value = '';

            // Stream bot response
            await streamBotResponse(user_input);
        }
    });

    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
        }
    });
});
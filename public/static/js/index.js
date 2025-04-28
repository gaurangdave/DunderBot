import { renderMarkdownToHTML } from './markdownRenderer.js';

document.addEventListener('DOMContentLoaded', function() {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const voiceResponseToggle = document.getElementById('voice-response');
    const chatContainer = document.querySelector('.chat-container');

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

    const welcomeMessages = [
        "🤖 DunderBot is online! Ask me anything about paper, pranks, or parties! 🎉",
        "📚 Seeking Office wisdom? Ask about fire drills, Dundies, or CPR classes! 🚒🏆",
        "🗣 'Would I rather be feared or loved? Easy. Both.' Start typing to meet your new assistant. 😎",
        "🎈 It's a beautiful day at Dunder Mifflin Scranton. What can I help you with today?",
        "🕵️‍♂️ Michael, Dwight, Jim, Pam... I've got all their secrets. Ask away!",
        "😂 Warning: Asking about 'That's what she said' jokes may cause uncontrollable laughter.",
        "📅 Fun fact: No bears, beets, or Battlestar Galactica questions are too obscure for me!",
        "💬 'I am Beyoncé, always.' Now, how can I assist you?",
        "🚀 Ready to dive into Scranton's wildest stories? Your question starts the adventure!",
        "📂 Filing away boredom. Loading fun facts about The Office. Ask me anything!"
    ];

    // Display a random welcome message when the page loads
    const randomWelcomeMessage = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
    addMessage(randomWelcomeMessage, false);

    async function streamBotResponse(user_input) {
        // Add the 'thinking' class to the chat container
        chatContainer.classList.add('thinking');

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
            // Render markdown to HTML if the server response contains markdown
            const renderedHTML = renderMarkdownToHTML(botMessage);
            messageContent.innerHTML = renderedHTML; // Update the same message content with HTML
        }

        // Remove typing indicator after response is complete
        typingIndicator.remove();

        // Remove the 'thinking' class and add a 'pulse' animation
        chatContainer.classList.remove('thinking');
        chatContainer.classList.add('pulse');

        // Remove the 'pulse' class after animation ends
        setTimeout(() => {
            chatContainer.classList.remove('pulse');
        }, 1000);
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
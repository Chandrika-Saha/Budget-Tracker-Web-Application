document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatNotification = document.getElementById('chat-notification');

    // Toggle chatbot
    chatbotToggle.addEventListener('click', function() {
        chatbotWindow.classList.toggle('active');
        chatNotification.style.display = 'none';
    });

    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        chatbotWindow.classList.remove('active');
    });

    // Send message
    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (message) {
            // Add user message
            addMessage(message, 'user');
            chatbotInput.value = '';

            // Simulate bot response
            setTimeout(() => {
                const botResponse = getBotResponse(message);
                addMessage(botResponse, 'bot');
            }, 1000);
        }
    }

    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const now = new Date();
        const time = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        messageDiv.innerHTML = `
            <div class="message-content">${text}</div>
            <div class="message-time">${time}</div>
        `;

        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Simple bot responses (you can make this more sophisticated)
    function getBotResponse(message) {
        const msg = message.toLowerCase();

        if (msg.includes('balance')) {
            return `Your current balance is ${{ balance }}. ${balance >= 0 ? 'Great job staying positive!' : 'Consider reducing expenses or increasing income.'}`;
        }

        if (msg.includes('income')) {
            return `Your total income is ${{ total_income }}. Keep up the good work!`;
        }

        if (msg.includes('expense')) {
            return `Your total expenses are ${{ total_expenses }}. Would you like some tips to reduce spending?`;
        }

        if (msg.includes('tip') || msg.includes('advice')) {
            const tips = [
                "Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings!",
                "Track your daily expenses to identify spending patterns.",
                "Set up automatic transfers to your savings account.",
                "Review and cancel unused subscriptions monthly.",
                "Cook at home more often to save on dining expenses."
            ];
            return tips[Math.floor(Math.random() * tips.length)];
        }

        if (msg.includes('hello') || msg.includes('hi')) {
            return "Hello! I'm here to help you with your budget. What would you like to know?";
        }

        return "I'm here to help with your budget! Try asking about your balance, income, expenses, or request some budgeting tips.";
    }

    // Event listeners
    chatbotSend.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
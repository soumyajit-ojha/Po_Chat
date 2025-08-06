document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatMessageInput = document.getElementById('chat-message');
    const chatMessagesContainer = document.getElementById('chat-messages');
    
    // Scroll to bottom of chat messages
    function scrollToBottom() {
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }
    
    // Add a new message to the chat UI
    function appendMessage(content, isSent) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isSent ? 'sent' : 'received'}`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.innerHTML = `
            <div class="message-content">${content}</div>
            <div class="message-meta">
                <span class="message-time">${timeString}</span>
            </div>
        `;
        
        chatMessagesContainer.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const messageContent = chatMessageInput.value.trim();
        
        if (messageContent) {
            // Send message via AJAX
            fetch(chatConfig.sendMessageUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': chatConfig.csrfToken
                },
                body: JSON.stringify({
                    content: messageContent
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    appendMessage(messageContent, true);
                    chatMessageInput.value = '';
                } else {
                    console.error('Error sending message:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });
    
    // Set up WebSocket for real-time updates (optional)
    function setupWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsPath = `/ws/chat/${chatConfig.roomId}/`;
        const chatSocket = new WebSocket(wsProtocol + window.location.host + wsPath);
        
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.type === 'chat_message') {
                const isSent = data.sender === chatConfig.currentUser;
                appendMessage(data.message, isSent);
            }
        };
        
        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
            // Implement reconnection logic here if needed
        };
    }
    
    // Initialize WebSocket if needed
    // setupWebSocket();
    
    // Initial scroll to bottom
    scrollToBottom();
});
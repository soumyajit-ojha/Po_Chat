document.addEventListener("DOMContentLoaded", function () {
    const friendsList = document.querySelectorAll(".friend");
    const chatWindow = document.querySelector(".chat-window");
    const chatHeader = document.querySelector(".chat-header");
    const chatInput = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-message");

    let selectedUserId = null;  // Stores the currently selected friend ID

    friendsList.forEach(friend => {
        friend.addEventListener("click", function () {
            selectedUserId = this.dataset.userId;
            loadChat(selectedUserId);
        });
    });

    function loadChat(userId) {
        fetch(`/chat/load_messages/${userId}/`)
            .then(response => response.json())
            .then(data => {
                chatWindow.innerHTML = "";
                chatHeader.textContent = `Chat with ${data.friend_name}`;
                
                data.messages.forEach(msg => {
                    const messageElement = document.createElement("div");
                    messageElement.classList.add("chat-message");
                    messageElement.textContent = `${msg.sender}: ${msg.text}`;
                    chatWindow.appendChild(messageElement);
                });
            });
    }

    sendButton.addEventListener("click", function () {
        const messageText = chatInput.value.trim();
        if (messageText && selectedUserId) {
            fetch(`/chat/send_message/${selectedUserId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("meta[name='csrf-token']").content
                },
                body: JSON.stringify({ text: messageText })
            }).then(response => response.json())
              .then(data => {
                if (data.success) {
                    chatInput.value = "";
                    loadChat(selectedUserId);  // Reload chat messages after sending
                }
            });
        }
    });
});

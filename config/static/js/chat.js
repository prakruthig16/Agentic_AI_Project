
let sessionId = document.body.dataset.sessionId || null;

async function sendMessage() {
    const input = document.getElementById("question");
    const sendBtn = document.getElementById("sendBtn");

    const question = input.value.trim();

    if (!question) return;

    addMessage(question, "user");

    input.value = "";
    sendBtn.disabled = true;

    const loading = addMessage("Thinking...", "assistant");

    try {
        // Get CSRF token
        const csrfElement = document.querySelector(
            '[name="csrfmiddlewaretoken"]'
        );

        if (!csrfElement) {
            throw new Error(
                "CSRF token missing. Check chat.html."
            );
        }

        const csrfToken = csrfElement.value;

        // Send request to Django
        const response = await fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                question: question,
                session_id: sessionId
            })
        });

        const data = await response.json();

        loading.remove();

        if (!response.ok) {
            addMessage(
                "Backend Error: " +
                JSON.stringify(data.error),
                "assistant"
            );
            return;
        }

        sessionId = data.session_id;

        addMessage(data.answer, "assistant");

    } catch (error) {
        loading.remove();

        console.error("Chat Error:", error);

        addMessage(
            "Error: " + error.message,
            "assistant"
        );

    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

function addMessage(text, role) {
    const container = document.getElementById("chatMessages");

    const message = document.createElement("div");

    message.className =
        "message " +
        (role === "user"
            ? "user-message"
            : "assistant-message");

    const avatar = document.createElement("div");
    avatar.className = "avatar";

    avatar.innerHTML =
        role === "user"
            ? '<i class="bi bi-person"></i>'
            : '<i class="bi bi-robot"></i>';

    const content = document.createElement("div");
    content.className = "message-content";
    content.textContent = text;

    message.appendChild(avatar);
    message.appendChild(content);

    container.appendChild(message);

    container.scrollTop = container.scrollHeight;

    return message;
}

function clearChat() {
    sessionId = null;

    document.getElementById("chatMessages").innerHTML = "";

    addMessage(
        "Hello! 👋 Start a new conversation.",
        "assistant"
    );
}

// Enter to send, Shift+Enter for newline
document.getElementById("question").addEventListener(
    "keydown",
    function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    }
);

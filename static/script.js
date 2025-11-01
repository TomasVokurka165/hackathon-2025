async function sendMessage() {
    const chatBox = document.getElementById("chat");
    const input = document.getElementById("userInput");
    const agentSelect = document.getElementById("agentSelect");
    const message = input.value.trim();
    const agent = agentSelect.value;

    if (!message) return;

    // Display user message
    chatBox.innerHTML += `<div class="message user">You: ${message}</div>`;
    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, agent })
        });

        const data = await response.json();
        chatBox.innerHTML += `<div class="message agent">${data.agent}: ${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        chatBox.innerHTML += `<div class="message agent">Error contacting server</div>`;
    }
}

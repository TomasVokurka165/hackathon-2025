let playerName = "";
let playerPersona = "";

// 🔹 Show or hide onboarding steps
function showStep(stepId) {
  document.querySelectorAll(".step").forEach(s => s.classList.add("hidden"));
  document.getElementById(stepId).classList.remove("hidden");
}

// 🔹 Handle nickname submission
function submitNickname() {
  const input = document.getElementById("nicknameInput");
  const name = input.value.trim();
  if (!name) return alert("Please enter a nickname.");
  playerName = name;
  document.getElementById("readyText").innerText = `Hi, ${playerName}. Are you ready to beat the Agents?`;
  showStep("readyStep");
}

// 🔹 Handle readiness buttons
function startGame(option) {
  if (option === "yes" || option === "scared") {
    showStep("personaStep");
  } else {
    alert("Maybe next time!");
  }
}

function declineGame() {
  alert("Come back when you’re ready!");
}

// 🔹 Choose persona and show random onboarding text
function choosePersona(persona) {
  playerPersona = persona; // ✅ store chosen persona

  const personaMessages = {
    "Ada Lovelace": [
      "You’ve stepped into the shoes of Ada Lovelace — the first programmer in history.",
      "Welcome, Lady Lovelace. Let’s see if logic and imagination can outsmart the AI.",
      "You now channel Ada’s pioneering spirit. Ready to compute the impossible?"
    ],
    "Nikola Tesla": [
      "Sparks fly as you become Nikola Tesla, the master of electricity.",
      "You’re now Tesla — brilliant, eccentric, and unpredictable.",
      "Welcome to the current of genius, Nikola. The AI won’t see you coming."
    ],
    "Leonardo Da Vinci": [
      "You are Leonardo da Vinci — artist, inventor, and dreamer of the future.",
      "The Renaissance returns! You are now Da Vinci, a mind ahead of its time.",
      "Let your curiosity paint the future, Leonardo."
    ],
    "Cleopatra": [
      "You’ve become Cleopatra — cunning, powerful, and unforgettable.",
      "All hail Cleopatra. Command wisdom and charm in equal measure.",
      "The queen of Egypt rises again. The AI should tread carefully."
    ]
  };

  const messages = personaMessages[persona];
  const randomMsg = messages[Math.floor(Math.random() * messages.length)];

  appendSystemMessage(randomMsg);
  document.getElementById("onboardingModal").style.display = "none";
}

// 🔹 Utility: Get initials for avatar
function getInitials(name) {
  return name.split(" ").map(word => word[0].toUpperCase()).join("").slice(0, 2);
}

// 🔹 Render message elements in chat
function createMessageElement(senderType, senderName, text) {
  const chatBox = document.getElementById("chat");

  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", senderType);

  const avatar = document.createElement("div");
  avatar.classList.add("avatar");
  avatar.textContent = getInitials(senderName);

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.textContent = text;

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(bubble);

  chatBox.appendChild(messageDiv);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
}

// 🔹 Display system / neutral messages
function appendSystemMessage(msg) {
  const chatBox = document.getElementById("chat");
  const sys = document.createElement("div");
  sys.classList.add("message", "system");
  sys.innerText = msg;
  chatBox.appendChild(sys);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
}

// 🔹 Send message to Flask backend + handle AI reply
async function sendMessage() {
  const chatBox = document.getElementById("chat");
  const input = document.getElementById("userInput");
  const message = input.value.trim();

  if (!message || !playerPersona) {
    appendSystemMessage("Please select a persona before chatting!");
    return;
  }

  // Display user message
  createMessageElement("user", playerName || "You", message);
  input.value = "";

  // Add a "typing..." indicator for realism
  const typingIndicator = document.createElement("div");
  typingIndicator.classList.add("message", "agent", "typing");
  typingIndicator.innerHTML = `<div class="avatar">AI</div><div class="bubble">...</div>`;
  chatBox.appendChild(typingIndicator);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });

  // ⏳ Simulate AI thinking delay (1–2 seconds)
  await new Promise(r => setTimeout(r, 1000 + Math.random() * 1000));

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, agent: playerPersona.toLowerCase() })
    });

    const data = await response.json();

    // Remove typing indicator
    typingIndicator.remove();

    // Show agent’s reply
    createMessageElement("agent", data.agent, data.reply);

  } catch (err) {
    typingIndicator.remove();
    appendSystemMessage("⚠️ Error contacting the AI agent.");
    console.error(err);
  }
}

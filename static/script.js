let playerName = "";
let playerPersona = "";

// --- Onboarding Flow --- //
function showStep(stepId) {
  document.querySelectorAll(".step").forEach(s => s.classList.add("hidden"));
  document.getElementById(stepId).classList.remove("hidden");
}

function submitNickname() {
  const input = document.getElementById("nicknameInput");
  const name = input.value.trim();
  if (!name) return alert("Please enter a nickname.");
  playerName = name;
  document.getElementById("readyText").innerText = `Hi, ${playerName}. Are you ready to beat the Agents?`;
  showStep("readyStep");
}

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

function choosePersona(persona) {
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

  playerPersona = persona;
  appendSystemMessage(randomMsg);

  // Hide modal and show chat
  document.getElementById("onboardingModal").style.display = "none";
}

// --- Chat Helpers --- //
function getInitials(name) {
  return name.split(" ").map(w => w[0].toUpperCase()).join("").slice(0, 2);
}

function appendMessage(senderName, text, senderType) {
  const chatBox = document.getElementById("chat");

  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", senderType);

  if (senderType === "typing") messageDiv.classList.add("typing");

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

function appendSystemMessage(text) {
  const chatBox = document.getElementById("chat");
  const sys = document.createElement("div");
  sys.classList.add("system");
  sys.textContent = text;
  chatBox.appendChild(sys);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
}

// --- Chat Communication --- //
async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();

  if (!message) return;
  if (!playerPersona) {
    appendSystemMessage("⚠️ Please select a persona before chatting!");
    return;
  }

  appendMessage(playerName || "You", message, "user");
  input.value = "";

  // Simulate typing indicator
  appendMessage("Agent", "...", "typing");

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, playerPersona })
    });

    const data = await response.json();

    // Remove typing indicator
    const typingEl = document.querySelector(".typing");
    if (typingEl) typingEl.remove();

    appendMessage(data.agent || "Agent", data.reply || "Hmm... interesting.", "agent");
  } catch (err) {
    const typingEl = document.querySelector(".typing");
    if (typingEl) typingEl.remove();
    appendSystemMessage("⚠️ Error contacting AI agent.");
    console.error(err);
  }
}

// --- Quality of Life: Press Enter to send --- //
document.getElementById("userInput").addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});

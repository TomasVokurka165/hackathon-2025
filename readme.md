# 🕰️ Bridging Worlds: The Deception Game

For DurHack X, our team, ChronoLink (AKA PrintedFewMole) have created a real-time deception game where **one human player** chats with **four AI agents**, each modeled after a different historical figure:

- Ada Lovelace
- Nikola Tesla
- Leonardo da Vinci
- Cleopatra

Each AI believes it is the real historical figure and does not know the others are AI.  
The player’s goal: **convince them that they too are a historical figure**.

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **AI:** DigitalOcean-hosted OpenAI-compatible model
- **Environment Variables:** `.env` for API keys and model endpoint
- **Cache:** Redis or in-memory (for multi-turn conversation memory, post-MVP)
- **Deploy / Test:** DigitalOcean, Docker, ngrok

---

## Flow

1. Player types a message in the frontend chat interface.
2. Frontend sends a POST request to Flask `/chat` endpoint with the message and selected AI agent.
3. Flask constructs a **system prompt** for the selected AI agent using persona data from `data.json`.
4. Flask calls the **DigitalOcean model endpoint** with the prompt and user message.
5. Model returns the AI agent’s reply.
6. Flask sends the reply back to the frontend, which displays it in the chat window.

> **Note:** Each AI agent currently does not maintain conversation memory. Multi-turn memory can be added later using Redis or in-memory storage, iF We hAvE tImEeeeEeEEe (screams internally) :(

---

## Quick Setup

### Clone & Install

```bash
git clone https://github.com/TomasVokurka165/hackathon-2025.git
cd deception-game
python -m venv venv
```

### Activate virtual environment:

#### Linux/Mac:

```bash
source venv/bin/activate
```

#### Windows:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

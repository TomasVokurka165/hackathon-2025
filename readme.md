# 🕰️ Bridging Worlds: The Deception Game

A real-time deception game where one **human player** joins a **TalkJS group chat** with four **AI agents** — each modeled after a different historical figure.  
Each AI believes it’s real and doesn’t know the others are AI.  
The player’s goal: **convince them they’re also a historical figure**.

---

## ⚙️ Stack

- **Frontend:** TalkJS (chat UI)
- **Backend:** Flask (Python)
- **AI:** DigitalOcean-hosted OpenAI-compatible model
- **Cache:** Redis or in-memory
- **Deploy:** DigitalOcean / Docker / ngrok for testing

---

## 🧩 Flow

1. Player sends a message in TalkJS.
2. TalkJS triggers a webhook → Flask endpoint `/webhook/talkjs`.
3. Flask relays the player’s message to each AI agent using its unique persona and message history.
4. Each AI generates a reply via the DigitalOcean model endpoint.
5. Flask sends each agent’s reply back to TalkJS as that persona.
6. Redis (or in-memory cache) maintains per-agent conversation history for context.

---

## 🚀 Quick Setup

### 1️⃣ Clone & Install

```bash
git clone <your-repo-url>
cd deception-game
pip install -r requirements.txt
```

### 2️⃣ Create .env file

```bash
DO_API_KEY=<digitalocean_api_key>
DO_MODEL_URL=<model_endpoint_url>
MODEL_NAME=gpt-4o-mini
TALKJS_APP_ID=<talkjs_app_id>
TALKJS_API_KEY=<talkjs_api_key>
REDIS_URL=redis://localhost:6379/0
```

### 3️⃣ Run Flask App

```bash
python app.py
```

### 4️⃣ Expose Locally (for TalkJS Webhooks)

```bash
ngrok http 8000
```

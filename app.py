from flask import Flask, request, jsonify, render_template
import os
from agent import Agent  # placeholder agent logic
from game import Game  # game logic placeholder

app = Flask(__name__)

# Load environment variables
DO_API_KEY = os.getenv("DO_API_KEY", "")
DO_MODEL_URL = os.getenv("DO_MODEL_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "OpenAI GPT-oss-120b")

# Initialize game object
game = Game()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    player_persona = data.get("playerPersona", "Player")

    # Build prompt for AI or use placeholder
    prompt = f"You are {player_persona}. Respond in character to the following message:\n'{user_message}'"

    if DO_API_KEY and DO_MODEL_URL:
        import requests
        headers = {
            "Authorization": f"Bearer {DO_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"model": MODEL_NAME, "input": prompt}
        try:
            response = requests.post(DO_MODEL_URL, headers=headers, json=payload)
            response.raise_for_status()
            ai_reply = response.json().get("output", "Sorry, I couldn't respond.")
        except Exception as e:
            ai_reply = f"[Error] Could not reach AI: {str(e)}"
    else:
        # Placeholder response for testing frontend without API keys
        ai_reply = f"[Placeholder reply as {player_persona}] You said: '{user_message}'"

    return jsonify({"agent": player_persona, "reply": ai_reply})

@app.route("/select_persona", methods=["POST"])
def select_persona():
    data = request.get_json()
    persona = data.get("persona")
    game.set_player_persona(persona)
    return jsonify({"status": "ok", "persona": persona})

if __name__ == "__main__":
    app.run(debug=True)

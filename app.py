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

    reply = f"Interesting, {player_persona}. You said: '{user_message}' - care to elaborate?"
    return jsonify({"agent": player_persona, "reply": reply})

@app.route("/select_persona", methods=["POST"])
def select_persona():
    data = request.get_json()
    persona = data.get("persona")
    game.set_player_persona(persona)
    return jsonify({"status": "ok", "persona": persona})

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from agent import Agent
from game import Game
import random as r
import json

app = Flask(__name__)

active_agents = {}
active_games = {}
user_message_count = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    persona = data.get("playerPersona")

    if not message or not persona:
        return jsonify({"agent": "System", "reply": "Missing message or persona"}), 400

    # Track message count per persona
    user_message_count[persona] = user_message_count.get(persona, 0) + 1

    historical_figures = initialise_figures()
    persona_map = {
        "Thomas Jefferson": 0,
        "MLK": 1,
        "Albert Einstein": 2,
    }
    i = r.randint(0,2)
    agent = Agent(1, historical_figures[i][1])
    response = agent.get_response(message)

    # Check if it's time to prompt for the game
    count = user_message_count[persona]
    special_prompt = None
    if count % 5 == 0:  # every 5 user messages
        special_prompt = (
            "🎯 You've sent 5 questions! Would you like to keep chatting or start the REAL game?"
        )

    return jsonify({"agent": persona, "reply": response, "specialPrompt": special_prompt})


def initialise_figures():
    with open("historical_figures.json", "r", encoding="utf-8") as js:
        file = json.load(js)
    return {int(key): value for key, value in file["Historical_figures"].items()}


if __name__ == "__main__":
    app.run(debug=True)
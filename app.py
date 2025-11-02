from flask import Flask, request, jsonify, render_template
import os
from agent import Agent  # placeholder agent logic
from game import Game  # game logic placeholder

app = Flask(__name__)

# Temporary in-memory cache to store which persona is active
active_agents = {}

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

    # --- Step 1: Map persona to the corresponding historical figure ID
    persona_map = {
        "Thomas Jefferson": 0,
        "MLK": 1,
        "Albert Einstein": 2,
    }
    hist_id = persona_map.get(persona)

    if hist_id is None:
        return jsonify({"agent": "System", "reply": f"Persona {persona} not recognized."}), 400

    # --- Step 2: Pick one of your DO endpoints (Agent 1/2/3)
    # You can rotate or always use 1 for simplicity.
    agent_id = 1  

    # Create agent only once per session/persona
    if persona not in active_agents:
        active_agents[persona] = Agent(agent_id, hist_id)

    agent = active_agents[persona]

    try:
        # --- Step 3: Get real response from DigitalOcean Agent
        reply = agent.get_response(message)
    except Exception as e:
        print("Agent error:", e)
        return jsonify({"agent": persona, "reply": "⚠️ Error connecting to agent."}), 500

    return jsonify({"agent": persona, "reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

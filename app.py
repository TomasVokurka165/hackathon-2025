from flask import Flask, request, jsonify, render_template
from agent import Agent
from game import Game

app = Flask(__name__)

active_agents = {}
active_games = {}

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

    persona_map = {
        "Thomas Jefferson": 0,
        "MLK": 1,
        "Albert Einstein": 2,
    }
    hist_id = persona_map.get(persona)

    # Create Agent and Game if not yet active
    if persona not in active_agents:
        active_agents[persona] = Agent(1, hist_id)
        active_games[persona] = Game(persona)

    agent = active_agents[persona]
    game = active_games[persona]

    # Step 1: Get game feedback
    game_feedback = game.process_message(message)

    # Step 2: Get agent response
    try:
        agent_reply = agent.get_response(message)
    except Exception as e:
        print("Agent error:", e)
        agent_reply = "⚠️ Error connecting to agent."

    # Step 3: Combine both into a single reply
    full_reply = f"{agent_reply}\n\n🎮 {game_feedback}\n(Score: {game.score})"

    return jsonify({"agent": persona, "reply": full_reply})

if __name__ == "__main__":
    app.run(debug=True)
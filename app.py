import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Load intents / persona data
with open("data.json", "r") as f:
    intents_data = json.load(f)

# Define AI agent personas
AGENTS = {
    "ada": {
        "name": "Ada Lovelace",
        "description": "19th-century mathematician, pioneer of computing, analytical and precise.",
        "example_intents": intents_data["intents"]
    },
    "tesla": {
        "name": "Nikola Tesla",
        "description": "Visionary inventor, expert in electricity and innovation, imaginative and confident.",
        "example_intents": intents_data["intents"]
    },
    "leonardo": {
        "name": "Leonardo da Vinci",
        "description": "Renaissance polymath, artist and scientist, curious and reflective.",
        "example_intents": intents_data["intents"]
    },
    "cleopatra": {
        "name": "Cleopatra",
        "description": "Queen of Egypt, strategic and charismatic leader, commanding and persuasive.",
        "example_intents": intents_data["intents"]
    }
}

# Load DigitalOcean API info
DO_API_KEY = os.getenv("DO_API_KEY")
DO_MODEL_URL = os.getenv("DO_MODEL_URL")
HEADERS = {
    "Authorization": f"Bearer {DO_API_KEY}",
    "Content-Type": "application/json"
}

# Build system prompt for the agent
def build_system_prompt(agent_id):
    agent = AGENTS.get(agent_id)
    examples_text = "\n".join([
        resp
        for intent in agent["example_intents"]
        for resp in intent.get("responses", [])[:2]
    ])
    prompt = (
        f"You are {agent['name']}, {agent['description']}.\n"
        f"Respond in-character naturally and consistently.\n"
        f"Example responses for guidance:\n{examples_text}\n"
        f"User messages will follow. Reply only as {agent['name']}."
    )
    return prompt

# Query DigitalOcean model
def query_model(system_prompt, user_message):
    payload = {
        "input": f"{system_prompt}\nUser: {user_message}\nAI:",
        "max_output_tokens": 150
    }
    try:
        resp = requests.post(DO_MODEL_URL, headers=HEADERS, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("output", data.get("result", "Sorry, I cannot answer that."))
        else:
            return f"[Error: {resp.status_code}] Could not get response from model."
    except Exception as e:
        return f"[Error] {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    agent_id = data.get("agent", "ada")  # default to Ada
    system_prompt = build_system_prompt(agent_id)
    ai_reply = query_model(system_prompt, user_message)
    return jsonify({
        "agent": AGENTS[agent_id]["name"],
        "reply": ai_reply
    })

# Serve as a test endpoint
@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    message = data.get("message", "")
    agent_id = data.get("agent", "ada")
    system_prompt = build_system_prompt(agent_id)
    reply = query_model(system_prompt, message)
    return jsonify({
        "agent": AGENTS[agent_id]["name"],
        "reply": reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

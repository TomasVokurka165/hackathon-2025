import json
import random
from openai import OpenAI



class Agent:
    def __init__(self, id, agent_endpoint, agent_access_key, current_figure, nerves):
        self.id = id
        self.suspicionDictionary = {}
        self.endpoint = agent_endpoint
        self.access_key = agent_access_key
        self.currentFigure = current_figure
        self.nerves = nerves

    def __repr__(self):
        return json.dumps({
            "ID": self.id,
            "OtherPlayers": self.suspicionDictionary,
            "CurrentFigure": self.currentFigure,
            "Nerves": self.nerves
        })

    def intialise_sus_dict(self, list_of_ids):
        for otherIds in list_of_ids:
            self.suspicionDictionary[otherIds] = [0, ""]

    def get_response(self, message):
        # Connect to the Agent.
        client = OpenAI(
            base_url = self.endpoint,
            api_key = self.access_key,
        )

        # Create a chat with the agent, storing its response.
        response = client.chat.completions.create(
            model = "n/a",
            messages= [{"role": "user", "content": f"{message}"}]
        )

        # Getting the content of the response.
        resp = response.choices[0].message.content
        return resp

    def check_suspicion(self, sus_id, message):
        susValue = 0
        susReason = ""
        self.suspicionDictionary[sus_id][0] += susValue
        self.suspicionDictionary[sus_id][1] += " " + message

    def generate_question(self, other_id, sus_level):
        return "question"

    def choose_player(self, sus_level):
        players = list(self.suspicionDictionary.keys())
        weights = list(self.suspicionDictionary.values())[0]
        return random.choices(players, weights=weights, k=1)[0]


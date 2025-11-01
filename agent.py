import json
import random
class Agent:
    def __init__(self, agent_id, current_figure, nerves):
        self.suspicionDictionary = {}
        self.id = agent_id
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
        return "response"

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
from agent import Agent as a
from message import Message as msg
from player import Player as p
from typing import List, Dict, Optional
import json, random

class Game:
    def __init__(self, player_figure: str):
        self.HISTORICAL_FIGURES = self.initialise_figures()
        self.player_figure = player_figure
        self.player_dict = {i: [] for i in range(0, 4)}
        self.host: Optional[a] = None
        self.msg_counter = 0
        self.output_log: List[str] = []   # ← collect dialogue text for web UI
        self.awaiting_player_response = False
        self.current_question = None
        self.current_asking_id = None
        self.current_target_id = None

    def initialise_figures(self):
        with open("historical_figures.json", "r", encoding="utf-8") as js:
            file = json.load(js)
        return {int(key): value for key, value in file["Historical_figures"].items()}

    def initialise_game_state(self):
        called_figures = []
        for i in range(0, 4):
            if i == 0:
                self.player_dict[i] = [self.player_figure, p(self.player_figure), True]
            else:
                randi = random.randint(0, len(self.HISTORICAL_FIGURES) - 2)
                while randi in called_figures:
                    randi = random.randint(0, len(self.HISTORICAL_FIGURES) - 2)
                called_figures.append(randi)
                self.player_dict[i] = [
                    self.HISTORICAL_FIGURES[randi][0],
                    a(i, self.HISTORICAL_FIGURES[randi][1], self.player_dict),
                    True,
                ]

        self.host = a(0, self.HISTORICAL_FIGURES[99][1])
        self.output_log.append("Game initialized with 3 AI agents and you.")
        return True

    # ---------- Gameplay flow ----------

    def start_round(self):
        """Starts a new round. Host asks a random agent a question."""
        self.msg_counter = 0
        self.current_target_id = None
        self.current_asking_id = random.randint(1, len(self.player_dict) - 1)
        string = self.HISTORICAL_FIGURES[99][1]
        formatted_string = string.format(self.player_dict[self.current_asking_id][0])
        question_asked = self.host.get_response(formatted_string)
        self.output_log.append(f"Host: {question_asked}")

        # AI agent responds to the host
        response = self.player_dict[self.current_asking_id][1].get_response(question_asked)
        self.output_log.append(f"{self.player_dict[self.current_asking_id][0]}: {response}")

        # Update suspicion
        for i, player in self.player_dict.items():
            if i != 0 and i != self.current_asking_id and player[2]:
                player[1].check_suspicion(self.current_asking_id, response)

        # Now prepare for the next question
        self.current_asking_id = self.current_asking_id
        self.current_target_id = 0  # now it's the player’s turn
        question = self.player_dict[self.current_asking_id][1].generate_question(self.current_target_id)
        self.current_question = question
        self.awaiting_player_response = True
        self.output_log.append(f"{self.player_dict[self.current_asking_id][0]} asks you: {question}")
        return question

    def handle_player_response(self, player_response: str):
        """Handles the player's answer to the current question."""
        if not self.awaiting_player_response:
            return "No question to answer right now."
        self.output_log.append(f"You: {player_response}")

        # AI agents evaluate your response
        for i, player in self.player_dict.items():
            if i != 0 and player[2]:
                player[1].check_suspicion(0, player_response)

        self.awaiting_player_response = False
        self.msg_counter += 1

        # After player responds → trigger AI-to-AI round
        return self._continue_conversation()

    def _continue_conversation(self):
        """Simulate one more AI-to-AI exchange."""
        asking_id = random.randint(1, len(self.player_dict) - 1)
        target_id = random.randint(1, len(self.player_dict) - 1)
        while target_id == asking_id or not self.player_dict[target_id][2]:
            target_id = random.randint(1, len(self.player_dict) - 1)

        question = self.player_dict[asking_id][1].generate_question(target_id)
        self.output_log.append(f"{self.player_dict[asking_id][0]} asks {self.player_dict[target_id][0]}: {question}")
        response = self.player_dict[target_id][1].get_response(question)
        self.output_log.append(f"{self.player_dict[target_id][0]}: {response}")

        # Update suspicions
        for i, player in self.player_dict.items():
            if i != 0 and i != target_id and player[2]:
                player[1].check_suspicion(target_id, response)

        # Now it’s time for a vote
        return self.vote()

    def vote(self):
        """Simulate the AI voting phase."""
        result_dict = {0: 0, 1: 0, 2: 0, 3: 0}
        for i in range(1, 4):
            result = self.vote_individually(i)
            result_dict[int(result)] += 1

        max_key = max(result_dict, key=result_dict.get)
        self.player_dict[max_key][2] = False

        if max_key == 0:
            self.output_log.append("You were voted out. You lose.")
            return "You lose."
        else:
            self.output_log.append(f"{self.player_dict[max_key][0]} was voted out!")
            alive = [p for p in self.player_dict.values() if p[2]]
            if len(alive) <= 2:
                self.output_log.append("You win! 🎉")
                return "You win!"
            return f"{self.player_dict[max_key][0]} eliminated."

    def vote_individually(self, voter_id):
        agent = self.player_dict[voter_id][1]
        suspicion_dict = agent.get_sus_dict()
        for key in list(suspicion_dict.keys()):
            if not self.player_dict[key][2]:
                suspicion_dict.pop(key)
        response = agent.get_response(
            f"You are asked to vote. This is the data set, where the number before the colon represents the ID and the data after represents suspiciousness and the reason. {suspicion_dict} Use the reasoning and the supicious_value to pick an ID to vote out of the game. A negative suspicious_value means that the person isnt as suspicious and the opposite is true for positive suspicious_values. The only exception is 0, which shows that the person hasnt answered any questions, in which case they should be ignored. The reply should just be the number, this number will be between 0 and 4"
        )
        return response

    def get_log(self):
        """Return recent messages (for Flask to display)."""
        return self.output_log[-10:]
from agent import Agent as a
from message import Message as msg
from player import Player as p
from typing import List, Dict
import json
class Game:
    def __init__(self, ):
        self.gameState = {} #key: id, value: list of key information in the order: name, is still in game

    def initialise_game_state(self, list_of_agents : List[a], player: p):
        self.gameState["0"] = [player.figure, True]
        for agent in list_of_agents:
            self.gameState[agent.id] = [agent.currentFigure, False]

    def update_voted_out(self, votes: Dict[str, int]):
        player_voted_out = max(votes, key=votes.get)
        self.gameState[player_voted_out][1] = False

    def play_round(self, response: msg):
        message = response.





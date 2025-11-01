from agent import Agent
import message as msg
from player import Player
from typing import List
import json
class Game:
    def __init__(self, ):
        self.gameState = {} #key: id, value: list of key information in the order: name, is still in game

    def initialise_game_state(self, list_of_agents : List[Agent], player: Player):
        self.gameState["0"] = [player.figure, True]
        for agent in list_of_agents:
            self.gameState[agent.id] = [agent.currentFigure, False]

    def update_voted_out(self, user_id):
        self.gameState[user_id][1] = False



from agent import Agent as a
from message import Message as msg
from player import Player as p
from typing import List, Dict, Optional, Tuple
import json
import random

class Game:
    def __init__(self, player_figure):
        self.HISTORICAL_FIGURES = self.initialise_figures()
        self.player_figure = player_figure
        # gameState: key=id, value=[name, is_alive]
        self.gameState: Dict[str, List] = {}
        self.player_dict = {i:[] for i in range(0,4)}
        self.agents_by_id: Dict[str, a] = {}
        self.player: Optional[p] = None
        self.msg_counter = 0
        self.host = None


    def initialise_figures(self):
        with open("historical_figures.json", "r", encoding="utf-8") as js:
            file = json.load(js)
        return {int(key):value for key, value in file["Historical_figures"].items()}
        

    # ---------- helpers ----------
    def _next_msg_id(self) -> str:
        self._msg_counter += 1
        return self._msg_counter


    def _actor_by_id(self, actor_id: str):
        # Return Agent or Player instance for id, else None
        if actor_id in self.agents_by_id:
            return self.agents_by_id[actor_id]
        if self.player is not None and getattr(self.player, "id", None) == actor_id:
            return self.player
        return None


    def _alive(self, actor_id: str) -> bool:
        rec = self.gameState.get(actor_id)
        return bool(rec and rec[1])


    # ---------- public API you already stated ----------
    def initialise_game_state(self):

        called_figures = []
        for i in range(0, 4):
            if i == 0:
                self.player_dict[i].append(self.player_figure)
                self.player_dict[i].append(p(self.player_figure))
                self.player_dict[i].append(True)
            else:
                randi = random.randint(0,len(self.HISTORICAL_FIGURES) - 2)
                while randi in called_figures and len(self.player_dict.values()) < 3:
                    print("uwu")
                    print(called_figures)
                    randi = random.randint(0,len(self.HISTORICAL_FIGURES) - 2)   
                    if len(self.player_dict.values()) < 3:
                        break
                called_figures.append(randi)
                
                self.player_dict[i] = [self.HISTORICAL_FIGURES[randi][0], a(i, self.HISTORICAL_FIGURES[randi][1], self.player_dict), True]
        
        self.host = a(0, self.HISTORICAL_FIGURES[99][1])
        self.start_game_loop()


    def start_game_loop(self):
        number_alive = len(self.player_dict.keys())
        while number_alive > 2:
            print(number_alive)
            initial_random_player_id = random.randint(1, len(self.player_dict)-1)
            string = self.HISTORICAL_FIGURES[99][1]
            formatted_string = string.format(self.player_dict[initial_random_player_id][0])
                                            
            question_asked = self.host.get_response(formatted_string)
            print(question_asked)
            response = self.player_dict[initial_random_player_id][1].get_response(question_asked)
            print(response)
            for i, player in self.player_dict.items():
                if i != 0 and i != initial_random_player_id:
                    _, agent, is_alive = player
                    if is_alive:
                        player[1].check_suspicion(initial_random_player_id, response)
                        print(player[1].get_sus_dict())
            asking_id = initial_random_player_id
            target_player_id = -1
            self.msg_counter += 1
            while self.msg_counter < 2:
                print("LENGTH: ", len(self.player_dict.keys()))
                print("asking-id: ", asking_id)
                print("asking-id: ", target_player_id)

                while target_player_id == asking_id or target_player_id < 0 or not self.player_dict[target_player_id][2]:
                    print(len(self.player_dict.keys())- 1)
                    print("TARGET: ", target_player_id)
                    target_player_id = random.randint(0, len(self.player_dict.keys())- 1)
                    
                question = self.player_dict[asking_id][1].generate_question(target_player_id)
                print(f"{self.player_dict[asking_id][0]}: " , question)
                if target_player_id == 0:
                    player_response = input("Answer: ")

                    for i, player in self.player_dict.items():
                        if i != 0 and i != target_player_id:
                            _, agent, is_alive = player

                            if is_alive:
                                agent.check_suspicion(0, player_response)

                    asking_id = random.randint(1, len(self.player_dict.keys()) - 1)

                else:
                    response = self.player_dict[target_player_id][1].get_response(question)
                    print(response)

                    for i, player in self.player_dict.items():

                        if i != 0 and i != target_player_id:
                            _, agent, is_alive = player

                            if is_alive:
                                agent.check_suspicion(target_player_id, response)

                    asking_id = target_player_id
                self.msg_counter += 1

            self.vote()
            for item in self.player_dict.values():
                if item[2]:
                    number_alive -= 1
            print(number_alive)
        print("You won :D")
        quit()

    def vote(self):
        result_dict = {0: 0, 1: 0, 2: 0, 3: 0}
        for i in range(1, 4):
            print(i)
            result = self.vote_individually(i)
            result_dict[int(result)] += 1

        print(result_dict)
        max_key = max(result_dict, key=result_dict.get)
        print(max_key)
        self.player_dict[max_key][2] = False
        if max_key != 0:
            print(self.player_dict)
            return
        else:
            print("You lose :(")
            quit()

    def vote_individually(self, voter_id):
        agent = self.player_dict[voter_id][1]
        print(voter_id)
        suspicion_dict = agent.get_sus_dict()
        print(suspicion_dict)
        key_list = []
        for key in suspicion_dict.keys():
            if not self.player_dict[key][2]:
                key_list.append(key)
        for item in key_list:
            suspicion_dict.pop(item)
        print(suspicion_dict)
        response = agent.get_response(f"You are asked to vote. This is the data set, where the number before the colon represents the ID and the data after represents suspiciousness and the reason. {suspicion_dict} Use the reasoning and the supicious_value to pick an ID to vote out of the game. A negative suspicious_value means that the person isnt as suspicious and the opposite is true for positive suspicious_values. The only exception is 0, which shows that the person hasnt answered any questions, in which case they should be ignored. The reply should just be the number, this number will be between 0 and 4")
        print(response)
        return response


    def update_voted_out(self, votes: Dict[str, int]) -> str:
        # votes keys may be str ids. Convert to int safely.
        def _to_int(k):
            try:
                return int(k)
            except Exception:
                return k  # leave it as-is; will fail lookup if inconsistent

        # Pick highest vote target
        voted_out_key = max(votes, key=votes.get)
        voted_out_id = _to_int(voted_out_key)

        if voted_out_id in self.gameState:
            self.gameState[voted_out_id][1] = False
        return voted_out_id

    def update_suspicion_levels(self, response: msg):
        # Only living agents update, and they skip evaluating the sender
        for agent_id, agent in self.agents_by_id.items():
            if not self._alive(agent_id):
                continue
            if agent_id == response.sender:
                continue
            # Sender may be player or an agent id; Agent.check_suspicion expects an int id and message str
            agent.check_suspicion(response.sender, response.content)

    def answer_question(self, question: msg, senderID, recipientID) -> msg:
        # Validate both are in game and alive
        if not self._alive(recipientID):
            raise ValueError(f"Recipient {recipientID} is not alive in game.")
        if not self._alive(senderID):
            raise ValueError(f"Sender {senderID} is not alive in game.")

        recipient = self._actor_by_id(recipientID)
        if recipient is None:
            raise KeyError(f"No actor found for id {recipientID}.")

        # Get response text. Prefer .get_response if available.
        if hasattr(recipient, "get_response") and callable(recipient.get_response):
            response_text = recipient.get_response(question.content)
        else:
            # Fallback: echo or empty response to avoid breaking flow.
            response_text = ""

        # Build response message
        response_message = msg(
            self._next_msg_id(),
            response_text,
            "answer",
            recipientID,
            senderID
        )

        # Update suspicion based on this answer
        self.update_suspicion_levels(response_message)

        return response_message


main = Game("Marie Curie")
main.initialise_game_state()

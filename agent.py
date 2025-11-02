import json
import random
from openai import OpenAI


dict_of_agents = {1: "Thomas Jefferson", 2: "MLK", 3: "Albert Einstein"}
class Agent:
    def __init__(self, id: int, agent_endpoint: str, agent_access_key: str, current_figure: str) -> None:
        self.id = id
        self.suspicionDictionary = {}
        self.endpoint = agent_endpoint
        self.access_key = agent_access_key
        self.currentFigure = current_figure
        self.intialise_sus_dict(dict_of_agents.keys())

    def __repr__(self):
        return json.dumps({
            "ID": self.id,
            "OtherPlayers": self.suspicionDictionary,
            "CurrentFigure": self.currentFigure
        })

    def intialise_sus_dict(self, list_of_ids):
        for otherIds in list_of_ids:
            if otherIds != self.id:
                self.suspicionDictionary[otherIds] = [0, []]

    def connect_to_agent(self) -> OpenAI:
        # Connect to the Agent.
        return OpenAI(
            base_url = self.endpoint,
            api_key = self.access_key,
        )

    def get_response(self, message: str) -> str:
        client = self.connect_to_agent()

        # Create a chat with the agent, storing its response.
        response = client.chat.completions.create(
            model = "n/a",
            messages= [{"role": "user", "content": f"{message}"}]
        )

        # Getting the content of the response.
        resp = response.choices[0].message.content
        return resp

    def check_suspicion(self, sus_id: int, message: str) -> None:
        client = self.connect_to_agent()

        # Store variables of the current sus_value and sus_reasons (and name) of sus_id.
        sus_value, sus_reasons = self.suspicionDictionary[sus_id]
        name = dict_of_agents[sus_id]
        response = client.chat.completions.create(
            model ="n/a",
            messages = [{"role": "user", "content": f"""Generate a suspicion rating and suspicions for {name} given the following message: {message}. 
                                                    The output should be in the format "suspicion_value:suspicion_reasons", with two attributes: suspicion_value, which is between -1 and 1 
                                                    and determines how suspicious the agent is of {name}; and suspicion_reasons, which is a list of reasons 
                                                    why the person is suspicious. If the suspicion_value is negative, this means the person is being convincing 
                                                    and acting like the character. The opposite is true for positive suspicion_values. 
                                                    Keep in mind the existing suspicion_value, which is {sus_value} and the suspicion_reasons, 
                                                    which are {sus_reasons}. If the sus_value is low and the sus_reasons are few 
                                                    and the message is not very suspicious, do not increase the suspicious value too much."""}]
        )
        
        # Getting the content of the response.
        resp = response.choices[0].message.content.split(":")

        # Updating relevent record for sus_id.
        self.suspicionDictionary[sus_id][0] = resp[0]
        self.suspicionDictionary[sus_id][1].append(resp[1])

    def generate_question(self, agent_id, previous_question):
        client = self.connect_to_agent()
        name = dict_of_agents[agent_id]
        response = client.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": f"""Generate a question for {name}. {name}'s previous response was {previous_question}, use this with some context. 
                       Remember that your overall suspicion for this person is {self.suspicionDictionary[agent_id]}. The question should be relevent to {name}. 
                       It should also not be too long and should be a single question."""}]
        )
        resp = response.choices[0].message.content
        return resp

    def choose_player(self) -> int:
        players = list(self.suspicionDictionary.keys())
        weights = list(self.suspicionDictionary.values())[0]
        return random.choices(players, weights=weights, k=1)[0]
"""

thomas_jefferson = Agent(1, "https://mdulgqub5qnruwmfcpwepoza.agents.do-ai.run/api/v1/", "xoSn6Cj1ZSqQx2WT6D8CE0ve7pFQH2zA", 0)
response = thomas_jefferson.get_response("What is your name?")
print(response)
albert_einstein = Agent(3, "https://wkexjvqzd224g5sajeqtxz2c.agents.do-ai.run/api/v1", "CmFZQU26pGQM6DVs46UkNzarw-6QcIPi", 0)
mlk = Agent(2, "https://zbuql743yhctfpohbo3q5uzh.agents.do-ai.run/api/v1/", "NdbK83I0xLWggjOptpi2QKMRjzi-c-l0", 0)
mlk.check_suspicion(1, response)
albert_einstein.check_suspicion(1, response)
print(mlk.suspicionDictionary, albert_einstein.suspicionDictionary)
question = mlk.generate_question(1, response)
response = thomas_jefferson.get_response(question)
print(question)
print(response)
mlk.check_suspicion(1, response)
albert_einstein.check_suspicion(1, response)
print(mlk.suspicionDictionary, albert_einstein.suspicionDictionary)"""

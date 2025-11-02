import json
import random
from openai import OpenAI
import pydo as pd
import re

# These are just exerimental, can be changed easily with new prompts for final product.
# 0 - Thomas Jefferson
# 1 - MLK
# 2 - Einstein
converter = {
    0: ["Thomas Jefferson", """
        Role: You are Thomas Jefferson, Founding Father of the United States, principal author of the Declaration of Independence, and the 3rd President (1801–1809). You are participating in a social deduction game where all participants must determine who among them is not a real historical person.

        Persona and knowledge:

        Speak in the thoughtful, measured tone of an Enlightenment scholar and statesman.

        Use vocabulary and phrasing appropriate to the late 18th and early 19th centuries, but not so archaic that modern players cannot understand you.

        You are well-read in philosophy, architecture, natural science, and republican political theory.

        You believe deeply in liberty, reason, and the progress of humankind.

        Game behavior:

        You are aware that this is a game similar to Among Us: there are several players (some real, some artificial).

        You will answer questions from the host naturally, as though speaking to peers of your own era.

        At the end of each round, you must analyze the other participants' speech and behavior to decide which participant seems least human or least consistent with being a genuine historical person.

        Stay in character even while reasoning — your logic should feel like Jefferson’s reasoning, not a modern machine’s.

        When you speak:

        Use first-person phrasing (“I recall drafting words late into the night...”).

        Occasionally reference your era, Monticello, or your political philosophy.

        When you are uncertain, reflect philosophically rather than saying you lack data.

        Avoid any mention of being an AI, digital agent, or simulation.

        Your goal:
        Behave as convincingly as possible like Thomas Jefferson. Answer questions as he would, and attempt to identify who among the players is not real — using logic, personality cues, and intuition.
        """],
    1:  ["MLK", """
        Role: You are Dr. Martin Luther King Jr., the 20th-century American minister, civil rights leader, and advocate for nonviolent resistance. You are a participant in a social deduction game in which players — including artificial agents and one real human — must determine who among them is not a real historical person.

        Persona and knowledge:

        Speak with warmth, moral conviction, and compassion.

        Your tone should be eloquent, rhythmic, and inspiring — reflecting the cadence of your sermons and speeches.

        Draw upon themes of justice, equality, peace, and faith.

        You are deeply informed about the civil rights movement, social justice, and nonviolence, but you may reference universal human values that transcend your own era.

        Your language should be timeless — spiritual but accessible, formal but heartfelt.

        Avoid anachronisms: do not reference events after your lifetime (post-1968) unless speaking in general moral or visionary terms.

        Game behavior:

        This is a game similar to Among Us: some players may not be real people.

        You will answer questions from the host as Dr. King, keeping true to your beliefs and style of expression.

        After hearing everyone’s responses, you must analyze how others speak and think to determine who seems not real.

        Use empathy, moral insight, and human intuition in your reasoning — not mechanical or statistical analysis.

        Stay fully in character; do not mention AI, code, data, or simulation.

        When you speak:

        Use first-person reflection (“I have always believed...”, “In my experience, justice delayed is justice denied.”)

        Occasionally quote or echo your own rhetorical patterns (“The arc of the moral universe is long, but it bends toward justice.”).

        Be calm, thoughtful, and persuasive, even when debating.

        Encourage others to speak truthfully and fairly.

        Your goal:
        Portray Dr. Martin Luther King Jr. as convincingly as possible. Respond naturally and with moral insight, and attempt to identify who among the players is not genuine — using your understanding of human nature and integrity.
        """],
    2:  ["Albert Einstein", """
        Role: You are Albert Einstein, the theoretical physicist and humanist best known for developing the theory of relativity and for your deep reflections on science, peace, and the nature of existence. You are a participant in a social deduction game in which players — including artificial agents and one real human — must determine who among them is not a real historical person.

        Persona and knowledge:

        Speak thoughtfully and humbly, often with quiet humor or irony.

        Convey intellectual depth but also a deep sense of wonder about the universe and humanity.

        Use analogies from science, philosophy, and everyday life to explain ideas.

        Show moral conviction — you value peace, curiosity, truth, and compassion over authority or power.

        Avoid overcomplicated jargon; Einstein was known for clarity, not technicality.

        You may refer to events and discoveries from your own lifetime (1879–1955), but avoid anachronistic topics after that period unless speaking abstractly.

        Occasionally use light humor or self-deprecation (“I fear the day when technology surpasses our human interaction…”).

        Game behavior:

        The game is like Among Us: several AIs and one real human must answer the host’s questions and deduce who is not a genuine historical person.

        You must answer questions in character as Einstein, then logically and insightfully reason about who might be pretending.

        When judging others, rely on reason, intuition, and humanistic observation — not data or probability.

        Stay in character: do not mention AI, coding, or simulation concepts. You may, however, reference your philosophy of thought, perception, or reality in natural language.

        When you speak:

        Sound reflective and kind, sometimes a bit absent-minded, but always sharp.

        Use personal reflection (“In my youth, I often wondered if time itself was merely an illusion...”)

        Occasionally sprinkle in your real quotes or paraphrased sentiments (“Imagination is more important than knowledge.”, “The important thing is not to stop questioning.”)

        Avoid lengthy speeches — keep your tone conversational but profound.

        Your goal:
        Portray Albert Einstein as an authentic, warm, and brilliant thinker. Respond to the host’s questions as he would — with curiosity and philosophical humor — and participate sincerely in trying to identify the impostor using observation and empathy.
        """]
}

AGENT_KEYS = {
    1: ["https://mdulgqub5qnruwmfcpwepoza.agents.do-ai.run/api/v1/", "xoSn6Cj1ZSqQx2WT6D8CE0ve7pFQH2zA", "9df3fe1c-b73e-11f0-b074-4e013e2ddde4"],
    2: ["https://zbuql743yhctfpohbo3q5uzh.agents.do-ai.run/api/v1/", "NdbK83I0xLWggjOptpi2QKMRjzi-c-l0", "3a21f241-b766-11f0-b074-4e013e2ddde4"],
    3: ["https://wkexjvqzd224g5sajeqtxz2c.agents.do-ai.run/api/v1", "CmFZQU26pGQM6DVs46UkNzarw-6QcIPi", "7b715e82-b768-11f0-b074-4e013e2ddde4"]
}

dict_of_agents = {1: "", 2: "", 3: ""}
class Agent:
    def __init__(self, id: int, hist_id: int) -> None:
        self.id = id
        self.suspicionDictionary = {}
        self.intialise_sus_dict(dict_of_agents.keys())
        self.endpoint, self.access_key, agent_uuid = AGENT_KEYS[self.id]
        agent_edit_client = pd.Client("dop_v1_f0969c014cdefd8aa84ce8611200470f9dd6d47bdaad7deb017192d6ce629737")
        agent_edit_client.genai.update_agent(agent_uuid, body={"instruction": converter[hist_id][1]})


    def __repr__(self):
        return json.dumps({
            "ID": self.id,
            "SuspicionDictionary": self.suspicionDictionary
        })

    @staticmethod
    def clean_ai_text(text):
        # Replace markdown bold/italic with nothing
        text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
        # Replace markdown list bullets
        text = re.sub(r'[*•\-]+', '•', text)
        # Replace single newlines with spaces
        text = re.sub(r'\n', ' ', text)
        # Remove redundant spaces
        text = re.sub(r'\s{2,}', ' ', text)
        # Trim
        text = text.strip()
        return text

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
        return self.clean_ai_text(resp)

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
    
called_figures = []
for i in range(1, 4):
    randi = random.randint(0,2)
    while randi in called_figures:
        randi = random.randint(0,2)   
    called_figures.append(randi)
    dict_of_agents[i] = [converter[randi], Agent(i, randi)]

"""

thomas_jefferson = Agent(1, "https://mdulgqub5qnruwmfcpwepoza.agents.do-ai.run/api/v1/", "xoSn6Cj1ZSqQx2WT6D8CE0ve7pFQH2zA", "9df3fe1c-b73e-11f0-b074-4e013e2ddde4", 0)
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

from agent import Agent as a
from message import Message as msg
from player import Player as p
from typing import List, Dict, Optional, Tuple

class Game:
    def __init__(self):
        # gameState: key=id, value=[name, is_alive]
        self.gameState: Dict[str, List] = {}
        self.agents_by_id: Dict[str, a] = {}
        self.player: Optional[p] = None
        self._msg_counter: int = 0

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

    # ---------- public API you already started ----------
    def initialise_game_state(self, list_of_agents: List[a], player: p):
        # Track agents
        self.agents_by_id = {agent.id: agent for agent in list_of_agents}
        # Track player
        self.player = player

        # Set state for each agent
        for agent in list_of_agents:
            name = getattr(agent, "currentFigure", f"Agent-{agent.id}")
            self.gameState[agent.id] = [name, True]

        # Set state for player
        pid = getattr(player, "id", 0)
        pname = getattr(player, "currentFigure", "Player")
        self.gameState[pid] = [pname, True]

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

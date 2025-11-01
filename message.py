import json
class Message:
    def __init__(self, msg_id, content, msg_type, sender, receiver):
        self.id = msg_id
        self.content = content
        self.type = msg_type
        self.sender = sender
        self.receiver = receiver

    def __repr__(self):
        return json.dumps({
            "ID": self.id,
            "Content": self.content,
            "Type": self.type,
            "Sender": self.sender,
            "Receiver": self.receiver
        })



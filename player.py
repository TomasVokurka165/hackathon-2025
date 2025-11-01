import json
class Player:
    def __init__(self, figure):
        self.figure = figure

    def __repr__(self):
        return json.dumps({
            "Figure": self.figure,
        })
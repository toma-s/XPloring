class Room:

    def __init__(self, data: dict):
        self.alias = data['alias']
        self.description = data['description']
        self.directions = data['directions']
        self.items = data['items']
        self.creatures = data['creatures']
        self.auto_actions = None
        if "auto_actions" in data:
            self.auto_actions = data["auto_actions"]

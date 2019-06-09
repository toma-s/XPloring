class Room:

    def __init__(self, data: dict):
        self.alias = data['alias']
        self.description = data['description']
        self.directions = data['directions']
        self.items = data['items']
        self.creatures = data['creatures']
        self.auto_commands = None
        if "auto_commands" in data:
            self.auto_commands = data["auto_commands"]

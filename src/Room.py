class Room:

    def __init__(self, data: dict):
        self.description = data['description']
        self.directions = data['directions']
        self.items = data['items']
        self.creature = data['creature']
        self.auto_commands = None
        if "auto_commands" in data:
            self.auto_commands = data["auto_commands"]

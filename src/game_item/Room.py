class Room:

    room_actions = {
        "go": {
            "command_move_direction": None
        }
    }

    def __init__(self, data: dict):
        self.alias = data['alias']
        self.description = data['description']
        self.directions = data['directions']
        self.items = data['items']
        self.creatures = data['creatures']
        self.actions = self.room_actions.copy()
        self.actions.update(data['actions'])
        self.auto_commands = data["auto_commands"]

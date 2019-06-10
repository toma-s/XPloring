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
        self.actions = data['actions']
        self.actions.update(self.room_actions)
        self.auto_actions = dict()
        if "auto_actions" in data:
            self.auto_actions = data["auto_actions"]

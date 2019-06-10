class TransitionObject:

    trans_obj_actions = {
        "examine": {
            "command_show_description": None
        }
    }

    def __init__(self, data: dict):
        self.alias = data['alias']
        self.locked = data['locked']
        self.description = data['description']
        self.actions = data['actions']
        self.actions.update(self.trans_obj_actions)

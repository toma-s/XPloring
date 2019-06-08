
class Item:

    item_actions = {
        "take": {
            "command_add_item_to_inventory": None
        },
        "examine": {
            "command_show_description": None
        }
    }

    def __init__(self, data: dict):
        super().__init__()
        self.alias = data['alias']
        self.description = data['description']
        self.actions = data['actions']
        self.actions.update(self.item_actions)

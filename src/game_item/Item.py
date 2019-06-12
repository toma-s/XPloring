class Item:
    item_actions = {
        "examine": {
            "command_show_description": None
        },
        "take": {
            "command_despawn_items": None,
            "command_add_items_to_inventory": None
        },
        "drop": {
            "command_drop_item": None
        }
    }

    def __init__(self, data: dict):
        super().__init__()
        self.alias = data['alias']
        self.description = data['description']
        self.actions = self.item_actions.copy()
        self.actions.update(data['actions'])

from game_item.Item import Item


class Equipment(Item):

    default_actions = {
        "equip": {
            "command_equip": None
        }
    }

    def __init__(self, data: dict):
        super().__init__(data)
        self.slot = data['slot']  # what equipment slot does this game_item fit
        self.in_use = data['in_use']  # is game_item currently equipped
        self.actions.update(self.default_actions)



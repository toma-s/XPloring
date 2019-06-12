from game_item.Item import Item


class Equipment(Item):
    equipment_actions = {
        "equip": {
            "command_equip": None
        },
        "unequip": {
            "command_unequip": None
        }
    }

    def __init__(self, data: dict):
        super().__init__(data)
        self.slot = data['slot']  # what equipment slot does this game_item fit
        self.actions.update(self.equipment_actions)

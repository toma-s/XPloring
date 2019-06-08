from game_item.Item import Item


class Equipment(Item):
    def __init__(self, data: dict):
        super().__init__(data)
        self.slot = data['slot']  # what equipment slot does this game_item fit
        self.in_use = data['in_use']  # is game_item currently equipped

from game_item.Item import Item


class Consumable(Item):
    def __init__(self, data: dict):
        super().__init__(data)
        self.value = data["value"]
from game_item.Equipment import Equipment


class Armour(Equipment):

    def __init__(self, data: dict):
        super().__init__(data)
        self.resistance = data["resistance"]
        self.durability = data["durability"]

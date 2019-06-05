from game_item.Equipment import Equipment


class Weapon(Equipment):

    def __init__(self, data: dict):
        super().__init__(data)
        self.damage = data["damage"]

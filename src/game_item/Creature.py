class Creature:
    def __init__(self, data: dict):
        self.description = data['description']
        self.alias = data['alias']
        self.health = data['health']
        self.damage = data['damage']
        self.drops = data['drops']

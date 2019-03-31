class Equipment:
    def __init__(self, data: dict):
        self.alias = data['alias']
        self.damage = data['damage']
        self.description = data['description']

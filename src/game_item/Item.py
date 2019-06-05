class Item:
    def __init__(self, data: dict):
        self.alias = data['alias']
        self.description = data['description']
        self.actions = data['actions']

class TransitionObject:
    def __init__(self, data: dict):
        self.alias = data['alias']
        self.unlocked = data['unlocked']
        self.description = data['description']
        self.actions = data['actions']

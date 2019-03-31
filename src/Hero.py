class Hero:

    def __init__(self, data: dict):
        self.health = data['health']
        self.location = data['location']
        self.actions = data['actions']


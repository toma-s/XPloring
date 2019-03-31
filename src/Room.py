class Room:

    def __init__(self, data: dict):
        self.description = data['description']
        self.directions = data['directions']
        self.items = data['items']
        self.creature = data['creature']

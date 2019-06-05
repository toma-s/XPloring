class Hero:

    def __init__(self, data: dict):
        self.health = data['health']
        self.location = data['location']
        self.right_hand = data['right_hand']
        self.left_hand = data['left_hand']
        self.head = data['head']
        self.chest = data['chest']
        self.legs = data['legs']
        self.actions = data['actions']
        self.achievements = data['achievements']
        self.number_of_letters = data['number_of_letters']
        self.inventory = data['inventory']
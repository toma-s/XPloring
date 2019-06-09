class Hero:

    hero_actions = {
        "go": {
            "command_move_direction": None
        },
        "look": {
            "command_show_room": None
        },
        "status": {
            "command_show_status": None
        },
        "inventory": {
            "command_show_inventory": None
        }
    }

    def __init__(self, data: dict):
        self.health = data['health']
        self.damage = data['damage']
        self.location = data['location']
        self.right_hand = data['right_hand']
        self.left_hand = data['left_hand']
        self.head = data['head']
        self.chest = data['chest']
        self.legs = data['legs']
        self.inventory = data['inventory']
        self.actions = data['actions']
        self.actions.update(self.hero_actions)



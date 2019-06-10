class Hero:

    hero_actions = {
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
        self.base_damage = data['base_damage']
        self.location = data['location']
        self.weapon_slot = data['weapon_slot']
        self.head_slot = data['head_slot']
        self.chest_slot = data['chest_slot']
        self.legs_slot = data['legs_slot']
        self.inventory = data['inventory']
        self.actions = data['actions']
        self.actions.update(self.hero_actions)



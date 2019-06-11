class Creature:

    creature_actions = {
        "attack": {
            "command_attack_creature": None
        },
        "examine": {
            "command_show_description": None
        }
    }

    def __init__(self, data: dict):
        self.description = data['description']
        self.alias = data['alias']
        self.health = data['health']
        self.damage = data['damage']
        self.drops = data['drops']
        self.actions = self.creature_actions.copy()
        self.actions.update(data['actions'])

class Equipment:
    def __init__(self, data: dict):
        self.alias = data['alias']
        self.description = data['description']
        self.slot = data['slot']  # what equipment slot does this item fit
        self.in_use = data['in_use']  # is item currently equipped 

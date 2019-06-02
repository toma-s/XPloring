commands_directions = {
    "north": {},
    "west": {},
    "east": {},
    "south": {}
}

commands_actions = {
    "use": {"accept", "apply", "handle"},
    "eat": {"drink", "feed", "chew"},
    "attack": {"hit", "kill", "destroy"},
    "open": {"release"},
    "go": {"run", "move"},
    "take": {"pick", "lift", "get"},
    "look": {"check", "observe"},
    "inventory": {"inv"}
}

command_rules = {
    "go": (1, commands_directions.keys()),
}

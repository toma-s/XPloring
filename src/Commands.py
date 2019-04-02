commands_directions = {
    "north": {},
    "west": {},
    "east": {},
    "south": {}
}

commands_actions = {
    "use": {"accept", "apply", "handle"},
    "eat": {"drink", "feed", "chew"},
    "attack": {"hit", "kill"},
    "open": {"release"},
    "go": {"run", "move"},
    "take": {"pick", "lift", "get"},
    "look": {"check"}
}

command_rules = {
    "go": (1, commands_directions.keys()),
}

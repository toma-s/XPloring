from src.GameState import GameState
from src.Commands import commands_directions, commands_actions, words_ignore
from src.Room import Room
from src.Item import Item


class InputHandle:

    def __init__(self, map: GameState):
        self.gs = map

    def parse_user_input(self, input):
        x = input.strip().split(" ")

        for i in range(len(x)):
            tmp = self.check_word(x[i])
            if tmp:
                x[i] = tmp

        return x

    def check_word(self, word):
        if word in commands_actions or word in commands_directions:
            return word

        for command in commands_actions:
            if word in commands_actions[command]:
                return command

        return None

    # ==============================================================================

    def single_command(self, command):
        if command in self.gs.hero.actions:
            com = self.gs.hero.actions[command].replace(",", '').split(" ")
            if com[0] == "display":
                if com[1] == "room":
                    self.display(self.gs.rooms[self.gs.hero.location])
                    return

        print("You are unsure about yourself. (wrong command)")

    def double_command(self, action, target):
        if action in self.gs.hero.actions:
            com = self.gs.hero.actions[action].replace(",", '').split(" ")
            if com[0] == "display":
                if com[1] == "item":
                    item = None
                    for it in self.gs.items:
                        if target in self.gs.items[it].alias:
                            item = self.gs.items[it]
                            break
                    if item:
                        self.display(item)

            elif com[0] == "move_to":
                if com[1] == "direction":
                    if target in self.gs.rooms[self.gs.hero.location].directions:
                        room_id = self.gs.rooms[self.gs.hero.location].directions[target]["room_id"]

                        my_direction = self.gs.rooms[self.gs.hero.location].directions[target]

                        if "env_obj_id" in my_direction:
                            env_obj = self.gs.environment_objects[my_direction["env_obj_id"]]
                            if not env_obj.unlocked:
                                print(env_obj.description)
                            else:
                                self.move_to(room_id)
                        else:
                            self.move_to(room_id)
                    else:
                        print("You cant go there.")

            elif com[0] == "item_take":
                if com[1] == "item":
                    item = None
                    for it in self.gs.items:
                        if target in self.gs.items[it].alias:
                            item = self.gs.items[it]
                            break

                    if not item:
                        for it in self.gs.equipment:
                            if target in self.gs.equipment[it].alias:
                                item = self.gs.equipment[it]
                                break
                    if item:
                        print(f"Taking {target} with me.")

            elif com[0] == "hit":
                if com[1] == "creature":
                    cr = None
                    for creature in self.gs.rooms[self.gs.hero.location].creature:
                        if target in self.gs.creatures[creature].alias:
                            cr = self.gs.creatures[creature]
                            break

                    if cr:
                        print(f"You hit {target}!")
                    else:
                        print(f"There's no such thing as {target}.")

        else:
            int_commands = None
            for it in self.gs.items:
                if target in self.gs.items[it].alias and action in self.gs.items[it].actions:
                    int_commands = self.gs.items[it].actions[action]
                    break
            if int_commands:
                self.run_internal_command(int_commands)

    def run_commands(self, commands):
        commands = [x for x in commands if x not in words_ignore]
        if len(commands) == 1:
            self.single_command(commands[0])
        elif len(commands) == 2:
            self.double_command(commands[0], commands[1])

    def discover_room(self):
        room = self.gs.rooms[self.gs.hero.location]

        # items in room
        for i in room.items:
            if i in self.gs.items:
                print(f"There is {self.gs.items[i].alias[0]} {self.gs.items[i].description}")
            elif i in self.gs.equipment:
                print(f"There is {self.gs.equipment[i].alias[0]} {self.gs.equipment[i].description}")

        # entities in room
        if not room.creature:
            print("Nothing scary here")
        else:
            for c in room.creature:
                print(f"There is a {self.gs.creatures[c].alias[0]} here. {self.gs.creatures[c].description}")

        # direction from room
        for d in room.directions:
            print(f"You can go {d.upper()}")

    def examine_item(self, item):
        print(f"{item.description}")

    def display(self, obj):
        if isinstance(obj, Room):
            self.discover_room()
        elif isinstance(obj, Item):
            self.examine_item(obj)
        else:
            print(obj)

    def move_to(self, room_id):
        self.gs.hero.location = room_id

        print(f"You entered: {self.gs.rooms[room_id].description}")

    def run_internal_command(self, commands):
        print(f"[DEBUG] running internal - {commands}")
        for c in commands:
            if c == "command_spawn_item":
                self.spawn_item(commands[c])
            if c == "command_display":
                self.display(commands[c])

    def spawn_item(self, item_id):
        room = self.gs.rooms[self.gs.hero.location]
        if item_id not in room.items:
            print(f"You found {self.gs.items[item_id].alias[0]} - {self.gs.items[item_id].description}")
            room.items.append(item_id)
        else:
            print(f"You already did this")

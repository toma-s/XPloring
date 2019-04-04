from src.GameState import GameState
from src.Room import Room
from src.Item import Item


class CommandRunner:

    def __init__(self, map: GameState):
        self.game_state = map

    def single_command(self, command):
        hero = self.game_state.hero
        rooms = self.game_state.rooms

        if command in hero.actions:
            verb, noun = tuple(hero.actions[command].replace(",", '').split(" "))
            if verb == "display":
                if noun == "room":
                    self.display(rooms[hero.location])
                    return

        print("I don't understand. Try again.")

    def double_command(self, action, target):

        hero = self.game_state.hero

        if action in hero.actions:
            verb, noun = tuple(hero.actions[action].replace(",", "").split(" "))
            if verb == "display":
                if noun == "item":
                    self._display_item(target)

            elif verb == "move_to":
                if noun == "direction":
                    self._move_to_direction(target)

            elif verb == "item_take":
                if noun == "item":
                    self._item_take(target)

            elif verb == "hit":
                if noun == "creature":
                    self._hit_creature(target)

        else:
            int_commands = None
            for it in self.game_state.rooms[self.game_state.hero.location].items:
                if it in self.game_state.items and target in self.game_state.items[it].alias and action in \
                        self.game_state.items[it].actions:
                    int_commands = self.game_state.items[it].actions[action]
                    break
            if int_commands:
                self.run_internal_command(int_commands)

    def _display_item(self, target):
        items = self.game_state.items

        item = None
        for it in items:
            if target in items[it].alias:
                item = items[it]
                break
        if item:
            self.display(item)

    def _move_to_direction(self, target):
        hero = self.game_state.hero
        rooms = self.game_state.rooms
        environment_objects = self.game_state.environment_objects

        if target in rooms[hero.location].directions:
            room_id = rooms[hero.location].directions[target]["room_id"]

            my_direction = rooms[hero.location].directions[target]

            if "env_obj_id" in my_direction:
                env_obj = environment_objects[my_direction["env_obj_id"]]
                if not env_obj.unlocked:
                    print(env_obj.description)
                else:
                    self.move_to(room_id)
            else:
                self.move_to(room_id)
        else:
            print(f"You are not allowed to go {target}.")

    def _item_take(self, target):
        items = self.game_state.items
        equipment = self.game_state.equipment

        item = None
        for it in items:
            if target in items[it].alias:
                item = items[it]
                break

        if not item:
            for it in equipment:
                if target in equipment[it].alias:
                    item = equipment[it]
                    break
        if item:
            print(f"You grabbed the {target}.")

    def _hit_creature(self, target):
        rooms = self.game_state.rooms
        creatures = self.game_state.creatures
        hero = self.game_state.hero

        spotted_creature = None
        for creature in rooms[hero.location].creature:
            if target in creatures[creature].alias:
                spotted_creature = creatures[creature]
                break

        if spotted_creature:
            print(f"You hit the {target}!")
        else:
            print(f"There's no such thing as {target}.")

    def execute(self, commands):
        ignored = {"the", "on", "a", "an", "this", "that"}
        commands = [command for command in commands if command not in ignored]
        if len(commands) == 1:
            self.single_command(commands[0])
        elif len(commands) == 2:
            self.double_command(commands[0], commands[1])

    def discover_room(self):
        items = self.game_state.items
        equipment = self.game_state.equipment
        creatures = self.game_state.creatures
        room = self.game_state.rooms[self.game_state.hero.location]

        # items in room
        for i in room.items:
            if i in items:
                print(f"There is a {items[i].alias[0]}. {items[i].description}.")
            elif i in equipment:
                print(f"There is a {equipment[i].alias[0]}. It's {equipment[i].description.lower()}.")

        # entities in room
        if not room.creature:
            print("There's nothing scary here.")
        else:
            for c in room.creature:
                print(f"There is a {creatures[c].alias[0]} here. It's {creatures[c].description}.")

        # direction from room
        for d in room.directions:
            print(f"You can GO {d.upper()}.")

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
        self.game_state.hero.location = room_id
        rooms = self.game_state.rooms
        print(f"You entered {rooms[room_id].description.lower()}")

    def run_internal_command(self, commands):
        # print(f"[DEBUG] running internal - {commands}")
        for c in commands:
            if c == "command_spawn_item":
                self.spawn_item(commands[c])
            if c == "command_display":
                self.display(commands[c])

    def spawn_item(self, item_id):
        items = self.game_state.items
        room = self.game_state.rooms[self.game_state.hero.location]
        if item_id not in room.items:
            print(f"You found {items[item_id].alias[0]}. {items[item_id].description}.")
            room.items.append(item_id)
        else:
            print(f"You already did this.")

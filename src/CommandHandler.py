from Finder import Finder
from InternalCommandHandler import InternalCommandHandler
from commands import commands_directions
from src.GameState import GameState
from game_item.Weapon import Weapon
from game_item.Armour import Armour


class CommandHandler:

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        # TODO
        self.internal_command_handler = InternalCommandHandler(game_state)
        self.finder = Finder(game_state)

    def single_command(self, action_name):
        hero = self.game_state.hero

        if action_name in hero.actions:
            verb, noun = tuple(hero.actions[action_name].replace(",", '').split(" "))
            if verb == "display":
                if noun == "room":
                    self.discover_room()
                    return
                if noun == "inventory":
                    self.show_inventory()
                    return
                if noun == "self":
                    self.show_status()
                    return

        print("You don't know how to do that.")

    def double_command(self, action_name, target_alias):
        hero = self.game_state.hero

        # if action_name in hero.actions:
        #     self._handle_hero_action(action_name, target_alias)
        #     return
        # TODO hero.actions (go, inventory, status)
        if action_name == "go":
            self._move_to_direction(target_alias)
            return

        if self._is_keyword(target_alias):
            print(f"This action is not allowed with the {target_alias}.")
            return
        found_ids = self.finder.find_ids_by_alias(target_alias)
        if not self._check_found_one_id_only(found_ids, target_alias):
            return

        target_id = found_ids[0]
        data = self.finder.get_data_by_id(target_id)

        if data is None or action_name not in data.actions:
            print(f"Action \"{action_name}\" is not allowed with the {target_alias}.")
            return

        action_data = data.actions[action_name]
        self.internal_command_handler.handle_internal_command(action_data, target_id)

    def _handle_hero_action(self, action_name, target_alias):
        hero = self.game_state.hero
        verb, noun = tuple(hero.actions[action_name].replace(",", "").split(" "))

        if verb == "move_to":
            if noun == "direction":
                self._move_to_direction(target_alias)
        else:
            print(f"You don't know how to {action_name}")

    def _check_found_one_id_only(self, ids, target_alias) -> bool:
        if len(ids) == 0:
            print(f"There is no such thing as {target_alias}.")
            return False
        if len(ids) > 1:
            print(f"There are {len(ids)} \"{target_alias}\". You have to be more specific.")
            return False
        return True

    def discover_room(self):
        items = self.game_state.items
        equipment = self.game_state.equipment
        creatures = self.game_state.creatures
        room = self.game_state.rooms[self.game_state.hero.location]

        # items in room
        for i in room.items:
            if i in items:
                print(f"There is a {items[i].alias[0]}. {self._capitalize_first(items[i].description)}.")
            elif i in equipment:
                print(f"There is a {equipment[i].alias[0]}. {self._capitalize_first(equipment[i].description)}.")

        # entities in room
        if not room.creatures:
            print("There's nothing scary here.")
        else:
            for c in room.creatures:
                print(f"There is a {creatures[c].alias[0]} here. {self._capitalize_first(creatures[c].description)}.")

        # direction from room
        for d in room.directions:
            print(f"You can GO {d.upper()}.")

    def _move_to_direction(self, direction_name):
        hero = self.game_state.hero
        rooms = self.game_state.rooms
        transition_objects = self.game_state.transition_objects

        if direction_name in rooms[hero.location].directions:
            room_id = rooms[hero.location].directions[direction_name]["room_id"]

            direction_data = rooms[hero.location].directions[direction_name]

            if "trans_obj_id" in direction_data:
                trans_obj = transition_objects[direction_data["trans_obj_id"]]
                if not trans_obj.unlocked:
                    print(trans_obj.description)
                else:
                    self.move_to(room_id)
            else:
                self.move_to(room_id)
        else:
            print(f"You are not allowed to go {direction_name}.")

    def execute(self, commands):
        ignored = {"the", "on", "a", "an", "this", "that"}
        commands = [command for command in commands if command not in ignored]
        action_name = commands[0]
        target_alias = " ".join(commands[1:])
        if len(commands) == 1:
            self.single_command(action_name)
        else:
            self.double_command(action_name, target_alias)

    def move_to(self, room_id):
        self.game_state.hero.location = room_id
        rooms = self.game_state.rooms
        print(f"{rooms[room_id].description}")
        if rooms[room_id].auto_commands is not None:
            self.internal_command_handler.handle_internal_command(rooms[room_id].auto_commands, room_id)

    def show_status(self):
        hero = self.game_state.hero
        print(f"----- HERO STATUS -----")
        print(f"Health: {hero.health}HP")
        tmp = "none"
        if hero.right_hand != "none":
            it = self.game_state.equipment[hero.right_hand]
            tmp = it.description
            tmp += f" {it.damage} ATK"
        print(f"Right hand: {tmp}")
        tmp = "none"
        if hero.head != "none":
            it = self.game_state.equipment[hero.head]
            tmp = it.description
            tmp += f" {it.resistance} DEF"
            tmp += f" {it.durability} Durability"
        print(f"Head: {tmp}")
        tmp = "none"
        if hero.chest != "none":
            it = self.game_state.equipment[hero.chest]
            tmp = it.description
            tmp += f" {it.resistance} DEF"
            tmp += f" {it.durability} Durability"
        print(f"Chest: {tmp}")
        tmp = "none"
        if hero.legs != "none":
            it = self.game_state.equipment[hero.legs]
            tmp = it.description
            tmp += " {it.resistance} DEF"
            tmp += f" {it.durability} Durability"
        print(f"Leg: {tmp}")
        print(f"For inventory detail type INV")
        print(f"-----------------------")

    def show_inventory(self):
        hero = self.game_state.hero
        if len(hero.inventory) == 0:
            print(f"Your inventory is empty")
            return

        for item in hero.inventory:
            if item in self.game_state.items:
                it = self.game_state.items[item]
            else:
                it = self.game_state.equipment[item]
            res = f"{it.alias[0]} - {it.description}"
            if isinstance(it, Armour) or isinstance(it, Weapon):
                if it.in_use:
                    res += " [EQUIPPED]"
            print(res)


    @staticmethod
    def _capitalize_first(input: str):
        return input[0].capitalize() + input[1:]

    @staticmethod
    def _is_keyword(target_alias):
        if target_alias == "inventory":
            return True
        if target_alias in commands_directions:
            return True

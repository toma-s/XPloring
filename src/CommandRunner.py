from game_item.EnvironmentObject import EnvironmentObject
from src.GameState import GameState
from game_item.Room import Room
from game_item.Item import Item
from game_item.Consumable import Consumable
from game_item.Weapon import Weapon
from game_item.Armour import Armour


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
                if noun == "inventory":
                    self.display("inventory")
                    return
                if noun == "self":
                    self.display("status")
                    return
            elif verb == "heal":
                if noun == "self":
                    self.heal()
                    return

        print("I don't understand. Try again.")

    def double_command(self, action_name, target_alias):
        hero = self.game_state.hero
        hero_room = self.game_state.rooms[hero.location]

        if action_name in hero.actions:
            self._handle_hero_action(action_name, target_alias)
            return

        self._handle_target_action(action_name, target_alias)

    def _handle_hero_action(self, action, target_alias):
        hero = self.game_state.hero
        verb, noun = tuple(hero.actions[action].replace(",", "").split(" "))
        if verb == "display":
            if noun == "game_item":
                self._display_item(target_alias)

        elif verb == "move_to":
            if noun == "direction":
                self._move_to_direction(target_alias)

        elif verb == "item_take":
            if noun == "game_item":
                self._item_take(target_alias)

        elif verb == "hit":
            if noun == "creature":
                self._hit_creature(target_alias)

        elif verb == "equip":
            if noun == "game_item":
                self._equip_item(target_alias)

    def _env_object_action(self, action_name, env_obj_id):
        obj = self.game_state.environment_objects[env_obj_id]
        if action_name == "unlock" and obj.unlocked:
            print(f"Already unlocked.")
            return
        int_commands = obj.actions[action_name]
        if int_commands:
            self.run_internal_command(int_commands, env_obj_id)

    def _handle_target_action(self, action_name, target_alias):
        ids = self._find_ids_by_alias(target_alias)

        if not self._check_found_one_id_only(ids, target_alias):
            return

        id = ids[0]
        data = None
        if id in self.game_state.items:
            data = self.game_state.items[id]
        elif id in self.game_state.environment_objects:
            data = self.game_state.environment_objects[id]
        if data is None or action_name not in data.actions:
            print(f"Action \"{action_name}\" is not allowed with \"{target_alias}\".")
            return

        action = data.actions[action_name]
        self.run_internal_command(action, id)

    def _find_env_obj_ids_by_alias(self, target_alias) -> [str]:
        foundIds = []

        hero = self.game_state.hero
        hero_room = self.game_state.rooms[hero.location]

        for direction in hero_room.directions:
            if "env_obj_id" in hero_room.directions[direction]:
                env_obj_id = hero_room.directions[direction]["env_obj_id"]
                env_obj_data: EnvironmentObject = self.game_state.environment_objects[env_obj_id]
                if target_alias in env_obj_data.alias:
                    foundIds.append(env_obj_id)
        return foundIds

    def _find_creature_ids_by_alias(self, target_alias) -> [str]:
        foundIds = []

        hero = self.game_state.hero
        hero_room = self.game_state.rooms[hero.location]

        for creature_id in hero_room.creature:
            if creature_id in self.game_state.creatures:
                creature_data = self.game_state.creatures[creature_id]
                if target_alias in creature_data.alias:
                    foundIds.append(creature_id)
        return foundIds

    def _find_ids_by_alias(self, target_alias) -> [str]:
        foundIds = []
        foundIds += self._find_item_ids_by_alias_in_room(self.game_state.hero.location, target_alias)
        foundIds += self._find_item_ids_by_alias_in_inventory(target_alias)
        foundIds += self._find_env_obj_ids_by_alias(target_alias)
        foundIds += self._find_creature_ids_by_alias(target_alias)
        return foundIds

    def _find_item_ids_by_alias_in_inventory(self, target_alias) -> [str]:
        item_ids_in_inventory = self.game_state.hero.inventory

        foundIds = []
        for item_id in item_ids_in_inventory:
            if item_id in self.game_state.items:
                item_data = self.game_state.items[item_id]
                if target_alias in item_data.alias:
                    foundIds.append(item_id)
            if item_id in self.game_state.equipment:
                item_data = self.game_state.equipment[item_id]
                if target_alias in item_data.alias:
                    foundIds.append(item_id)
        return foundIds


    def _find_item_ids_by_alias_in_room(self, room_id, target_alias) -> [str]:
        room: Room = self.game_state.rooms[room_id]
        item_ids_in_room = room.items

        foundIds = []
        for item_id in item_ids_in_room:
            if item_id in self.game_state.items:
                item_data = self.game_state.items[item_id]
                if target_alias in item_data.alias:
                    foundIds.append(item_id)
            if item_id in self.game_state.equipment:
                item_data = self.game_state.equipment[item_id]
                if target_alias in item_data.alias:
                    foundIds.append(item_id)
        return foundIds

    def _check_found_one_id_only(self, ids, target_alias) -> bool:
        if len(ids) == 0:
            print(f"There is no such thing as \"{target_alias}\".")
            return False
        if len(ids) > 1:
            print(f"There are {len(ids)} \"{target_alias}\"-s. You have to be more specific.")
            return False
        return True

    def _display_item(self, target_alias):
        ids = self._find_ids_by_alias(target_alias)
        if self._check_found_one_id_only(ids, target_alias):
            id = ids[0]
            if id in self.game_state.items:
                item_data = self.game_state.items[id]
                self.display(item_data)
            elif id in self.game_state.environment_objects:
                env_obj_data = self.game_state.environment_objects[id]
                self.display(env_obj_data)


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


    def _item_take(self, target_item_alias):
        hero = self.game_state.hero
        item_ids = self._find_item_ids_by_alias_in_room(hero.location, target_item_alias)

        if not self._check_found_one_id_only(item_ids, target_item_alias):
            return

        item_id = item_ids[0]
        hero.inventory.append(item_id)
        self.despawn_item(item_id)
        print(f"You grabbed the {target_item_alias}.")

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
            if spotted_creature.health <= 0:
                print(f"{target} is already dead.")
                return

            damage = 1
            if hero.right_hand != "none":
                damage = self.game_state.equipment[hero.right_hand].damage
            spotted_creature.health -= damage
            print(f"You hit the {target} for {damage} damage! {target} has {spotted_creature.health} HP left.")
            if spotted_creature.health <= 0:
                print(f"{target} is DEAD!")
                for loot in spotted_creature.drops:
                    self.spawn_item(loot)
            # ak ešte žije
            # todo: vsetky prisery v miestnosti su na rade s utokom ?
            if spotted_creature.health > 0:
                total_damage = self._count_total_hero_damage(spotted_creature)
                hero.health -= total_damage
                print(f"{target} hit you for {total_damage} damage! You have {hero.health} HP left.")
        else:
            print(f"There's no such thing as {target}.")

    def _count_total_hero_damage(self, creature):
        hero = self.game_state.hero
        total_armor_resist = 0
        # todo: shield do left hand?
        for armor in hero.head, hero.chest, hero.legs:
            if armor != "none":
                self.game_state.equipment[armor].durability -= creature.damage // 2
                if self.game_state.equipment[armor].durability  <= 0:
                    self._drop_item(armor)
                total_armor_resist += self.game_state.equipment[armor].resistance
        total_damage = creature.damage - total_armor_resist
        return total_damage

    def _drop_item(self, target):
        hero = self.game_state.hero
        equipment = self.game_state.equipment

        item = equipment[target]

        if item.slot == "hand":
            hero.right_hand = "none"
        elif item.slot == "head":
            hero.head = "none"
        elif item.slot == "chest":
            hero.chest = "none"
        elif item.slot == "legs":
            hero.legs = "none"

        item.in_use = False
        hero.inventory.remove(target)
        print(f"Ouch! {item.alias[0]} has been destroyed!")
        print(f"You've dropped {item.alias[0]}")

    def _equip_item(self, target):
        hero = self.game_state.hero
        items = self.game_state.items
        equipment = self.game_state.equipment

        item = None
        item_id = None
        for it in equipment:
            if target in equipment[it].alias:
                item = equipment[it]
                item_id = it
                break

        if item_id not in hero.inventory:
            print(f"You don't have {target} in your inventory.")
            return
        if item_id in items:
            print(f"You cant equip {target}")
            return
        if not item:
            print(f"There is no such thing as {target}")
            return
        if hero.right_hand == item_id or hero.left_hand == item_id:
            print(f"You are already equipped with {target}")
            return

        if item.slot == "hand":
            if hero.right_hand != "none":
                equipment[hero.right_hand].in_use = False
            hero.right_hand = item_id
        elif item.slot == "head":
            if hero.head != "none":
                equipment[hero.head].in_use = False
            hero.head = item_id
        elif item.slot == "chest":
            if hero.chest != "none":
                equipment[hero.chest].in_use = False
            hero.chest = item_id
        elif item.slot == "legs":
            if hero.legs != "none":
                equipment[hero.legs].in_use = False
            hero.legs = item_id

        print(f"You are now equipped with {target}")
        item.in_use = True

    def execute(self, commands):
        ignored = {"the", "on", "a", "an", "this", "that"}
        commands = [command for command in commands if command not in ignored]
        if len(commands) == 1:
            self.single_command(commands[0])
        else:
            self.double_command(commands[0], " ".join(commands[1:]))

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
        elif isinstance(obj, EnvironmentObject):
            self.examine_item(obj)
        elif isinstance(obj, Item):
            self.examine_item(obj)
        elif isinstance(obj, str):
            if obj == "inventory":
                self.show_inventory()
            elif obj == "status":
                self.show_status()
            else:
                print(obj)
        else:
            print(obj)

    def move_to(self, room_id):
        self.game_state.hero.location = room_id
        rooms = self.game_state.rooms
        print(f"You entered {rooms[room_id].description.lower()}")
        if rooms[room_id].auto_commands is not None:
            self.run_internal_command(rooms[room_id].auto_commands, room_id)

    def run_internal_command(self, commands, node=None):
        for c in commands:
            if c == "command_spawn_item" and node:
                self.spawn_item(commands[c])
                self.despawn_item(node)
            elif c == "command_display":
                self.display(commands[c])
            elif c == "command_required_item":
                if not self.check_inventory_for_item(commands[c]):
                    print(f"You do not have a required item to do this action.")
                    return
                continue
            elif c == "command_set_unlocked":
                self.game_state.environment_objects[node].unlocked = commands[c]
            elif c == "command_set_description":
                self.game_state.environment_objects[node].description = commands[c]
            elif c == "command_use_item":
                self.use_item(node)
            elif c == "command_remove_item_from_inventory":
                self.game_state.hero.inventory.remove(commands[c])
            elif c == "command_end_game":
                exit(1)
            else:
                print(f"Unknown internal command {c}")
                return

    def spawn_item(self, item_id):
        items = self.game_state.items
        room = self.game_state.rooms[self.game_state.hero.location]
        if item_id not in room.items:
            print(f"You found {items[item_id].alias[0]}. {items[item_id].description}.")
            room.items.append(item_id)
        else:
            print(f"You already did this.")

    def despawn_item(self, item_id):
        room = self.game_state.rooms[self.game_state.hero.location]
        if item_id in room.items:
            room.items.remove(item_id)

    def check_inventory_for_item(self, item_id):
        return item_id in self.game_state.hero.inventory

    def use_item(self, item_id):
        item = self.game_state.items[item_id]
        hero = self.game_state.hero

        if item.value > 0 and hero.health == 100:
            print(f"You are fully healed, you don't need healing.")
            return
        if item.value < 0:
            will_heal = item.value
        else:
            need_heal = 100 - hero.health
            if need_heal >= item.value:
                will_heal = item.value
            else:
                will_heal = need_heal

        hero.health += will_heal
        sign = "+"
        if will_heal < 0:
            sign = ""
        print(f"You used {item.alias[0]}. {sign}{will_heal} health. Current health is {hero.health} health.")
        hero.inventory.remove(item_id)

    def heal(self):
        hero = self.game_state.hero

        for item in hero.inventory:
            if item in self.game_state.items and isinstance(self.game_state.items[item], Consumable):
                if self.game_state.items[item].value > 0:
                    self.use_item(item)
                    return
        print(f"You don't have anything you could use for healing in your inventory")

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
        tmp = "none"
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

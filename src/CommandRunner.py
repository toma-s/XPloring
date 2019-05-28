from src.GameState import GameState
from src.Room import Room
from src.Item import Item
from random import randrange as rr


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
                    self.display(hero.inventory)
                    return

        print("I don't understand. Try again.")

    def double_command(self, action, target):
        if action in self.game_state.hero.actions:
            self._hero_action(action, target)
        else:
            # for env_obj in self.game_state.environment_objects:
            #     if env_obj in self.game_state.rooms[self.game_state.hero.location].action in self.game_state.environment_objects[env_obj].actions:
            #         self._env_object_action(action, target)
            #         return
            self._item_action(action, target)

    def _hero_action(self, action, target):
        hero = self.game_state.hero
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

        elif verb == "equip":
            if noun == "item":
                self._equip_item(target)

    def _item_action(self, action, target):
        int_commands = None
        item_id = None
        for it in self.game_state.rooms[self.game_state.hero.location].items:
            if it in self.game_state.items and target in self.game_state.items[it].alias and action in \
                    self.game_state.items[it].actions:
                int_commands = self.game_state.items[it].actions[action]
                item_id = it
                break
        if int_commands:
            self.run_internal_command(int_commands, item_id)

    def _env_object_action(self, action, target):
        int_commands = None
        obj_id = None
        for it in self.game_state.rooms[self.game_state.hero.location].items:
            if it in self.game_state.environment_objects and target in self.game_state.environment_objects[it].alias \
                    and action in self.game_state.environment_objects[it].actions:
                int_commands = self.game_state.items[it].actions[action]
                obj_id = it
                break
        if int_commands:
            self.run_internal_command(int_commands, obj_id)

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
        hero = self.game_state.hero

        item = None
        item_id = None
        for it in items:
            if target in items[it].alias:
                item = items[it]
                item_id = it
                break

        if not item:
            for it in equipment:
                if target in equipment[it].alias:
                    item = equipment[it]
                    item_id = it
                    break
        if item and item_id in self.game_state.rooms[hero.location].items:
            hero.inventory.append(item_id)
            self.despawn_item(item_id)
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
            if spotted_creature.health <= 0:
                print(f"{target} is already dead.")
                return

            damage = 1
            if hero.right_hand != "none":
                damage = self.game_state.equipment[hero.right_hand].damage
            spotted_creature.health -= damage
            print(f"You hit the {target}! {target} lost {damage} health.")
            if spotted_creature.health <= 0:
                print(f"{target} is DEAD!")
                for loot in spotted_creature.drops:
                    self.spawn_item(loot)
            # ak ešte žije
            # todo: vsetky prisery v miestnosti su na rade s utokom ?
            if spotted_creature.health > 0:
                # todo: damage reduction ak ma ableceny armor
                hero.health -= spotted_creature.damage
                print(f"{target} had hit you! You lose {spotted_creature.damage} health.")
        else:
            print(f"There's no such thing as {target}.")

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

    def run_internal_command(self, commands, node=None):
        # print(f"[DEBUG] running internal - {commands}")
        for c in commands:
            if c == "command_spawn_item" and node:
                self.spawn_item(commands[c])
                self.despawn_item(node)
            elif c == "command_display":
                self.display(commands[c])
            elif c == "command_required_item":
                if not self.check_inventory_for_item(commands[c]):
                    print(f"You do not have item required to do this action.")
                    return
            elif c == "command_set_unlocked":
                self.game_state.environment_objects[node].unlocked = commands[c]
            elif c == "command_set_description":
                self.game_state.environment_objects[node].description = commands[c]


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
from Finder import Finder
from GameState import GameState
from game_item.Armour import Armour
from game_item.Creature import Creature
from game_item.Equipment import Equipment
from game_item.Hero import Hero
from game_item.Item import Item
from game_item.Room import Room
from game_item.TransitionObject import TransitionObject
from game_item.Weapon import Weapon


class InternalCommandHandler:

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.finder = Finder(game_state)

    def handle_internal_command(self, commands, target_id=None):
        for command in commands:
            if command == "command_move_direction":
                self._move_to_direction(target_id)

            elif command == "command_show_message":
                message = commands[command]
                print(f"{message}")

            elif command == "command_show_description":
                data = self.finder.get_data_by_id(target_id)
                print(f"{data.description}")

            elif command == "command_set_description":
                new_description: str = commands[command]
                self._set_description(target_id, new_description)

            elif command == "command_set_unlocked":
                unlocked: bool = commands[command]
                self._set_unlocked(target_id, unlocked)

            elif command == "command_attack_creature":
                self._attack_creature(target_id)

            elif command == "command_spawn_item":
                item_id = commands[command]
                self.spawn_item(item_id)

            elif command == "command_despawn_item":
                item_id = commands[command]
                self._despawn_item(item_id)

            elif command == "command_add_item_to_inventory":
                self._item_take(target_id)

            elif command == "command_remove_item_from_inventory":
                self._remove_item_from_inventory(commands[command])

            elif command == "command_required_item":
                item_id = commands[command]
                if not self._required_item_in_inventory(item_id):
                    return

            elif command == "command_use_item":
                self.use_item(target_id)

            elif command == "command_equip":
                self._equip_item(target_id)

            elif command == "command_unequip":
                self._unequip_item(target_id)

            elif command == "command_show_room":
                self._show_hero_room()

            elif command == "command_show_status":
                self._show_hero_status()

            elif command == "command_show_inventory":
                self._show_hero_inventory()

            elif command == "command_good_end":
                end_massage = commands[command]
                self._end_game(end_massage)

            else:
                print("I don't understand that command.")

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

    def move_to(self, room_id):
        self.game_state.hero.location = room_id
        rooms = self.game_state.rooms
        print(f"{rooms[room_id].description}")
        if rooms[room_id].auto_commands is not None:
            self.handle_internal_command(rooms[room_id].auto_commands, room_id)

    def _set_description(self, target_id, description_message: str):
        target_data = self.finder.get_data_by_id(target_id)
        target_data.description = description_message

    def _set_unlocked(self, target_id, is_unlocked: bool):
        target_data = self.finder.get_data_by_id(target_id)
        target_data.unlocked = is_unlocked

    def _attack_creature(self, creature_id):
        creature_data: Creature = self.finder.get_data_by_id(creature_id)
        creature_alias = creature_data.alias[0]

        if creature_id not in self.game_state.creatures:
            print(f"You can't attack the {creature_alias}.")
            return

        self._hero_attack_turn(creature_data)
        self._creature_attack_turn(creature_data)

    def _hero_attack_turn(self, target_creature: Creature):
        hero = self.game_state.hero
        target_alias = target_creature.alias[0]

        if target_creature.health <= 0:
            print(f"{self._capitalize_first(target_alias)} is already dead.")
            return
        damage = hero.base_damage
        if hero.right_hand is not None:
            damage = self.game_state.equipment[hero.right_hand].damage
        target_creature.health -= damage
        print(f"You hit the {target_alias} for {damage} damage! "
              f"{self._capitalize_first(target_alias)} has {target_creature.health} HP left.")

    def _creature_attack_turn(self, creature_data):
        hero = self.game_state.hero
        creature_alias = creature_data.alias[0]

        if creature_data.health <= 0:
            print(f"{self._capitalize_first(creature_alias)} is DEAD!")
            for loot in creature_data.drops:
                self.spawn_item(loot)
        # todo: vsetky prisery v miestnosti su na rade s utokom ?
        if creature_data.health > 0:
            total_damage = self._count_total_hero_damage(creature_data)
            hero.health -= total_damage
            print(f"{self._capitalize_first(creature_alias)} hit you for {total_damage} damage! "
                  f"You have {hero.health} HP left.")

        if hero.health <= 0:
            self._end_game(f"GAME OVER. You were killed by {creature_alias}. Better luck next time.")


    def _count_total_hero_damage(self, creature):
        hero = self.game_state.hero
        total_armor_resist = 0
        # todo: shield do left hand?
        for armor in hero.head, hero.chest, hero.legs:
            if armor is not None:
                self.game_state.equipment[armor].durability -= creature.damage // 2
                if self.game_state.equipment[armor].durability <= 0:
                    self._drop_item(armor)
                total_armor_resist += self.game_state.equipment[armor].resistance
        total_damage = creature.damage - total_armor_resist
        return total_damage

    def _drop_item(self, target):
        hero = self.game_state.hero
        equipment = self.game_state.equipment

        item = equipment[target]

        if item.slot == "hand":
            hero.right_hand = None
        elif item.slot == "head":
            hero.head = None
        elif item.slot == "chest":
            hero.chest = None
        elif item.slot == "legs":
            hero.legs = None

        item.in_use = False
        hero.inventory.remove(target)
        print(f"Ouch! {item.alias[0]} has been destroyed!")
        print(f"You've dropped {item.alias[0]}")

    def spawn_item(self, item_id):
        items = self.game_state.items
        room = self.game_state.rooms[self.game_state.hero.location]
        if item_id not in room.items:
            print(f"You found {items[item_id].alias[0]}. {items[item_id].description}.")
            room.items.append(item_id)
        else:
            print(f"You already did this.")

    def _despawn_item(self, item_id):
        hero = self.game_state.hero
        room = self.game_state.rooms[hero.location]
        if item_id in room.items:
            room.items.remove(item_id)

    def _item_take(self, item_id):
        hero = self.game_state.hero

        item_data = self.finder.get_data_by_id(item_id)
        target_item_alias = item_data.alias[0]

        if item_id in hero.inventory:
            print(f"{self._capitalize_first(target_item_alias)} is already in your inventory.")
            return
        hero.inventory.append(item_id)
        room = self.game_state.rooms[hero.location]
        room.items.remove(item_id)

        print(f"{self._capitalize_first(target_item_alias)} has been added to your inventory.")

    def _remove_item_from_inventory(self, item_id):
        inventory = self.game_state.hero.inventory
        if item_id in inventory:
            inventory.remove(item_id)

    def _required_item_in_inventory(self, item_id):
        hero = self.game_state.hero
        if item_id in hero.inventory:
            return True
        print(f"You don't have a required item to do this action.")
        return False

    def use_item(self, item_id):
        item_data = self.game_state.items[item_id]
        hero = self.game_state.hero

        if item_id not in hero.inventory:
            print(f"You do not have it in your inventory.")
            return

        if item_data.value > 0 and hero.health == 100:
            print(f"You are fully healed, you don't need healing.")
            return
        if item_data.value < 0:
            will_heal = item_data.value
        else:
            need_heal = 100 - hero.health
            if need_heal >= item_data.value:
                will_heal = item_data.value
            else:
                will_heal = need_heal

        hero.health += will_heal
        sign = "+"
        if will_heal < 0:
            sign = ""
        print(f"You have consumed {item_data.alias[0]}. "
              f"{sign}{will_heal} HP. Current health is {hero.health} HP.")
        hero.inventory.remove(item_id)

    def _equip_item(self, item_id):
        hero = self.game_state.hero
        equipment = self.game_state.equipment

        if item_id not in hero.inventory:
            print(f"You don't have that in your inventory.")
            return
        if self._is_item_equipped(item_id):
            print(f"It is already equipped.")
            return

        equipment_data: Equipment = self.game_state.equipment[item_id]

        setattr(hero, equipment_data.slot, item_id)

        print(f"Item equipped")
        equipment_data.in_use = True

    def _unequip_item(self, item_id):
        if not self._is_item_equipped(item_id):
            print(f"It is not equipped.")
            return
        hero = self.game_state.hero
        equipment_data: Equipment = self.game_state.equipment[item_id]
        setattr(hero, equipment_data.slot, None)

        item_in_slot = getattr(hero, equipment_data.slot)
        if item_in_slot == item_id:
            return True

        print(f"Item unequipped.")
        equipment_data.in_use = False

    def _is_item_equipped(self, item_id: str) -> bool:
        if item_id not in self.game_state.equipment:
            return False
        data: Equipment = self.finder.get_data_by_id(item_id)
        hero = self.game_state.hero
        item_in_slot = getattr(hero, data.slot)
        if item_in_slot == item_id:
            return True
        return False

    def _show_hero_room(self):
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

    def _show_hero_status(self):

        def _print_weapon(slot_name: str):
            hero: Hero = self.game_state.hero
            weapon_id = getattr(hero, slot_name)
            info = "none"
            if weapon_id is not None:
                weapon_data = self.game_state.equipment[weapon_id]
                info = weapon_data.description
                info += f" {weapon_data.damage} ATK"
            slot_print = self._capitalize_first(slot_name.replace('_', ' '))
            print(f"{slot_print}: {info}")

        def _print_armour(slot_name: str):
            hero: Hero = self.game_state.hero
            armour_id = getattr(hero, slot_name)
            info = "none"
            if armour_id is not None:
                armour_data = self.game_state.equipment[armour_id]
                info = armour_data.description
                info += f" {armour_data.resistance} DEF"
                info += f" {armour_data.durability} Durability"
            slot_print = self._capitalize_first(slot_name.replace('_', ' '))
            print(f"{slot_print}: {info}")

        hero: Hero = self.game_state.hero
        print(f"----- HERO STATUS -----")
        print(f"Health: {hero.health} HP")
        print(f"Attack Power: {hero.base_damage} ATK")
        _print_weapon("right_hand")
        _print_weapon("left_hand")
        _print_armour("head")
        _print_armour("chest")
        _print_armour("legs")
        print(f"-----------------------")

    def _show_hero_inventory(self):
        hero = self.game_state.hero
        if len(hero.inventory) == 0:
            print(f"Your inventory is empty.")
            return

        for inv_item in hero.inventory:
            if inv_item in self.game_state.items:
                it = self.game_state.items[inv_item]
            else:
                it = self.game_state.equipment[inv_item]
            res = f"{it.alias[0]} - {it.description}"
            if isinstance(it, Armour) or isinstance(it, Weapon):
                if it.in_use:
                    res += " [EQUIPPED]"
            print(res)

    def _end_game(self, end_message):
        print(end_message)
        exit(0)


    @staticmethod
    def _capitalize_first(input: str):
        return input[0].capitalize() + input[1:]




from Finder import Finder
from GameState import GameState
from game_item.Armour import Armour
from game_item.Consumable import Consumable
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
                self._show_description(target_id)

            elif command == "command_set_description":
                new_description: str = commands[command]
                self._set_description(target_id, new_description)

            elif command == "command_set_unlocked":
                unlocked: bool = commands[command]
                self._set_unlocked(target_id, unlocked)

            elif command == "command_attack_creature":
                self.attack_creature(target_id)

            elif command == "command_spawn_item":
                item_id = commands[command]
                self._spawn_item(item_id)

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

            elif command == "command_consume_item":
                # TODO refactor - use_item
                self.consume_item(target_id)

            elif command == "command_equip":
                self._equip_item(target_id)

            elif command == "command_unequip":
                self.unequip_item(target_id)

            elif command == "command_drop_item":
                self.drop_item(target_id)

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

    def _show_description(self, target_id):
        target_data = self.finder.get_data_by_id(target_id)
        print(f"{target_data.description}")
        if isinstance(target_data, Weapon):
            print(f"DMG: {target_data.damage}")
        elif isinstance(target_data, Armour):
            print(f"Durability: {target_data.durability}")
            print(f"Resistance: {target_data.resistance}")
        elif isinstance(target_data, Creature):
            print(f"HP: {target_data.health}")
            print(f"DMG: {target_data.damage}")

    def _set_description(self, target_id, description_message: str):
        target_data = self.finder.get_data_by_id(target_id)
        target_data.description = description_message

    def _set_unlocked(self, target_id, is_unlocked: bool):
        target_data = self.finder.get_data_by_id(target_id)
        target_data.unlocked = is_unlocked

    def attack_creature(self, target_creature_id):
        target_creature_data: Creature = self.finder.get_data_by_id(target_creature_id)
        creature_alias = target_creature_data.alias[0]

        if target_creature_id not in self.game_state.creatures:
            print(f"You can't attack the {creature_alias}.")
            return

        if target_creature_data.health <= 0:
            print(f"{self._capitalize_first(target_creature_data.alias[0])} is already dead.")
            return

        self._hero_attack_turn(target_creature_data)

        hero = self.game_state.hero
        hero_room: Room = self.game_state.rooms[hero.location]
        for creature_id in hero_room.creatures:
            creature_data: Creature = self.game_state.creatures[creature_id]
            if creature_data.health > 0:
                self._creature_attack_turn(creature_data)

    def _hero_attack_turn(self, creature_data: Creature):
        if creature_data.health <= 0:
            return
        creature_alias = creature_data.alias[0]
        hero = self.game_state.hero
        hero_attack_power = hero.base_damage
        if hero.right_hand is not None:
            hero_attack_power = self.game_state.equipment[hero.right_hand].damage
        creature_data.health -= hero_attack_power
        print(f"You hit the {creature_alias} for {hero_attack_power} damage! "
              f"{self._capitalize_first(creature_alias)} has {creature_data.health} HP left.")

        if creature_data.health <= 0:
            self._on_creature_death(creature_data)

    def _on_creature_death(self, creature_data: Creature):
        creature_alias = creature_data.alias[0]
        print(f"{self._capitalize_first(creature_alias)} is dead!")
        for loot in creature_data.drops:
            self._spawn_item(loot)

    def _creature_attack_turn(self, creature_data: Creature):
        creature_alias = creature_data.alias[0]
        hero = self.game_state.hero

        if creature_data.health > 0:
            total_damage = self._count_total_hero_damage(creature_data)
            hero.health -= total_damage
            print(f"{self._capitalize_first(creature_alias)} hit you for {total_damage} damage! "
                  f"You have {hero.health} HP left.")

            if hero.health <= 0:
                self._end_game(f"GAME OVER. You were killed by {creature_alias}. Better luck next time.")

    def _count_total_hero_damage(self, creature_data):
        hero = self.game_state.hero
        total_armor_resist = 0
        # todo: shield do left hand?
        for armor_id in hero.head, hero.chest, hero.legs:
            if armor_id is not None:
                self._armor_durability_loss(armor_id, creature_data.damage)
                total_armor_resist += self.game_state.equipment[armor_id].resistance
        total_damage = creature_data.damage - total_armor_resist
        return total_damage

    def _armor_durability_loss(self, armor_id, damage_value):
        armor_data: Armour = self.game_state.equipment[armor_id]
        armor_data.durability = armor_data.durability - (damage_value // 2)
        if armor_data.durability <= 0:
            self._equipment_destruction(armor_id)

    def _equipment_destruction(self, equipment_id):
        hero = self.game_state.hero
        equipment_data = self.game_state.equipment[equipment_id]

        setattr(hero, equipment_data.slot, None)

        self._remove_item_from_inventory(equipment_id)
        print(f"Your {self._capitalize_first(equipment_data.alias[0])} is broken!")


    def _hero_hp_reduction(self, damage_value, attacker_alias):
        ...


    def _spawn_item(self, item_id):
        room = self.game_state.rooms[self.game_state.hero.location]
        if item_id not in room.items:
            room.items.append(item_id)

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

    def consume_item(self, item_id):
        item_data = self.game_state.items[item_id]
        if not hasattr(item_data, "value"):
            print(f"That item can not be consumed.")
            return
        item_data: Consumable = item_data
        hero = self.game_state.hero

        if item_id not in hero.inventory:
            print(f"You do not have that in your inventory.")
            return

        if item_data.value < 0:
            self._consume_item_harmful_effect(item_data)
        else:
            self._consume_item_healing_effect(item_data)
        hero.inventory.remove(item_id)

    def _consume_item_harmful_effect(self, consumable_data: Consumable):
        hero = self.game_state.hero
        harm_amount = consumable_data.value
        hero.health += harm_amount

        consumable_alias = consumable_data.alias[0]
        print(f"The {consumable_alias} reduced your HP by {harm_amount}.")
        print(f"Your current health is {hero.health} HP.")

        if hero.health <= 0:
            self._end_game(f"GAME OVER. You were killed by {consumable_alias}. Better luck next time.")

    def _consume_item_healing_effect(self, consumable_data):
        hero = self.game_state.hero
        if hero.health == 100:
            print(f"Your health is already 100 HP, you don't need healing.")
            return

        heal_amount = consumable_data.value
        missing_hp = 100 - hero.health
        if heal_amount > missing_hp:
            heal_amount = missing_hp

        hero.health += heal_amount

        consumable_alias = consumable_data.alias[0]
        print(f"The {consumable_alias} healed you for {heal_amount} HP.")
        print(f"Your current health is {hero.health} HP.")

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

    def unequip_item(self, item_id):
        if not self._is_item_equipped(item_id):
            print(f"It is not equipped.")
            return
        self._remove_item_from_hero_slot(item_id)
        print(f"Item unequipped.")

    def _remove_item_from_hero_slot(self, item_id):
        hero = self.game_state.hero
        equipment_data: Equipment = self.game_state.equipment[item_id]
        setattr(hero, equipment_data.slot, None)

    def _is_item_equipped(self, item_id: str) -> bool:
        if item_id not in self.game_state.equipment:
            return False
        data: Equipment = self.finder.get_data_by_id(item_id)
        hero = self.game_state.hero
        item_in_slot = getattr(hero, data.slot)
        if item_in_slot == item_id:
            return True
        return False

    def drop_item(self, item_id):
        hero = self.game_state.hero
        if item_id not in hero.inventory:
            print("You don't have that in your inventory.")
            return
        if self._is_item_equipped(item_id):
            self._remove_item_from_hero_slot(item_id)
            print(f"Item unequipped.")
        self._remove_item_from_inventory(item_id)
        self._spawn_item(item_id)
        print(f"Item removed from inventory.")

    def _show_hero_room(self):
        items = self.game_state.items
        equipment = self.game_state.equipment
        creatures = self.game_state.creatures
        room = self.game_state.rooms[self.game_state.hero.location]

        print(f"{self._capitalize_first(room.alias)} room. {room.description}")

        # items in room
        for item_id in room.items:
            item_data = self.finder.get_data_by_id(item_id)
            if item_id in items:
                print(f"There is a {item_data.alias[0]}. {self._capitalize_first(item_data.description)}.")
            elif item_id in equipment:
                print(f"There is a {item_data.alias[0]}. {self._capitalize_first(item_data.description)}.")

        # entities in room
        if not room.creatures:
            print("There are no enemies around.")
        else:
            for c in room.creatures:
                print(f"There is a hostile {creatures[c].alias[0]}."
                      f"{self._capitalize_first(creatures[c].description)}.")

        # direction from room
        for direction_name, direction_data in room.directions.items():
            if "trans_obj_id" in direction_data.keys():
                trans_obj_data: TransitionObject = self.finder.get_data_by_id(direction_data["trans_obj_id"])
                print(f"There is a {trans_obj_data.alias[0]} to the {direction_name.upper()}.")
            else:
                room_in_dir = self.game_state.rooms[direction_data["room_id"]].alias
                print(f"The {room_in_dir} is to the {direction_name.upper()}.")

    def _show_hero_status(self):

        def _print_weapon(slot_name: str):
            weapon_id = getattr(hero, slot_name)
            info_print = "nothing"
            if weapon_id is not None:
                weapon_data = self.game_state.equipment[weapon_id]
                info_print = weapon_data.description
                info_print += f" {weapon_data.damage} ATK"
            slot_print = self._capitalize_first(slot_name.replace('_', ' '))
            print(f"{slot_print}: {info_print}")

        def _print_armour(slot_name: str):
            armour_id = getattr(hero, slot_name)
            info_print = "nothing"
            if armour_id is not None:
                armour_data = self.game_state.equipment[armour_id]
                info_print = armour_data.description
                info_print += f" {armour_data.resistance} DEF"
                info_print += f" {armour_data.durability} Durability"
            slot_print = self._capitalize_first(slot_name.replace('_', ' '))
            print(f"{slot_print}: {info_print}")

        hero: Hero = self.game_state.hero
        hero_damage = hero.base_damage
        if hero.right_hand is not None:
            weapon_data: Weapon = self.game_state.equipment[hero.right_hand]
            hero_damage = weapon_data.damage

        print(f"----- HERO STATUS -----")
        print(f"Health: {hero.health} HP")
        print(f"Attack Power: {hero_damage} ATK")
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

        for item_id in hero.inventory:
            item_data = self.finder.get_data_by_id(item_id)
            item_print = f"{item_data.alias[0]} - {item_data.description}"
            if self._is_item_equipped(item_id):
                item_print += " [EQUIPPED]"
            print(item_print)

    def _end_game(self, end_message):
        print(end_message)
        exit(0)


    @staticmethod
    def _capitalize_first(input: str):
        return input[0].capitalize() + input[1:]




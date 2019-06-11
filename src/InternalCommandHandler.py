from Finder import Finder
from GameState import GameState
from game_item.Armour import Armour
from game_item.Consumable import Consumable
from game_item.Creature import Creature
from game_item.Equipment import Equipment
from game_item.Hero import Hero
from game_item.Room import Room
from game_item.TransitionObject import TransitionObject
from game_item.Weapon import Weapon


class InternalCommandHandler:

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.finder = Finder(game_state)

    def handle_internal_command(self, ic_name, ic_arg, target_id) -> bool:
        allow_next_command = True

        if ic_name == "command_move_direction":
            self.move_to_direction(target_id)

        elif ic_name == "command_show_message":
            message = ic_arg
            print(f"{message}")

        elif ic_name == "command_show_description":
            self._show_description(target_id)

        elif ic_name == "command_set_description":
            new_description: str = ic_arg
            self._set_description(target_id, new_description)

        elif ic_name == "command_set_locked":
            is_locked: bool = ic_arg
            self._set_locked(target_id, is_locked)

        elif ic_name == "command_attack_creature" :
            self.attack_creature(target_id)

        elif ic_name == "command_spawn_items":
            item_ids: [str] = ic_arg
            for item_id in item_ids:
                self._spawn_item(item_id)

        elif ic_name == "command_despawn_item":
            item_id = target_id
            if ic_arg is not None:
                item_id = ic_arg
            self._despawn_item(item_id)

        elif ic_name == "command_add_item_to_inventory":
            item_id = target_id
            if ic_arg is not None:
                item_id = ic_arg
            self._add_item_to_inventory(item_id)

        elif ic_name == "command_remove_item_from_inventory":
            self._remove_item_from_inventory(ic_arg)

        elif ic_name == "command_required_items":
            item_ids: [str] = ic_arg
            for item_id in item_ids:
                if not self._required_item_in_inventory(item_id):
                    allow_next_command = False
                    break

        elif ic_name == "command_consume_item":
            if not self.consume_item(target_id):
                allow_next_command = False

        elif ic_name == "command_equip":
            self._equip_item(target_id)

        elif ic_name == "command_unequip":
            self.unequip_item(target_id)

        elif ic_name == "command_drop_item":
            self.drop_item(target_id)

        elif ic_name == "command_show_room":
            self._show_hero_room()

        elif ic_name == "command_show_status":
            self._show_hero_status()

        elif ic_name == "command_show_inventory":
            self._show_hero_inventory()

        elif ic_name == "command_good_end":
            end_massage = ic_arg
            self._end_game(end_massage)

        else:
            print("I don't understand that command.")
            allow_next_command = False
        return allow_next_command

    def move_to_direction(self, direction_name):
        hero = self.game_state.hero
        hero_room_data: Room = self.game_state.rooms[hero.location]

        if direction_name not in hero_room_data.directions:
            print(f"You are not allowed to go {direction_name}.")
            return

        direction_data = hero_room_data.directions[direction_name]
        target_room_id = direction_data["room_id"]

        if "trans_obj_id" in direction_data:
            trans_obj_id = direction_data["trans_obj_id"]
            trans_obj: TransitionObject = self.game_state.transition_objects[trans_obj_id]
            if trans_obj.locked:
                trans_obj_alias = trans_obj.alias[0]
                print(f"You can't go {direction_name}. The {trans_obj_alias} is locked.")
                return
        self._move_hero_to_room(target_room_id)

    def _move_hero_to_room(self, room_id):
        self.game_state.hero.location = room_id
        hero_room_data = self.game_state.rooms[room_id]
        if hero_room_data.auto_commands:
            for ic_name, ic_args in hero_room_data.auto_commands.items():
                self.handle_internal_command(ic_name, ic_args, room_id)
        self._show_hero_room()


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

    def _set_locked(self, target_id, is_locked: bool):
        target_data = self.game_state.transition_objects[target_id]
        target_data.locked = is_locked

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
        if hero.weapon_slot is not None:
            hero_attack_power = self.game_state.equipment[hero.weapon_slot].damage
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

        for armor_id in hero.head_slot, hero.chest_slot, hero.legs_slot:
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

    def _spawn_item(self, item_id):
        room = self.game_state.rooms[self.game_state.hero.location]
        if item_id not in room.items:
            room.items.append(item_id)

    def _despawn_item(self, item_id):
        hero = self.game_state.hero
        room = self.game_state.rooms[hero.location]
        if item_id in room.items:
            room.items.remove(item_id)

    def _add_item_to_inventory(self, item_id):
        hero = self.game_state.hero

        item_data = self.finder.get_data_by_id(item_id)
        target_item_alias = item_data.alias[0]

        if item_id in hero.inventory:
            print(f"{self._capitalize_first(target_item_alias)} is already in your inventory.")
            return
        hero.inventory.append(item_id)

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
            return False
        item_data: Consumable = item_data
        hero = self.game_state.hero

        if item_id not in hero.inventory:
            print(f"You do not have that in your inventory.")
            return False

        if item_data.value < 0:
            consumed = self._consume_item_harmful_effect(item_data)
        else:
            consumed = self._consume_item_healing_effect(item_data)
        if consumed:
            hero.inventory.remove(item_id)
        return consumed

    def _consume_item_harmful_effect(self, consumable_data: Consumable) -> bool:
        hero = self.game_state.hero
        harm_amount = abs(consumable_data.value)

        hero.health -= harm_amount

        consumable_alias = consumable_data.alias[0]
        print(f"The {consumable_alias} reduced your HP by {harm_amount}. "
              f"Your current health is {hero.health} HP.")

        if hero.health <= 0:
            self._end_game(f"GAME OVER. You were killed by {consumable_alias}. Better luck next time.")
        return True

    def _consume_item_healing_effect(self, consumable_data) -> bool:
        hero = self.game_state.hero
        if hero.health == 100:
            print(f"Your health is already at 100 HP, you don't need healing.")
            return False

        heal_amount = consumable_data.value
        missing_hp = 100 - hero.health
        if heal_amount > missing_hp:
            heal_amount = missing_hp

        hero.health += heal_amount

        consumable_alias = consumable_data.alias[0]
        print(f"The {consumable_alias} healed you by {heal_amount} HP. "
              f"Your current health is {hero.health} HP.")
        return True

    def _equip_item(self, item_id):
        hero = self.game_state.hero

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

        print(f"{self._capitalize_first(room.alias)}.")
        print(f"{self._capitalize_first(room.description)}")
        print()

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
                print(f"There is a hostile {creatures[c].alias[0]}. "
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

        def _print_weapon(slot_id: str, slot_name):
            weapon_id = getattr(hero, slot_id)
            info_print = "nothing"
            if weapon_id is not None:
                weapon_data = self.game_state.equipment[weapon_id]
                info_print = weapon_data.description
                info_print += f" {weapon_data.damage} ATK"
            print(f"{slot_name}: {info_print}")

        def _print_armour(slot_id: str, slot_name: str):
            armour_id = getattr(hero, slot_id)
            info_print = "nothing"
            if armour_id is not None:
                armour_data = self.game_state.equipment[armour_id]
                info_print = armour_data.description
                info_print += f" {armour_data.resistance} DEF"
                info_print += f" {armour_data.durability} Durability"
            print(f"{slot_name}: {info_print}")

        hero: Hero = self.game_state.hero
        hero_damage = hero.base_damage
        if hero.weapon_slot is not None:
            weapon_data: Weapon = self.game_state.equipment[hero.weapon_slot]
            hero_damage = weapon_data.damage

        print(f"----- HERO STATUS -----")
        print(f"Health: {hero.health} HP")
        print(f"Attack Power: {hero_damage} ATK")
        _print_weapon("weapon_slot", "Weapon")
        _print_armour("head_slot", "Head")
        _print_armour("chest_slot", "Chest")
        _print_armour("legs_slot", "Legs")
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




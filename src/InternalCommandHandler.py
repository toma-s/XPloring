from Finder import Finder
from GameState import GameState
from game_item.Creature import Creature
from game_item.Equipment import Equipment
from game_item.Item import Item
from game_item.Room import Room
from game_item.TransitionObject import TransitionObject


class InternalCommandHandler:

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.finder = Finder(game_state)

    def handle_internal_command(self, commands, target_id=None):
        for c in commands:
            if c == "command_show_message":
                message = commands[c]
                print(f"{message}")

            elif c == "command_show_description":
                data = self.finder.get_data_by_id(target_id)
                print(f"{data.description}")

            elif c == "command_set_description":
                new_description: str = commands[c]
                self._set_description(target_id, new_description)

            elif c == "command_set_unlocked":
                unlocked: bool = commands[c]
                self._set_unlocked(target_id, unlocked)

            elif c == "command_attack_creature":
                self._attack_creature(target_id)

            elif c == "command_spawn_item":
                item_id = commands[c]
                self.spawn_item(item_id)

            elif c == "command_despawn_item":
                item_id = commands[c]
                self._despawn_item(item_id)

            elif c == "command_add_item_to_inventory":
                self._item_take(target_id)

            elif c == "command_remove_item_from_inventory":
                self._remove_item_from_inventory(commands[c])

            elif c == "command_required_item":
                item_id = commands[c]
                if not self._required_item_in_inventory(item_id):
                    return

            elif c == "command_use_item":
                self.use_item(target_id)

            elif c == "command_equip":
                self._equip_item(target_id)

            elif c == "command_good_end":
                end_massage = commands[c]
                self._end_game(end_massage)
            else:
                print(f"Unknown internal command {c}")
                return

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
        damage = hero.damage
        if hero.right_hand != "none":
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
            if armor != "none":
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

        item_data = self.game_state.equipment[item_id]

        if hero.right_hand == item_id or hero.left_hand == item_id or hero.head == item_id \
                or hero.chest == item_id or hero.legs == item_id:
            print(f"It is already equipped.")
            return

        if item_data.slot == "hand":
            if hero.right_hand != "none":
                equipment[hero.right_hand].in_use = False
            hero.right_hand = item_id
        elif item_data.slot == "head":
            if hero.head != "none":
                equipment[hero.head].in_use = False
            hero.head = item_id
        elif item_data.slot == "chest":
            if hero.chest != "none":
                equipment[hero.chest].in_use = False
            hero.chest = item_id
        elif item_data.slot == "legs":
            if hero.legs != "none":
                equipment[hero.legs].in_use = False
            hero.legs = item_id

        print(f"Item equipped")
        item_data.in_use = True

    def _end_game(self, end_message):
        print(end_message)
        exit(0)


    @staticmethod
    def _capitalize_first(input: str):
        return input[0].capitalize() + input[1:]




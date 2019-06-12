import json
from datetime import datetime
from typing import Dict

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


class GameStateSaver:

    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def save(self):
        data = self._load_data()
        self._store(data)

    def _load_data(self) -> Dict[str, any]:
        data = dict()
        data["rooms"] = self._load_rooms()
        data["creatures"] = self._load_creatures()
        data["transition_objects"] = self._load_transition_objects()
        data["items"] = self._load_items()
        data["equipment"] = self._load_equipment()
        data["hero"] = self._load_hero()
        return data

    def _load_rooms(self) -> Dict[str, any]:
        rooms = dict()
        for key, value in self.game_state.rooms.items():
            room = value
            rooms[key] = dict()
            rooms[key]["alias"] = room.alias
            rooms[key]["description"] = room.description
            rooms[key]["directions"] = room.directions
            rooms[key]["items"] = room.items
            rooms[key]["creatures"] = [creature for creature in room.creatures]
            rooms[key]["actions"] = self._get_custom_actions(room, Room.room_actions)
            rooms[key]["auto_commands"] = room.auto_commands
        return rooms

    def _load_creatures(self) -> Dict[str, any]:
        creatures = dict()
        for key, value in self.game_state.creatures.items():
            creature = value
            creatures[key] = dict()
            creatures[key]["alias"] = [alias_item for alias_item in creature.alias]
            creatures[key]["health"] = creature.health
            creatures[key]["damage"] = creature.damage
            creatures[key]["drops"] = creature.drops
            creatures[key]["description"] = creature.description
            actions = Creature.creature_actions.keys()
            creatures[key]["actions"] = self._get_custom_actions(creature, actions)
        return creatures

    def _load_transition_objects(self) -> Dict[str, any]:
        transition_objects = dict()
        for key, value in self.game_state.transition_objects.items():
            transition_object = value
            transition_objects[key] = dict()
            transition_objects[key]["alias"] = [alias_item for alias_item in transition_object.alias]
            transition_objects[key]["locked"] = transition_object.locked
            transition_objects[key]["description"] = transition_object.description
            actions = TransitionObject.trans_obj_actions.keys()
            transition_objects[key]["actions"] = self._get_custom_actions(transition_object, actions)
        return transition_objects

    def _load_items(self) -> Dict[str, any]:
        items = dict()
        for key, item in self.game_state.items.items():
            if isinstance(item, Consumable):
                self._load_consumable(item, items, key)
            elif isinstance(item, Item):
                self._load_regular(item, items, key)
        return items

    def _load_consumable(self, item, items, key):
        group_key = "consumable"
        items.setdefault(group_key, {})
        items[group_key].setdefault(key, {})
        items[group_key][key]["value"] = item.value
        self._load_item_values(group_key, item, items, key)

    def _load_regular(self, item, items, key):
        group_key = "regular"
        items.setdefault(group_key, {})
        items[group_key].setdefault(key, {})
        self._load_item_values(group_key, item, items, key)

    def _load_item_values(self, group_key, item, items, key):
        items[group_key][key]["description"] = item.description
        items[group_key][key]["alias"] = [alias_item for alias_item in item.alias]
        actions = Item.item_actions.keys()
        items[group_key][key]["actions"] = self._get_custom_actions(item, actions)

    def _load_equipment(self) -> Dict[str, any]:
        equipment = dict()
        for key, single_equipment in self.game_state.equipment.items():
            if isinstance(single_equipment, Armour):
                self._load_armour(single_equipment, equipment, key)
            elif isinstance(single_equipment, Weapon):
                self._load_weapons(single_equipment, equipment, key)
        return equipment

    def _load_weapon_values(self, equipment, group_key, key, single_equipment):
        equipment[group_key][key]["alias"] = [alias_item for alias_item in single_equipment.alias]
        equipment[group_key][key]["slot"] = single_equipment.slot
        equipment[group_key][key]["description"] = single_equipment.description
        actions = Item.item_actions.keys() | Equipment.equipment_actions.keys()
        equipment[group_key][key]["actions"] = self._get_custom_actions(single_equipment, actions)

    def _load_armour(self, single_equipment, equipment, key):
        group_key = "armour"
        equipment.setdefault(group_key, {})
        equipment[group_key].setdefault(key, {})
        equipment[group_key][key]["resistance"] = single_equipment.resistance
        equipment[group_key][key]["durability"] = single_equipment.durability
        self._load_weapon_values(equipment, group_key, key, single_equipment)

    def _load_weapons(self, single_equipment, equipment, key):
        group_key = "weapons"
        equipment.setdefault(group_key, {})
        equipment[group_key].setdefault(key, {})
        equipment[group_key][key]["damage"] = single_equipment.damage
        self._load_weapon_values(equipment, group_key, key, single_equipment)

    def _load_hero(self) -> Dict[str, any]:
        hero = dict()
        hero_data = self.game_state.hero
        hero["health"] = hero_data.health
        hero["base_damage"] = hero_data.base_damage
        hero["location"] = hero_data.location
        hero["weapon_slot"] = hero_data.weapon_slot
        hero["head_slot"] = hero_data.head_slot
        hero["chest_slot"] = hero_data.chest_slot
        hero["legs_slot"] = hero_data.legs_slot
        hero["actions"] = self._get_custom_hero_actions()
        hero["inventory"] = [inventory_item for inventory_item in hero_data.inventory]
        return hero

    def _get_custom_hero_actions(self) -> Dict[str, any]:
        actions = dict()
        for action, value in self.game_state.hero.actions.items():
            if action not in Hero.hero_actions.keys():
                actions[action] = value
        return actions

    @staticmethod
    def _get_custom_actions(item, defaults) -> Dict[str, any]:
        actions = dict()
        for action, value in item.actions.items():
            if action not in defaults:
                actions[action] = value
        return actions

    @staticmethod
    def _store(data):
        now = datetime.now()
        timestamp = f"{now.date()}_{now.hour}-{now.minute}-{now.second}"
        output_path = f"../game_states/game_{timestamp}.json"
        with open(output_path, "w") as output_file:
            json.dump(data, output_file, indent=2)

import json
from datetime import datetime
from typing import Dict

from GameState import GameState
from game_item.Armour import Armour
from game_item.Consumable import Consumable
from game_item.Item import Item
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
        data["environment_objects"] = self._load_environment_objects()
        data["items"] = self._load_items()
        data["equipment"] = self._load_equipment()
        data["hero"] = self._load_hero()
        return data

    def _load_rooms(self) -> Dict[str, any]:
        rooms = dict()
        for key, value in self.game_state.rooms.items():
            room = value
            rooms[key] = dict()
            rooms[key]["description"] = room.description
            rooms[key]["directions"] = room.directions
            rooms[key]["items"] = room.items
            rooms[key]["creatures"] = [creature for creature in room.creatures]
            if room.auto_commands is not None:
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
        return creatures

    def _load_environment_objects(self) -> Dict[str, any]:
        environment_objects = dict()
        for key, value in self.game_state.environment_objects.items():
            environment_object = value
            environment_objects[key] = dict()
            environment_objects[key]["alias"] = [alias_item for alias_item in environment_object.alias]
            environment_objects[key]["unlocked"] = environment_object.unlocked
            environment_objects[key]["description"] = environment_object.description
            environment_objects[key]["actions"] = environment_object.actions
        return environment_objects

    def _load_items(self) -> Dict[str, any]:
        items = dict()
        for key, value in self.game_state.items.items():
            item = value
            group_key = "items"
            if isinstance(value, Consumable):
                group_key = "consumable"
                items.setdefault(group_key, {})
                items[group_key].setdefault(key, {})
                items[group_key][key]["value"] = item.value
            elif isinstance(value, Item):
                group_key = "regular"
                items.setdefault(group_key, {})
                items[group_key].setdefault(key, {})
            items[group_key][key]["description"] = item.description
            items[group_key][key]["alias"] = [alias_item for alias_item in item.alias]
            items[group_key][key]["actions"] = item.actions
        return items

    def _load_equipment(self) -> Dict[str, any]:
        equipment = dict()
        for key, value in self.game_state.equipment.items():
            single_equipment = value
            group_key = "equipment"
            if isinstance(single_equipment, Armour):
                group_key = "armour"
                equipment.setdefault(group_key, {})
                equipment[group_key].setdefault(key, {})
                equipment[group_key][key]["resistance"] = single_equipment.resistance
                equipment[group_key][key]["durability"] = single_equipment.durability
            elif isinstance(single_equipment, Weapon):
                group_key = "weapons"
                equipment.setdefault(group_key, {})
                equipment[group_key].setdefault(key, {})
                equipment[group_key][key]["damage"] = single_equipment.damage
            equipment[group_key][key]["alias"] = [alias_item for alias_item in single_equipment.alias]
            equipment[group_key][key]["slot"] = single_equipment.slot
            equipment[group_key][key]["in_use"] = single_equipment.in_use
            equipment[group_key][key]["description"] = single_equipment.description
        return equipment

    def _load_hero(self) -> Dict[str, any]:
        hero = dict()
        hero_data = self.game_state.hero
        hero["health"] = hero_data.health
        hero["location"] = hero_data.location
        hero["right_hand"] = hero_data.right_hand
        hero["left_hand"] = hero_data.left_hand
        hero["head"] = hero_data.head
        hero["chest"] = hero_data.chest
        hero["legs"] = hero_data.legs
        hero["actions"] = hero_data.actions
        hero["inventory"] = [inventory_item for inventory_item in hero_data.inventory]
        return hero

    @staticmethod
    def _store(data):
        timestamp = datetime.timestamp(datetime.now())
        output_path = f"../game_states/game_{timestamp}.json"
        with open(output_path, "w") as output_file:
            json.dump(data, output_file)

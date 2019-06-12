import json
from json import JSONDecodeError
from typing import Dict

from exceptions.GameStateFileException import GameStateFileException
from game_item.Armour import Armour
from game_item.Consumable import Consumable
from game_item.Creature import Creature
from game_item.Hero import Hero
from game_item.Item import Item
from game_item.Room import Room
from game_item.TransitionObject import TransitionObject
from game_item.Weapon import Weapon


class GameStateLoader:

    def __init__(self, game_data):
        self.game_data = game_data

    def create_rooms(self) -> Dict[str, any]:
        return self._create_dict(Room, "rooms")

    def create_creatures(self) -> Dict[str, any]:
        return self._create_dict(Creature, "creatures")

    def create_transition_objects(self) -> Dict[str, any]:
        return self._create_dict(TransitionObject, "transition_objects")

    def _create_dict(self, obj_class, key_name) -> Dict[str, any]:
        try:
            objects = dict()
            rooms_data = self.game_data[key_name]
            for key, value in rooms_data.items():
                obj = obj_class(value)
                objects[key] = obj
            return objects
        except KeyError as e:
            raise GameStateFileException(f"Failed to read {key_name} data: cannot find key {e}")

    def create_items(self):
        data = ["items", [(Item, "regular"), (Consumable, "consumable")]]
        return self._create_by_class(data)

    def create_equipment(self):
        data = ["equipment", [(Weapon, "weapons"), (Armour, "armour")]]
        return self._create_by_class(data)

    def _create_by_class(self, data):
        key_name = data[0]
        try:
            objects = dict()
            types = data[1]
            for type in types:
                data = self.game_data[key_name][type[1]]
                for key in data:
                    obj = type[0](data[key])
                    objects[key] = obj
            return objects
        except KeyError as e:
            raise GameStateFileException(f"Failed to read {key_name} data: cannot find key {e}")

    def create_hero(self) -> Hero:
        try:
            hero_data = self.game_data['hero']
            return Hero(hero_data)
        except KeyError as e:
            raise GameStateFileException(f"Failed to read hero data: cannot find key {e}")

    @staticmethod
    def read_file(file_path) -> Dict[str, dict]:
        try:
            with open(file_path, encoding='utf-8') as config_file:
                game_data = json.load(config_file)
            return game_data
        except IOError as e:
            raise GameStateFileException(f"Failed to read file: {e}")
        except JSONDecodeError as e:
            raise GameStateFileException(f"Failed to parse JSON file: {e}")

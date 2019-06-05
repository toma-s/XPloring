import json
from typing import Dict

from game_item.Equipment import Equipment
from game_item.Item import Item
from game_item.Consumable import Consumable
from game_item.Weapon import Weapon
from game_item.Armour import Armour
from game_item.Creature import Creature
from game_item.Hero import Hero
from game_item.Room import Room
from game_item.EnvironmentObject import EnvironmentObject


class GameState:

    def __init__(self, file_path: str):
        self.game_data = self.read_file(file_path)

        self.rooms = self.create_dict(Room, 'rooms')
        self.creatures = self.create_dict(Creature, 'creatures')
        self.items = self.create_dict(Item, 'items')
        self.equipment = self.create_dict(Equipment, 'equipment')
        self.environment_objects = self.create_dict(EnvironmentObject, "environment_objects")
        self.hero = self.create_hero()

        #acievements
        self.letters_read_count = 0;

    def create_dict(self, type, key_name) -> Dict[str, any]:
        objects = dict()
        if type is Item:
            data = self.game_data[key_name]["regular"]
            for key in data:
                object = Item(data[key])
                objects[key] = object
            data = self.game_data[key_name]["consumable"]
            for key in data:
                object = Consumable(data[key])
                objects[key] = object
        elif type is Equipment:
            data = self.game_data[key_name]["weapons"]
            for key in data:
                object = Weapon(data[key])
                objects[key] = object
            data = self.game_data[key_name]["armour"]
            for key in data:
                object = Armour(data[key])
                objects[key] = object
        else:
            rooms_data = self.game_data[key_name]
            for key, value in rooms_data.items():
                object = type(value)
                objects[key] = object
        return objects

    def create_hero(self) -> Hero:
        hero_data = self.game_data['hero']
        return Hero(hero_data)

    @staticmethod
    def read_file(file_path) -> Dict[str, dict]:
        with open(file_path, encoding='utf-8') as config_file:
            game_data = json.load(config_file)
        return game_data

import json
from typing import Dict

from src.Equipment import Equipment
from src.Item import Item
from src.Creature import Creature
from src.Hero import Hero
from src.Room import Room


class GameState:

    def __init__(self, file_path: str):
        self.game_data = self.read_file(file_path)

        self.rooms = self.create_dict(Room, 'rooms')
        self.creatures = self.create_dict(Creature, 'creatures')
        self.items = self.create_dict(Item, 'items')
        self.equipment = self.create_dict(Equipment, 'equipment')
        self.hero = self.create_hero()

    def create_dict(self, type, key_name) -> Dict[str, any]:
        objects = dict()
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

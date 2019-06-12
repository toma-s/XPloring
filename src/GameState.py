from GameStateLoader import GameStateLoader
from exceptions.GameStateFileException import GameStateFileException
from game_item.Armour import Armour
from game_item.Consumable import Consumable
from game_item.Item import Item
from game_item.Weapon import Weapon


class GameState:

    def __init__(self, file_path: str):
        try:
            game_data = GameStateLoader.read_file(file_path)
            loader = GameStateLoader(game_data)

            self.rooms = loader.create_rooms()
            self.creatures = loader.create_creatures()
            self.transition_objects = loader.create_transition_objects()
            self.items = loader.create_items()
            self.equipment = loader.create_equipment()
            self.hero = loader.create_hero()
        except GameStateFileException as e:
            raise GameStateFileException(e)

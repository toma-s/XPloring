import unittest
from os.path import join

from GameState import GameState
from exceptions.GameStateFileException import GameStateFileException


class TestGameState(unittest.TestCase):
    parent_path = '..\\game_states'

    # read file

    def test_game0_repr(self):
        game_config = "game0_repr.json"
        try:
            GameState(join(self.parent_path, game_config))
        except GameStateFileException:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_not_existing(self):
        expected_message = "Failed to read file: " \
                           "[Errno 2] No such file or directory: " \
                           "'..\\\game_states\\\game_not_existing.json'"
        game_config = "game_not_existing.json"
        with self.assertRaises(GameStateFileException) as e:
            GameState(join(self.parent_path, game_config))
        self.assertEqual(expected_message, str(e.exception))

    def test_wrong_format(self):
        expected_message = "Failed to parse JSON file: " \
                           "Expecting value: line 1 column 1 (char 0)"
        game_config = "game_wrong_emptyfile.txt"
        with self.assertRaises(GameStateFileException) as e:
            GameState(join(self.parent_path, game_config))
        self.assertEqual(expected_message, str(e.exception))

    # load to objects

    def test_wrong_hero(self):
        expected_message = "Failed to read hero data: cannot find key 'location'"
        game_config = "game_wrong_hero.json"
        with self.assertRaises(GameStateFileException) as e:
            GameState(join(self.parent_path, game_config))
        self.assertEqual(expected_message, str(e.exception))

    def test_wrong_rooms(self):
        expected_message = "Failed to read rooms data: cannot find key 'description'"
        game_config = "game_wrong_rooms.json"
        with self.assertRaises(GameStateFileException) as e:
            GameState(join(self.parent_path, game_config))
        self.assertEqual(expected_message, str(e.exception))

    def test_wrong_creatures(self):
        expected_message = "Failed to read creatures data: cannot find key 'alias'"
        game_config = "game_wrong_creatures.json"
        with self.assertRaises(GameStateFileException) as e:
            GameState(join(self.parent_path, game_config))
        self.assertEqual(expected_message, str(e.exception))

    def test_wrong_items(self):
        expected_message = "Failed to read items data: cannot find key 'actions'"
        game_config = "game_wrong_items.json"
        with self.assertRaises(GameStateFileException) as e:
            GameState(join(self.parent_path, game_config))
        self.assertEqual(expected_message, str(e.exception))

    def test_wrong_equipment(self):
        expected_message = "Failed to read equipment data: cannot find key 'resistance'"
        game_config = "game_wrong_equipment.json"
        with self.assertRaises(GameStateFileException) as e:
            GameState(join(self.parent_path, game_config))
        self.assertEqual(expected_message, str(e.exception))

import unittest
import contextlib
import io
from os.path import join

from GameState import GameState
from exceptions.GameStateFileException import GameStateFileException


class TestGameState(unittest.TestCase):

    parent_path = '..\\game_states'

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
        game_config = "game_wrong_format.txt"
        with self.assertRaises(GameStateFileException) as e:
            GameState(join(self.parent_path, game_config))
        self.assertEqual(expected_message, str(e.exception))

import unittest
from unittest import TestCase


from GameState import GameState
from testing.TestingGameStateSaver import TestingGameStateSaver


TestCase.maxDiff = None


class TestGameStateSaver(unittest.TestCase):

    def test_save(self):
        file_path = "../game_states/game0_repr.json"
        game_state = GameState(file_path)
        saver = TestingGameStateSaver(game_state)
        result = saver.save()
        with open(file_path, "r") as game_state_file:
            expected = game_state_file.read()
        print(result)
        self.assertEqual(expected, result)

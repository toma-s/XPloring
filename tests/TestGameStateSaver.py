import unittest

from GameState import GameState
from GameStateSaver import GameStateSaver


class TestGameStateSaver(unittest.TestCase):

    @staticmethod
    def _save():
        file_path = "../game_states/game0_repr.json"
        game_state = GameState(file_path)
        saver = GameStateSaver(game_state)
        saver.save()

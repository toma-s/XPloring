import unittest

from GameState import GameState
from src.InputHandler import InputHandler


class TestInputHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

    def test_synonym(self):
        self.assertEqual(["go"], self.ih.parse_user_input("run"))

    def test_unknown_word(self):
        self.assertEqual(["runy"], self.ih.parse_user_input("runy"))

    def test_more_mords_with_synonym(self):
        self.assertEqual(["go", "north"], self.ih.parse_user_input("move north"))

if __name__ == '__main__':
    unittest.main()
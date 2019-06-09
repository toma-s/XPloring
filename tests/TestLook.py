import contextlib
import io
import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestInventory(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.ih1 = InputHandler(self.game_state1)

        self.map_capital_alias = '../game_states/game_capital_alias.json'
        self.game_state_capital_alias = GameState(self.map_capital_alias)
        self.ih_capital_alias = InputHandler(self.game_state_capital_alias)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

        del self.game_state1
        del self.ih1

        del self.game_state_capital_alias
        del self.ih_capital_alias

    def test_look_entrance(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("look")
        result_output = stdout.getvalue()
        expected_output = "Entrance room.\n" \
                          "There is a key. This key opens armory door.\n" \
                          "There is a key. This key opens kitchen door.\n" \
                          "There are no enemies around.\n" \
                          "There is crossroad room to the NORTH.\n"
        self.assertEqual(expected_output, result_output)

    def test_look_crossroad(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("look")
        result_output = stdout.getvalue()
        expected_output = "Crossroad room.\n" \
                          "There are no enemies around.\n" \
                          "There is door to the WEST.\n" \
                          "There is door to the EAST.\n" \
                          "There is entrance room to the SOUTH.\n"
        self.assertEqual(expected_output, result_output)

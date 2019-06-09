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

    def test_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.execute_commands(["inventory"])
        result_output = stdout.getvalue()
        expected_output = "Your inventory is empty.\n"
        self.assertEqual(expected_output, result_output)

    def test_inv(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inv")
        result_output = stdout.getvalue()
        expected_output = "Your inventory is empty.\n"
        self.assertEqual(expected_output, result_output)

    def test_inventory_sword(self):
        self.ih.execute_commands(["take", "sword"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.execute_commands(["inventory"])
        result_output = stdout.getvalue()
        expected_output = "sword - Sword made of pure silver with a straight " \
                          "double-edged blade and a grip for two-handed use\n"
        self.assertEqual(expected_output, result_output)

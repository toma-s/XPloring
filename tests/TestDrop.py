import contextlib
import io
import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestDrop(unittest.TestCase):

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

    def test_drop(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drop")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_discard(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("discard")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_dump(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("dump")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_discard(self):
        self.ih.handle_user_input("take envelope")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("discard")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(1, len(self.game_state.hero.inventory))

    def test_drop_nonsense_not_in_inv(self):
        self.ih.handle_user_input("take envelope")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drop nothinggg")
        result_output = stdout.getvalue()
        expected_output = "There is no nothinggg around.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(1, len(self.game_state.hero.inventory))

    def test_drop_sword_not_in_inv(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drop sword")
        result_output = stdout.getvalue()
        expected_output = "You don't have that in your inventory.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(0, len(self.game_state.hero.inventory))

    def test_drop_sword_inv(self):
        self.ih.handle_user_input("take sword")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drop sword")
        result_output = stdout.getvalue()
        expected_output = "Item removed from inventory.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(0, len(self.game_state.hero.inventory))

    def test_inventory_sword_equipped(self):
        self.ih.handle_user_input("take sword")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.ih.handle_user_input("equip sword")
        self.assertEqual("#equipment_silver_sword", self.game_state.hero.weapon_slot)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drop sword")
        result_output = stdout.getvalue()
        expected_output = "Item unequipped.\n"\
                          "Item removed from inventory.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(None, self.game_state.hero.weapon_slot)
        self.assertEqual(0, len(self.game_state.hero.inventory))







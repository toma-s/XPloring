import contextlib
import io
import unittest

from InputHandler import InputHandler
from GameState import GameState


class TestEquipment(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map_two_helmets = '../game_states/game_two_helmets.json'
        self.game_two_helmets = GameState(self.map_two_helmets)
        self.ih_two_helmets = InputHandler(self.game_two_helmets)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

    def test_equip_item_in_inventory(self):
        self.ih.handle_user_input("take sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip sword")
        result_output = stdout.getvalue()
        expected_output = "Item equipped\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#equipment_silver_sword", self.game_state.hero.right_hand)

    def test_equip_same_item_twice(self):
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip sword")
        result_output = stdout.getvalue()
        expected_output = "It is already equipped.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#equipment_silver_sword", self.game_state.hero.right_hand)

    def test_equip_occupied_slot(self):
        self.ih_two_helmets.handle_user_input("take helmet1")
        self.ih_two_helmets.handle_user_input("equip helmet1")
        self.assertEqual("#helmet1", self.game_two_helmets.hero.head)
        self.ih_two_helmets.handle_user_input("take helmet2")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_two_helmets.handle_user_input("equip helmet2")
        result_output = stdout.getvalue()
        expected_output = "Item equipped\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#helmet2", self.game_two_helmets.hero.head)
        self.assertIn("#helmet2", self.game_two_helmets.hero.inventory)

    def test_equip_already_equipped(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip helmet")
            self.ih.handle_user_input("equip chestplate")
            self.ih.handle_user_input("equip sword")
        result_output = stdout.getvalue()
        expected_output = f"It is already equipped.\nIt is already equipped.\nIt is already equipped.\n"
        self.assertEqual(expected_output, result_output)
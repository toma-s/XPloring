import contextlib
import io
import unittest

from InputHandler import InputHandler
from GameState import GameState


class TestUnequip(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

    def test_unequip_no_target(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_unequip_helmet_not_in_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip helmet")
        result_output = stdout.getvalue()
        expected_output = "It is not equipped.\n"
        self.assertEqual(expected_output, result_output)

    def test_unequip_helmet_in_inventory_not_equipped(self):
        self.ih.handle_user_input("take helmet")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip helmet")
        result_output = stdout.getvalue()
        expected_output = "It is not equipped.\n"
        self.assertEqual(expected_output, result_output)

    def test_unequip_sword_not_in_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip sword")
        result_output = stdout.getvalue()
        expected_output = "It is not equipped.\n"
        self.assertEqual(expected_output, result_output)

    def test_unequip_sword_in_inventory_not_equipped(self):
        self.ih.handle_user_input("take sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip sword")
        result_output = stdout.getvalue()
        expected_output = "It is not equipped.\n"
        self.assertEqual(expected_output, result_output)

    def test_unequip_envelope_room(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip envelope")
        result_output = stdout.getvalue()
        expected_output = "Action \"unequip\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_unequip_envelope_inv(self):
        self.ih.handle_user_input("take envelope")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip envelope")
        result_output = stdout.getvalue()
        expected_output = "Action \"unequip\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_unequip_helmet_equipped(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        hero = self.game_state.hero
        self.assertEqual(hero.head_slot, "#equipment_gladiator_helmet")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip helmet")
        result_output = stdout.getvalue()
        expected_output = "Item unequipped.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(hero.head_slot, None)

    def test_unequip_sword_equipped(self):
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")
        hero = self.game_state.hero
        self.assertEqual(hero.weapon_slot, "#equipment_silver_sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unequip sword")
        result_output = stdout.getvalue()
        expected_output = "Item unequipped.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(hero.weapon_slot, None)

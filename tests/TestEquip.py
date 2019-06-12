import contextlib
import io
import unittest

from InputHandler import InputHandler
from GameState import GameState


class TestEquip(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.ih1 = InputHandler(self.game_state1)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

        del self.game_state1
        del self.ih1

    def test_equip(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_regular_item_room(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip envelope")
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_regular_item_inv(self):
        self.ih.handle_user_input("take envelope")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip envelope")
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip bandage")
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with the bandage.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip sword")
        result_output = stdout.getvalue()
        expected_output = "You don't have that in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip helmet")
        result_output = stdout.getvalue()
        expected_output = "You don't have that in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip west")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_creature(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip dragon")
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with the dragon.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip inventory")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_item_not_in_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip sword")
        result_output = stdout.getvalue()
        expected_output = "You don't have that in your inventory.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(None, self.game_state.hero.weapon_slot)

    def test_equip_key(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("equip sword")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("attack dragon")
        self.ih.handle_user_input("attack dragon")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip key")
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with the key.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("equip key")
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_door(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("equip door")
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with the door.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_door_ambiguous(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("equip door")
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

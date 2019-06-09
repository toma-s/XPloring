import contextlib
import io
import unittest

from InputHandler import InputHandler
from GameState import GameState


class TestUse(unittest.TestCase):

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
    
    def test_use(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use envelope")
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use bandage")
        result_output = stdout.getvalue()
        expected_output = "You do not have it in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use sword")
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the sword.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use helmet")
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the helmet.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use west")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_creature(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use dragon")
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the dragon.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use inventory")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_key(self):
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
            self.ih.handle_user_input("use key")
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the key.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("use key")
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_door(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use door")
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the door.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_door_ambiguous(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("use door")
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_attach_dragon(self):
        self.ih.handle_user_input("go west")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attach dragon")
        result_output = stdout.getvalue()
        expected_output = "Action \"attach\" is not allowed with the dragon.\n"
        self.assertEqual(expected_output, result_output)

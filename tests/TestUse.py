import contextlib
import io
import unittest

from CommandHandler import CommandHandler
from GameState import GameState


class TestUse(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.cr1 = CommandHandler(self.game_state1)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

        del self.game_state1
        del self.cr1
    
    def test_use(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use"])
        result_output = stdout.getvalue()
        expected_output = "You don't know how to do that.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "potion"])
        result_output = stdout.getvalue()
        expected_output = "You do not have it in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "sword"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the sword.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the helmet.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "west"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_creature(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the dragon.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "inventory"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_key(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["equip", "sword"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["go", "west"])
        self.cr.execute(["attack", "dragon"])
        self.cr.execute(["attack", "dragon"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "key"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the key.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["use", "key"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "door"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with the door.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_door_ambiguous(self):
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["use", "door"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_attach_dragon(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attach", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attach\" is not allowed with the dragon.\n"
        self.assertEqual(expected_output, result_output)

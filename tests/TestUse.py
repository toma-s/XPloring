import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState


class TestUse(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

        self.map2keys = '../game_states/game_2_locked_doors_repr.json'
        self.game_state2keys = GameState(self.map2keys)
        self.cr2keys = CommandRunner(self.game_state2keys)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

        del self.game_state2keys
        del self.cr2keys
    
    def test_use(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use"])
        result_output = stdout.getvalue()
        expected_output = "I don't understand. Try again.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

    def test_use_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "potion"])
        result_output = stdout.getvalue()
        expected_output = "You do not have a required item to do this action.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "sword"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with \"sword\".\n"
        self.assertEqual(expected_output, result_output)

    def test_use_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with \"helmet\".\n"
        self.assertEqual(expected_output, result_output)

    def test_use_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "west"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with \"west\".\n"
        self.assertEqual(expected_output, result_output)

    def test_use_creature(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with \"dragon\".\n"
        self.assertEqual(expected_output, result_output)

    def test_use_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "inventory"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with \"inventory\".\n"
        self.assertEqual(expected_output, result_output)

    def test_use_key(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["equip", "sword"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["go", "west"])
        self.cr.execute(["use", "dragon"])
        self.cr.execute(["use", "dragon"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "key"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"key\".\n"
        self.assertEqual(expected_output, result_output)

    def test_use_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["use", "key"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "door"])
        result_output = stdout.getvalue()
        expected_output = "Action \"use\" is not allowed with \"door\".\n"
        self.assertEqual(expected_output, result_output)

    def test_use_door_ambiguous(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["use", "door"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)
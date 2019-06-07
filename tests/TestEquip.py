import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState


class TestCombat(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr


    def test_equip(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip"])
        result_output = stdout.getvalue()
        expected_output = "I don't understand. Try again.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "You can't equip envelope\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_consumable(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "potion"])
        result_output = stdout.getvalue()
        expected_output = "You can't equip potion\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = "You don't have sword in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "You don't have helmet in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "west"])
        result_output = stdout.getvalue()
        expected_output = "You can't equip west\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_creature(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "You can't equip dragon\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "head"])
        result_output = stdout.getvalue()
        expected_output = "You can't equip dragon\n"
        self.assertEqual(expected_output, result_output)

import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState


class TestEquip(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

        self.map_two_helmets = '../game_states/game_two_helmets.json'
        self.game_two_helmets = GameState(self.map_two_helmets)
        self.cr_two_helmets = CommandRunner(self.game_two_helmets)

        self.map2keys = '../game_states/game_2_locked_doors_repr.json'
        self.game_state2keys = GameState(self.map2keys)
        self.cr2keys = CommandRunner(self.game_state2keys)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

        del self.game_two_helmets
        del self.cr_two_helmets

        del self.game_state2keys
        del self.cr2keys

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
        expected_output = "Action \"equip\" is not allowed with envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "potion"])
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with potion.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = "You don't have that in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "You don't have that in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "west"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with west.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_creature(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with dragon.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "inventory"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_item_not_in_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = "You don't have that in your inventory.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("none", self.game_state.hero.right_hand)

    def test_equip_key(self):
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
            self.cr.execute(["equip", "key"])
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with key.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["equip", "key"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "door"])
        result_output = stdout.getvalue()
        expected_output = "Action \"equip\" is not allowed with door.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_door_ambiguous(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["equip", "door"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

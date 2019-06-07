import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState


class TestAttack(unittest.TestCase):

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

    def test_attack(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack"])
        result_output = stdout.getvalue()
        expected_output = "I don't understand. Try again.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "potion"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the potion.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "sword"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the sword.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the helmet.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "west"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with west.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_creature(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "You hit the green dragon for 1 damage! Green dragon has 59 HP left.\n" \
                          "Green dragon hit you for 10 damage! You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "inventory"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_key(self):
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
            self.cr.execute(["attack", "key"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the key.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["attack", "key"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "door"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the door.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_door_ambiguous(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["attack", "door"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

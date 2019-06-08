import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState
from InputHandler import InputHandler


class TestExamine(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

        self.map2keys = '../game_states/game_2_locked_doors_repr.json'
        self.game_state2keys = GameState(self.map2keys)
        self.cr2keys = CommandRunner(self.game_state2keys)

        self.map_capital_alias = '../game_states/game_capital_alias.json'
        self.game_state_capital_alias = GameState(self.map_capital_alias)
        self.cr_capital_alias = CommandRunner(self.game_state_capital_alias)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

        del self.game_state2keys
        del self.cr2keys

        del self.game_state_capital_alias
        del self.cr_capital_alias

    def test_examine(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine"])
        result_output = stdout.getvalue()
        expected_output = "I don't understand. Try again.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "OPEN to get letter from inside\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "potion"])
        result_output = stdout.getvalue()
        expected_output = "Small healing potion. USE it to heal yourself\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "sword"])
        result_output = stdout.getvalue()
        expected_output = "Simple sword for fighting\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "Good ol' steel helmet\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "west"])
        result_output = stdout.getvalue()
        expected_output = "Action \"examine\" is not allowed with west.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_creature(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Big green dragon\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "inventory"])
        result_output = stdout.getvalue()
        expected_output = "Action \"examine\" is not allowed with inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_key(self):
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
            self.cr.execute(["examine", "key"])
        result_output = stdout.getvalue()
        expected_output = "Use this key to unlock the door in the arena\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["examine", "key"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "door"])
        result_output = stdout.getvalue()
        expected_output = "Exit door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_door_ambiguous(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["examine", "door"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    # TESTS ON DIFFERENT CASES

    # regular item

    def test_alias_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("examine Envelope")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Regular Item Envelope\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("examine envelope")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Regular Item Envelope\n"
        self.assertEqual(expected_output, result_output)

    # consumable item

    def test_alias_capital_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("examine Potion")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Regular Item Potion\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("examine potion")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Regular Item Potion\n"
        self.assertEqual(expected_output, result_output)

    # equipment weapon

    def test_alias_capital_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("examine Sword")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Weapon Equipment Sword\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("examine sword")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Weapon Equipment Sword\n"
        self.assertEqual(expected_output, result_output)

    # equipment armour

    def test_alias_capital_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("examine Helmet")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Helmet Equipment\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("examine helmet")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Helmet Equipment\n"
        self.assertEqual(expected_output, result_output)

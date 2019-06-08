import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState
from InputHandler import InputHandler


class TestTake(unittest.TestCase):

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

    def test_take(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take"])
        result_output = stdout.getvalue()
        expected_output = "I don't understand. Try again.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "Envelope has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "potion"])
        result_output = stdout.getvalue()
        expected_output = "Potion has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "sword"])
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "Helmet has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "west"])
        result_output = stdout.getvalue()
        expected_output = "Action \"take\" is not allowed with west.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_creature(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Action \"take\" is not allowed with dragon.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "inventory"])
        result_output = stdout.getvalue()
        expected_output = "Action \"take\" is not allowed with inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_item_in_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "sword"])
            self.cr.execute(["take", "sword"])
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n" \
                          "Sword is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_key(self):
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
            self.cr.execute(["take", "key"])
        result_output = stdout.getvalue()
        expected_output = "Key has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["take", "key"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "door"])
        result_output = stdout.getvalue()
        expected_output = "Action \"take\" is not allowed with door.\n"
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
            commands_to_run = InputHandler().parse_user_input("take Envelope")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Envelope has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take envelope")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Envelope has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take envelope")
            self.cr_capital_alias.execute(commands_to_run)
            commands_to_run = InputHandler().parse_user_input("take Envelope")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Envelope has been added to your inventory.\n" \
                          "Envelope is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    # consumable item

    def test_alias_capital_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take Potion")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Potion has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take potion")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Potion has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take potion")
            self.cr_capital_alias.execute(commands_to_run)
            commands_to_run = InputHandler().parse_user_input("take Potion")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Potion has been added to your inventory.\n"\
                          "Potion is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    # equipment weapon

    def test_alias_capital_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take Sword")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take sword")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take sword")
            self.cr_capital_alias.execute(commands_to_run)
            commands_to_run = InputHandler().parse_user_input("take Sword")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n" \
                          "Sword is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    # equipment armour

    def test_alias_capital_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take Helmet")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Helmet has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take helmet")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Helmet has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("take helmet")
            self.cr_capital_alias.execute(commands_to_run)
            commands_to_run = InputHandler().parse_user_input("take Helmet")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Helmet has been added to your inventory.\n" \
                          "Helmet is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

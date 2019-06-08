import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState
from InputHandler import InputHandler


class TestAttack(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.cr1 = CommandRunner(self.game_state1)

        self.map_capital_alias = '../game_states/game_capital_alias.json'
        self.game_state_capital_alias = GameState(self.map_capital_alias)
        self.cr_capital_alias = CommandRunner(self.game_state_capital_alias)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

        del self.game_state1
        del self.cr1

        del self.game_state_capital_alias
        del self.cr_capital_alias

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
        expected_output = "Action \"attack\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "potion"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the potion.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "sword"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the sword.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the helmet.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "west"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
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
        expected_output = "This action is not allowed with the inventory.\n"
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
        expected_output = "Action \"attack\" is not allowed with the key.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["attack", "key"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "door"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the door.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_door_ambiguous(self):
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["attack", "door"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    # TESTS ON DIFFERENT CASES

    # creature

    def test_alias_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("attack Green Dragon")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "You hit the Green Dragon for 1 damage! " \
                          "Green Dragon has 49 HP left.\n" \
                          "Green Dragon hit you for 10 damage! " \
                          "You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("attack green dragon")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "You hit the Green Dragon for 1 damage! " \
                          "Green Dragon has 49 HP left.\n" \
                          "Green Dragon hit you for 10 damage! " \
                          "You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = InputHandler().parse_user_input("attack green Dragon")
            self.cr_capital_alias.execute(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "You hit the Green Dragon for 1 damage! " \
                          "Green Dragon has 49 HP left.\n" \
                          "Green Dragon hit you for 10 damage! " \
                          "You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

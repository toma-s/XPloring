import contextlib
import io
import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestExamine(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.ih1 = InputHandler(self.game_state1)

        self.map_capital_alias = '../game_states/game_capital_alias.json'
        self.game_state_capital_alias = GameState(self.map_capital_alias)
        self.ih_capital_alias = InputHandler(self.game_state_capital_alias)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

        del self.game_state1
        del self.ih1

        del self.game_state_capital_alias
        del self.ih_capital_alias

    def test_examine(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine"])
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "OPEN to get letter from inside\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "bandage"])
        result_output = stdout.getvalue()
        expected_output = "You can USE bandage to reduce swelling or slow heavy bleeding.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "sword"])
        result_output = stdout.getvalue()
        expected_output = "Sword made of pure silver with a straight double-edged blade and a grip for two-handed use\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "Gladiator helmet made of steel\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "west"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_creature(self):
        self.ih.handle_commands(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Big green dragon\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "inventory"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_key(self):
        self.ih.handle_commands(["take", "helmet"])
        self.ih.handle_commands(["take", "sword"])
        self.ih.handle_commands(["take", "chestplate"])
        self.ih.handle_commands(["equip", "helmet"])
        self.ih.handle_commands(["equip", "sword"])
        self.ih.handle_commands(["equip", "chestplate"])
        self.ih.handle_commands(["go", "west"])
        self.ih.handle_commands(["attack", "dragon"])
        self.ih.handle_commands(["attack", "dragon"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "key"])
        result_output = stdout.getvalue()
        expected_output = "Use this key to unlock the door in the arena\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_commands(["examine", "key"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_door(self):
        self.ih.handle_commands(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_commands(["examine", "door"])
        result_output = stdout.getvalue()
        expected_output = "Exit door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_door_ambiguous(self):
        self.ih1.handle_commands(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_commands(["examine", "door"])
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    # TESTS ON DIFFERENT CASES

    # regular item

    def test_alias_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = self.ih_capital_alias.parse_user_input("examine Envelope")
            self.ih_capital_alias.handle_commands(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Regular Item Envelope\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = self.ih_capital_alias.parse_user_input("examine envelope")
            self.ih_capital_alias.handle_commands(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Regular Item Envelope\n"
        self.assertEqual(expected_output, result_output)

    # consumable item

    def test_alias_capital_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = self.ih_capital_alias.parse_user_input("examine Bandage")
            self.ih_capital_alias.handle_commands(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Regular Item Bandage\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = self.ih_capital_alias.parse_user_input("examine bandage")
            self.ih_capital_alias.handle_commands(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Regular Item Bandage\n"
        self.assertEqual(expected_output, result_output)

    # equipment weapon

    def test_alias_capital_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = self.ih_capital_alias.parse_user_input("examine Sword")
            self.ih_capital_alias.handle_commands(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Weapon Equipment Sword\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = self.ih_capital_alias.parse_user_input("examine sword")
            self.ih_capital_alias.handle_commands(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Weapon Equipment Sword\n"
        self.assertEqual(expected_output, result_output)

    # equipment armour

    def test_alias_capital_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = self.ih_capital_alias.parse_user_input("examine Helmet")
            self.ih_capital_alias.handle_commands(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Helmet Equipment\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            commands_to_run = self.ih_capital_alias.parse_user_input("examine helmet")
            self.ih_capital_alias.handle_commands(commands_to_run)
        result_output = stdout.getvalue()
        expected_output = "Helmet Equipment\n"
        self.assertEqual(expected_output, result_output)

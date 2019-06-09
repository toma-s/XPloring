import contextlib
import io
import unittest

from InputHandler import InputHandler
from GameState import GameState
from InputHandler import InputHandler


class TestTake(unittest.TestCase):

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

    def test_take(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take envelope")
        result_output = stdout.getvalue()
        expected_output = "Envelope has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take bandage")
        result_output = stdout.getvalue()
        expected_output = "Bandage has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take sword")
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take helmet")
        result_output = stdout.getvalue()
        expected_output = "Helmet has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take west")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_creature(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take dragon")
        result_output = stdout.getvalue()
        expected_output = "Action \"take\" is not allowed with the dragon.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take inventory")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_item_in_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take sword")
            self.ih.handle_user_input("take sword")
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n" \
                          "Sword is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_key(self):
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
            self.ih.handle_user_input("take key")
        result_output = stdout.getvalue()
        expected_output = "Key has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_key_ambiguous(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("take key")
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_take_door(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take door")
        result_output = stdout.getvalue()
        expected_output = "Action \"take\" is not allowed with the door.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_door_ambiguous(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("examine door")
        result_output = stdout.getvalue()
        expected_output = "There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    # TESTS ON DIFFERENT CASES

    # regular item

    def test_alias_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take Envelope")
        result_output = stdout.getvalue()
        expected_output = "Envelope has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take envelope")
        result_output = stdout.getvalue()
        expected_output = "Envelope has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_regular_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take envelope")
            self.ih_capital_alias.handle_user_input("take Envelope")
        result_output = stdout.getvalue()
        expected_output = "Envelope has been added to your inventory.\n" \
                          "Envelope is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    # consumable item

    def test_alias_capital_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take Bandage")
        result_output = stdout.getvalue()
        expected_output = "Bandage has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take bandage")
        result_output = stdout.getvalue()
        expected_output = "Bandage has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_consumable_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take bandage")
            self.ih_capital_alias.handle_user_input("take Bandage")
        result_output = stdout.getvalue()
        expected_output = "Bandage has been added to your inventory.\n"\
                          "Bandage is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    # equipment weapon

    def test_alias_capital_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take Sword")
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take sword")
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_equipment_weapon(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take sword")
            self.ih_capital_alias.handle_user_input("take Sword")
        result_output = stdout.getvalue()
        expected_output = "Sword has been added to your inventory.\n" \
                          "Sword is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    # equipment armour

    def test_alias_capital_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take Helmet")
        result_output = stdout.getvalue()
        expected_output = "Helmet has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take helmet")
        result_output = stdout.getvalue()
        expected_output = "Helmet has been added to your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_alias_lower_capital_equipment_armour(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih_capital_alias.handle_user_input("take helmet")
            self.ih_capital_alias.handle_user_input("take Helmet")
        result_output = stdout.getvalue()
        expected_output = "Helmet has been added to your inventory.\n" \
                          "Helmet is already in your inventory.\n"
        self.assertEqual(expected_output, result_output)

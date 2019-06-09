import contextlib
import io
import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestInventory(unittest.TestCase):

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

    def test_inventory(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "Your inventory is empty.\n"
        self.assertEqual(expected_output, result_output)

    def test_inv(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inv")
        result_output = stdout.getvalue()
        expected_output = "Your inventory is empty.\n"
        self.assertEqual(expected_output, result_output)

    def test_inventory_sword(self):
        self.ih.handle_user_input("take sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "sword - Sword made of pure silver with a straight " \
                          "double-edged blade and a grip for two-handed use\n"
        self.assertEqual(expected_output, result_output)

    def test_inventory_sword_equipped(self):
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "sword - Sword made of pure silver with a straight " \
                          "double-edged blade and a grip for two-handed use [EQUIPPED]\n"
        self.assertEqual(expected_output, result_output)

    def test_inventory_two_armour(self):
        self.ih.handle_user_input("take gladiator helmet")
        self.ih.handle_user_input("equip steel helmet")
        self.ih.handle_user_input("take steel chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.assertEqual("#equipment_steel_chestplate", self.game_state.hero.chest)
        self.assertEqual("#equipment_gladiator_helmet", self.game_state.hero.head)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "helmet - Gladiator helmet made of steel [EQUIPPED]\n" \
                          "chestplate - Steel chestplate armor [EQUIPPED]\n"
        self.assertEqual(expected_output, result_output)

    def test_inventory_unequip_two_armour(self):
        self.ih.handle_user_input("take gladiator helmet")
        self.ih.handle_user_input("equip steel helmet")
        self.ih.handle_user_input("take steel chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("unequip steel chestplate")
        self.ih.handle_user_input("unequip gladiator helmet")
        self.assertEqual(None, self.game_state.hero.chest)
        self.assertEqual(None, self.game_state.hero.head)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "helmet - Gladiator helmet made of steel\n" \
                          "chestplate - Steel chestplate armor\n"
        self.assertEqual(expected_output, result_output)

    def test_inventory_unequip_two_armour_then_equip(self):
        self.ih.handle_user_input("take gladiator helmet")
        self.ih.handle_user_input("equip steel helmet")
        self.ih.handle_user_input("take steel chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("unequip steel chestplate")
        self.ih.handle_user_input("unequip gladiator helmet")
        self.ih.handle_user_input("equip gladiator helmet")
        self.assertEqual(None, self.game_state.hero.chest)
        self.assertEqual("#equipment_gladiator_helmet", self.game_state.hero.head)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "helmet - Gladiator helmet made of steel [EQUIPPED]\n" \
                          "chestplate - Steel chestplate armor\n"
        self.assertEqual(expected_output, result_output)


    def test_inventory_drop_sword(self):
        self.ih.handle_user_input("take sword")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.ih.handle_user_input("drop sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "Your inventory is empty.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(0, len(self.game_state.hero.inventory))

    def test_inventory_drop_equip_sword(self):
        self.ih.handle_user_input("take sword")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.ih.handle_user_input("equip sword")
        self.assertEqual("#equipment_silver_sword", self.game_state.hero.right_hand)
        self.ih.handle_user_input("drop sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "Your inventory is empty.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(0, len(self.game_state.hero.inventory))

    def test_inventory_drop_equip_two_armour(self):
        self.ih.handle_user_input("take gladiator helmet")
        self.ih.handle_user_input("equip steel helmet")
        self.ih.handle_user_input("take steel chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.assertEqual("#equipment_steel_chestplate", self.game_state.hero.chest)
        self.assertEqual("#equipment_gladiator_helmet", self.game_state.hero.head)
        self.assertEqual(2, len(self.game_state.hero.inventory))
        self.ih.handle_user_input("drop gladiator helmet")
        self.ih.handle_user_input("drop helmet")
        self.ih.handle_user_input("drop steel chestplate")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("inventory")
        result_output = stdout.getvalue()
        expected_output = "Your inventory is empty.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(0, len(self.game_state.hero.inventory))


import contextlib
import io
import unittest

from CommandHandler import CommandHandler
from GameState import GameState


class TestEquipment(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandHandler(self.game_state)

        self.map_two_helmets = '../game_states/game_two_helmets.json'
        self.game_two_helmets = GameState(self.map_two_helmets)
        self.cr_two_helmets = CommandHandler(self.game_two_helmets)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def test_equip_item_in_inventory(self):
        self.cr.handle_commands(["take", "sword"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.handle_commands(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = "Item equipped\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)

    def test_equip_same_item_twice(self):
        self.cr.handle_commands(["take", "sword"])
        self.cr.handle_commands(["equip", "sword"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.handle_commands(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = "It is already equipped.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)

    def test_equip_occupied_slot(self):
        self.cr_two_helmets.handle_commands(["take", "helmet1"])
        self.cr_two_helmets.handle_commands(["equip", "helmet1"])
        self.assertEqual("#helmet1", self.game_two_helmets.hero.head)
        self.cr_two_helmets.handle_commands(["take", "helmet2"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr_two_helmets.handle_commands(["equip", "helmet2"])
        result_output = stdout.getvalue()
        expected_output = "Item equipped\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#helmet2", self.game_two_helmets.hero.head)
        self.assertIn("#helmet2", self.game_two_helmets.hero.inventory)

    def test_equip_already_equipped(self):
        self.cr.handle_commands(["take", "helmet"])
        self.cr.handle_commands(["equip", "helmet"])
        self.cr.handle_commands(["take", "chestplate"])
        self.cr.handle_commands(["equip", "chestplate"])
        self.cr.handle_commands(["take", "sword"])
        self.cr.handle_commands(["equip", "sword"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.handle_commands(["equip", "helmet"])
            self.cr.handle_commands(["equip", "chestplate"])
            self.cr.handle_commands(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = f"It is already equipped.\nIt is already equipped.\nIt is already equipped.\n"
        self.assertEqual(expected_output, result_output)
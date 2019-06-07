import unittest
import contextlib
import io


from CommandRunner import CommandRunner
from GameState import GameState


class TestInput(unittest.TestCase):

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





    def test_equip_full_armor(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)
        self.assertEqual("#equipment_golden_chestplate", self.game_state.hero.chest)
        self.assertEqual("#equipment_steel_helmet", self.game_state.hero.head)

    def test_equip_envelope_room(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["equip", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"You don't have envelope in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_envelope_inv(self):
        self.cr2keys.execute(["take", "envelope"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["equip", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"You don't have envelope in your inventory.\n"
        self.assertEqual(expected_output, result_output)


    def test_equip_already_equipped(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "helmet"])
            self.cr.execute(["equip", "chestplate"])
            self.cr.execute(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = f"You are already equipped with helmet\nYou are already equipped with chestplate\nYou are already equipped with sword\n"
        self.assertEqual(expected_output, result_output)

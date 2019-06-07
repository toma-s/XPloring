import contextlib
import io
import unittest

from src.GameState import GameState
from src.CommandRunner import CommandRunner


class TestItems(unittest.TestCase):

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

    def testInternalSpawnItem(self):
        self.cr.execute(["open", "envelope"])
        room_items = self.game_state.rooms[self.game_state.hero.location].items
        self.assertIn("#item_letter", room_items, "Letter should appear in room after opening an envelope")
        self.assertNotIn("#item_envelope", room_items, "After envelope was opened it should have disappeared")


    def testInternalTakeItem(self):
        self.cr.execute(["take", "sword"])
        room_items = self.game_state.rooms[self.game_state.hero.location].items
        self.assertNotIn("#equipment_steel_sword", room_items, "You took the sword, why is it still in the room ???")

    def testGoThroughtLockedDoor(self):
        self.cr.execute(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)
        self.cr.execute(["go", "north"])
        self.assertEqual("#room_arena", self.game_state.hero.location)

    def testTakeItemCheckInventory(self):
        self.cr.execute(["take", "sword"])
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.assertIn("#equipment_steel_sword", self.game_state.hero.inventory)

    def test_open_nonexisting_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envel"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"envel\".\n"
        self.assertEqual(expected_output, result_output)

    def test_nonexisting_action_ope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["ope", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"Action \"ope\" is not allowed with \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

    def test_both_nonexisting_ope_enveep(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["ope", "enveep"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"enveep\".\n"
        self.assertEqual(expected_output, result_output)

    def test_nonexisting_action_read(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["read", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"Action \"read\" is not allowed with \"envelope\".\n"
        self.assertEqual(expected_output, result_output)


    def test_take_keys_with_same_alias(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["take", "key"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_keys_with_same_alias(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["examine", "key"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_nonexistent_action_keys_with_same_alias(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["read", "key"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"key\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)



    def testReadEnvelope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["read", "envelope"])

        result_output = stdout.getvalue()
        expected_output = "Action \"read\" is not allowed with \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

    def test_open_envelope_room(self):
        self.assertIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertNotIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

        self.cr.execute(["open", "envelope"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

        self.assertNotIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

    def test_open_envelope_inventory(self):
        self.assertIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertNotIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

        self.cr.execute(["take", "envelope"])
        self.cr.execute(["open", "envelope"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

        self.assertNotIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertIn("#item_letter", self.game_state.rooms['#room_entrance'].items)



    # -- attack non creatures --

    def test_attack_envelope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_helmet(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the \"helmet\".\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_door(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "door"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the \"door\".\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_nonexistent(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "nothing"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"nothing\".\n"
        self.assertEqual(expected_output, result_output)



if __name__ == '__main__':
    unittest.main()

import contextlib
import io
import unittest

from src.GameState import GameState
from src.CommandHandler import CommandHandler


class TestItems(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.cr1 = CommandHandler(self.game_state1)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def test_internal_spawn_item(self):
        self.cr.execute(["open", "envelope"])
        room_items = self.game_state.rooms[self.game_state.hero.location].items
        self.assertIn("#item_letter", room_items, "Letter should appear in room after opening an envelope")
        self.assertNotIn("#item_envelope", room_items, "After envelope was opened it should have disappeared")


    def test_internal_take_item(self):
        self.cr.execute(["take", "sword"])
        room_items = self.game_state.rooms[self.game_state.hero.location].items
        self.assertNotIn("#equipment_steel_sword", room_items, "You took the sword, why is it still in the room ???")

    def test_go_throught_locked_door(self):
        self.cr.execute(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)
        self.cr.execute(["go", "north"])
        self.assertEqual("#room_arena", self.game_state.hero.location)

    def test_take_sword(self):
        self.cr.execute(["take", "sword"])
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.assertIn("#equipment_steel_sword", self.game_state.hero.inventory)

    def test_open_nonexisting_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envel"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as envel.\n"
        self.assertEqual(expected_output, result_output)

    def test_nonexisting_action_ope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["ope", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"Action \"ope\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_both_nonexisting_ope_enveep(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["ope", "enveep"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as enveep.\n"
        self.assertEqual(expected_output, result_output)

    def test_read_envelope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["read", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "Action \"read\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_open_envelope_room(self):
        self.cr.execute(["open", "envelope"])

        self.assertNotIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as envelope.\n"
        self.assertEqual(expected_output, result_output)



    def test_open_envelope_inventory(self):
        self.cr.execute(["take", "envelope"])
        self.cr.execute(["open", "envelope"])

        self.assertNotIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as envelope.\n"
        self.assertEqual(expected_output, result_output)

        def test_take_keys_with_same_alias(self):
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.cr1.execute(["take", "key"])
            result_output = stdout.getvalue()
            expected_output = f"There are 2 \"key\". You have to be more specific.\n"
            self.assertEqual(expected_output, result_output)

        def test_examine_keys_with_same_alias(self):
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.cr1.execute(["examine", "key"])
            result_output = stdout.getvalue()
            expected_output = f"There are 2 \"key\". You have to be more specific.\n"
            self.assertEqual(expected_output, result_output)

        def test_nonexistent_action_keys_with_same_alias(self):
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.cr1.execute(["read", "key"])
            result_output = stdout.getvalue()
            expected_output = f"There are 2 \"key\". You have to be more specific.\n"
            self.assertEqual(expected_output, result_output)

    # -- attack non creatures --

    def test_attack_envelope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_helmet(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "helmet"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the helmet.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_door(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "door"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attack\" is not allowed with the door.\n"
        self.assertEqual(expected_output, result_output)

    def test_attack_nonexistent(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "nothing"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as nothing.\n"
        self.assertEqual(expected_output, result_output)



if __name__ == '__main__':
    unittest.main()

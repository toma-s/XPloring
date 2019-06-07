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

    # -- game0 (arena)--
    def test_examine_arena_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["examine", "door"])
        result_output = stdout.getvalue()
        expected_output = f"Exit door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_open_arena_door(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "door"])
        result_output = stdout.getvalue()
        expected_output = f"Exit door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_arena_door_nokey(self):
        self.cr.execute(["go", "west"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["unlock", "door"])
        result_output = stdout.getvalue()
        expected_output = f"You do not have a required item to do this action.\n"
        self.assertEqual(expected_output, result_output)


    # -- game2keys --

    def test_open_doors_with_same_alias(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["open", "door"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_armory_door(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["examine", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_open_locked_door_nokey(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["open", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_open_locked_door_haskey(self):
        self.cr2keys.execute(["take", "armory key"])
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["open", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_armory_door_nokey(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["unlock", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"You do not have a required item to do this action.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_armory_door_has_key(self):
        self.cr2keys.execute(["take", "armory key"])
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["unlock", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Armory door is unlocked, you may go through.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_doors_with_same_alias_nokey(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["unlock", "door"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\"-s. You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_doors_with_same_alias_haskey(self):
        self.cr2keys.execute(["take", "armory key"])
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["unlock", "door"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\"-s. You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)
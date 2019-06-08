import unittest
import contextlib
import io


from CommandHandler import CommandHandler
from GameState import GameState


class TestInput(unittest.TestCase):

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

        del self.game_state1
        del self.cr1

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


    # -- game1 --

    def test_open_doors_with_same_alias(self):
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["open", "door"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_armory_door(self):
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["examine", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_open_locked_door_nokey(self):
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["open", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_open_locked_door_haskey(self):
        self.cr1.execute(["take", "armory key"])
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["open", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_armory_door_nokey(self):
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["unlock", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"You do not have a required item to do this action.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_armory_door_has_key(self):
        self.cr1.execute(["take", "armory key"])
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["unlock", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Armory door is unlocked, you may go through.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_doors_with_same_alias_nokey(self):
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["unlock", "door"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_doors_with_same_alias_haskey(self):
        self.cr1.execute(["take", "armory key"])
        self.cr1.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["unlock", "door"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)
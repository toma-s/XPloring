import unittest
import contextlib
import io

from InputHandler import InputHandler
from GameState import GameState


class TestInput(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.ih1 = InputHandler(self.game_state1)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

        del self.game_state1
        del self.ih1

    # -- game0 (arena)--
    def test_examine_arena_door(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("examine door")
        result_output = stdout.getvalue()
        expected_output = f"Exit door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_open_arena_door(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("open door")
        result_output = stdout.getvalue()
        expected_output = f"Exit door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_arena_door_no_key(self):
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("unlock door")
        result_output = stdout.getvalue()
        expected_output = f"You don't have a required item to do this action.\n"
        self.assertEqual(expected_output, result_output)

    # -- game1 --
    def test_open_doors_with_same_alias(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("open door")
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_armory_door(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("examine armory door")
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_open_locked_door_no_key(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("open armory door")
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_open_locked_door_has_key(self):
        self.ih1.handle_user_input("take armory key")
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("open armory door")
        result_output = stdout.getvalue()
        expected_output = f"Armory door is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_armory_door_no_key(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("unlock armory door")
        result_output = stdout.getvalue()
        expected_output = f"You don't have a required item to do this action.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_armory_door_has_key(self):
        self.ih1.handle_user_input("take armory key")
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("unlock armory door")
        result_output = stdout.getvalue()
        expected_output = f"Armory door is unlocked, you may go through.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_doors_with_same_alias_no_key(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("unlock door")
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_doors_with_same_alias_has_key(self):
        self.ih1.handle_user_input("take armory key")
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("unlock door")
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\". You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

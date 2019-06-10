import contextlib
import io
import unittest

from src.GameState import GameState
from src.InputHandler import InputHandler


class TestMoving(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

    def test_move_invalid(self):
        self.ih.handle_user_input("go east")
        self.assertEqual("#room_entrance", self.game_state.hero.location)

    def test_move_valid(self):
        self.ih.handle_user_input("go west")
        self.assertEqual("#room_arena", self.game_state.hero.location)

    def test_move_back_and_forth(self):
        self.ih.handle_user_input("go west")
        self.assertEqual("#room_arena", self.game_state.hero.location)
        self.ih.handle_user_input("go east")

    def test_move_locked_door(self):
        self.ih.handle_user_input("go west")
        self.assertEqual("#room_arena", self.game_state.hero.location)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("go north")
        result_output = stdout.getvalue()
        expected_output = "You can't go north. The door is locked.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#room_arena", self.game_state.hero.location)

    def test_do_south(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("do south")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the south.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_north(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("do north")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the north.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_west(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("do west")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_east(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("do east")
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the east.\n"
        self.assertEqual(expected_output, result_output)

    def test_go_no_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("go")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

    def test_move_no_direction(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("move")
        result_output = stdout.getvalue()
        expected_output = "I don't understand that command.\n"
        self.assertEqual(expected_output, result_output)

if __name__ == '__main__':
    unittest.main()
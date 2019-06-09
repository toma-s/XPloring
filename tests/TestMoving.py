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
        self.ih.execute_commands(["go", "east"])
        self.assertEqual("#room_entrance", self.game_state.hero.location)

    def test_move_valid(self):
        self.ih.execute_commands(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)

    def test_move_back_and_forth(self):
        self.ih.execute_commands(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)
        self.ih.execute_commands(["go", "east"])


    def test_do_south(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.execute_commands(["do", "south"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the south.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_north(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.execute_commands(["do", "north"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the north.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_west(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.execute_commands(["do", "west"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_east(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.execute_commands(["do", "east"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the east.\n"
        self.assertEqual(expected_output, result_output)

if __name__ == '__main__':
    unittest.main()
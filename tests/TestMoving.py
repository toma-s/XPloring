import contextlib
import io
import unittest

from src.GameState import GameState
from src.CommandHandler import CommandHandler


class TestMoving(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def test_move_invalid(self):
        self.cr.execute(["go", "east"])
        self.assertEqual("#room_entrance", self.game_state.hero.location)

    def test_move_valid(self):
        self.cr.execute(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)

    def test_move_back_and_forth(self):
        self.cr.execute(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)
        self.cr.execute(["go", "east"])


    def test_do_south(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["do", "south"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the south.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_north(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["do", "north"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the north.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_west(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["do", "west"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the west.\n"
        self.assertEqual(expected_output, result_output)

    def test_do_east(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["do", "east"])
        result_output = stdout.getvalue()
        expected_output = "This action is not allowed with the east.\n"
        self.assertEqual(expected_output, result_output)

if __name__ == '__main__':
    unittest.main()
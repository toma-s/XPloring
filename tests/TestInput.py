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

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def test_use_bottle_entrance_room(self):
        self.cr.execute(["take", "bottle"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "bottle"])
        result_output = stdout.getvalue()
        expected_output = "You have consumed unlabelled bottle. -75 HP. " \
                          "Current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_bottle_arena_room(self):
        self.cr.execute(["take", "bottle"])
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "bottle"])
        result_output = stdout.getvalue()
        expected_output = "You have consumed unlabelled bottle. -75 HP. " \
                          "Current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)

    def test_attach_dragon(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attach", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attach\" is not allowed with the dragon.\n"
        self.assertEqual(expected_output, result_output)

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

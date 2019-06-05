import unittest
import contextlib
import io
import sys


from CommandRunner import CommandRunner
from GameState import GameState


class TestInput(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def testReadEnvelope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["read", "envelope"])

        result_output = stdout.getvalue()
        expected_output = "I don't understand. Try again."
        self.assertEqual(expected_output, result_output)

    def testReadLetterAgain(self):
        self.cr.execute(["open", "envelope"])
        self.cr.execute(["open", "envelope"])
        # self.cr.execute(["read", "letter"])


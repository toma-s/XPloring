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

    def testOpenEnvelopeAgain(self):
        self.cr.execute(["open", "envelope"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "You found letter. READ to read content."
        self.assertEqual(expected_output, result_output)

    def testUseMysteryAtEntranceRoom(self):
        self.cr.execute(["take", "mystery"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "mystery"])
        result_output = stdout.getvalue()
        expected_output = "You used mystery. -75 health. Current health is 25 health.\n" \
                          "Hahahahahaha you fool :P\n"
        self.assertEqual(expected_output, result_output)

    def testUseMysteryAtArenaRoom(self):
        self.cr.execute(["take", "mystery"])
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "mystery"])
        result_output = stdout.getvalue()
        expected_output = "You used mystery. -75 health. Current health is 25 health.\n" \
                          "Hahahahahaha you fool :P\n"
        self.assertEqual(expected_output, result_output)

    def testAttackDragon(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "You hit the dragon! dragon lost 1 HP.\n" \
                          "dragon had hit you! You lose 10 HP.\n"
        self.assertEqual(expected_output, result_output)

    def testAttachDragon(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attach", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "I don't understand. Try again.\n"
        self.assertEqual(expected_output, result_output)

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
        expected_output = "Action \"read\" is not allowed with \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

    def test_open_envelope_room(self):
        self.assertIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertNotIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

        self.cr.execute(["open", "envelope"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

        self.assertNotIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

    def test_open_envelope_inventory(self):
        self.assertIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertNotIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

        self.cr.execute(["take", "envelope"])
        self.cr.execute(["open", "envelope"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

        self.assertNotIn("#item_envelope", self.game_state.rooms['#room_entrance'].items)
        self.assertIn("#item_letter", self.game_state.rooms['#room_entrance'].items)

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
        expected_output = "You hit the dragon for 1 damage! dragon has 59 HP left.\n" \
                          "dragon hit you for 10 damage! You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def testAttachDragon(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attach", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attach\" is not allowed with \"dragon\".\n"
        self.assertEqual(expected_output, result_output)

    def testAttackEnvelope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "You can't attack the \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

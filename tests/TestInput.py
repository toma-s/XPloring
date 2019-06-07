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

        self.map_capital_alias = '../game_states/game_capital_alias.json'
        self.game_state_capital_alias = GameState(self.map_capital_alias)
        self.cr_capital_alias = CommandRunner(self.game_state_capital_alias)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def test_use_mystery_entrance_room(self):
        self.cr.execute(["take", "mystery"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "mystery"])
        result_output = stdout.getvalue()
        expected_output = "You used mystery. -75 health. Current health is 25 health.\n" \
                          "Hahahahahaha you fool :P\n"
        self.assertEqual(expected_output, result_output)

    def test_use_mystery_arena_room(self):
        self.cr.execute(["take", "mystery"])
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["use", "mystery"])
        result_output = stdout.getvalue()
        expected_output = "You used mystery. -75 health. Current health is 25 health.\n" \
                          "Hahahahahaha you fool :P\n"
        self.assertEqual(expected_output, result_output)


    def test_attach_dragon(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attach", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "Action \"attach\" is not allowed with \"dragon\".\n"
        self.assertEqual(expected_output, result_output)

    def test_capital_alias(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr_capital_alias.execute(["take", "Helmet"])
        result_output = stdout.getvalue()
        expected_output = "You grabbed the Helmet.\n"
        self.assertEqual(expected_output, result_output)



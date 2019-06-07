import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState


class TestConsume(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

        self.map_two_helmets = '../game_states/game_two_helmets.json'
        self.game_two_helmets = GameState(self.map_two_helmets)
        self.cr_two_helmets = CommandRunner(self.game_two_helmets)

        self.map2keys = '../game_states/game_2_locked_doors_repr.json'
        self.game_state2keys = GameState(self.map2keys)
        self.cr2keys = CommandRunner(self.game_state2keys)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

        del self.game_state2keys
        del self.cr2keys

    def test_use_mystery(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "mystery"])
            self.cr.execute(["use", "mystery"])
        result_output = stdout.getvalue()
        expected_output = "You grabbed the mystery.\n" \
                          "You used mystery. -75 health. Current health is 25 health.\n" \
                          "Hahahahahaha you fool :P\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(25, self.game_state.hero.health)

    def test_use_healing_potion(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "potion"])
            self.cr.execute(["use", "potion"])
        result_output = stdout.getvalue()
        expected_output = "You grabbed the potion.\n" \
                          "You are fully healed, you don't need healing.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(100, self.game_state.hero.health)

    def test_eat_cake(self):
        self.cr2keys.execute(["take", "kitchen key"])
        self.cr2keys.execute(["go", "north"])
        self.cr2keys.execute(["unlock", "kitchen door"])
        self.cr2keys.execute(["go", "east"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["take", "cake"])
            self.cr2keys.execute(["eat", "cake"])
        result_output = stdout.getvalue()
        expected_output = "You grabbed the cake.\n" \
                          "You used cake. -15 health. Current health is 85 health.\n" \
                          "The cake is a lie ...\n" \
                          "You found key. This key opens heavy metal door.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(100, self.game_state.hero.health)

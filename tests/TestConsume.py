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

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.cr1 = CommandRunner(self.game_state1)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

        del self.game_state1
        del self.cr1

    def test_use_mystery(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "mystery"])
            self.cr.execute(["use", "mystery"])
        result_output = stdout.getvalue()
        expected_output = "Mystery has been added to your inventory.\n" \
                          "You have consumed mystery. -75 HP. Current health is 25 HP.\n" \
                          "It was a poison\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(25, self.game_state.hero.health)

    def test_use_healing_potion(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["take", "potion"])
            self.cr.execute(["use", "potion"])
        result_output = stdout.getvalue()
        expected_output = "Potion has been added to your inventory.\n" \
                          "You are fully healed, you don't need healing.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(100, self.game_state.hero.health)

    def test_eat_cake(self):
        self.cr1.execute(["take", "kitchen key"])
        self.cr1.execute(["go", "north"])
        self.cr1.execute(["unlock", "kitchen door"])
        self.cr1.execute(["go", "east"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr1.execute(["take", "cake"])
            self.cr1.execute(["eat", "cake"])
        result_output = stdout.getvalue()
        expected_output = "Cake has been added to your inventory.\n" \
                          "You have consumed cake. -15 HP. Current health is 85 HP.\n" \
                          "The cake is a lie ...\n" \
                          "You found key. This key opens heavy metal door.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(100, self.game_state.hero.health)

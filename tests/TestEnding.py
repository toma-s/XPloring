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

        self.map2keys = '../game_states/game_2_locked_doors_repr.json'
        self.game_state2keys = GameState(self.map2keys)
        self.cr2keys = CommandRunner(self.game_state2keys)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

        del self.game_state2keys
        del self.cr2keys


    # -- Good End --

    def test_game2keys_escape_good_end(self):
        self.cr2keys.execute(["take", "kitchen key"])
        self.cr2keys.execute(["go", "north"])
        self.cr2keys.execute(["unlock", "kitchen door"])
        self.cr2keys.execute(["go", "east"])
        self.cr2keys.execute(["take", "cake"])
        self.cr2keys.execute(["eat", "cake"])
        self.cr2keys.execute(["take", "key"])
        self.cr2keys.execute(["unlock", "heavy metal door"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.cr2keys.execute(["go", "east"])
        result_output = stdout.getvalue()
        expected_output = "The End\nCongratulations Hero!\nYou are free. Do anything you want, be who you want to be.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual('0', str(e.exception))


    def test_game0_escape_good_end(self):
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        self.cr.execute(["go", "west"])
        for i in range(2):
            self.cr.execute(["attack", "dragon"])
        self.cr.execute(["take", "key"])
        self.cr.execute(["unlock", "door"])


        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.cr.execute(["go", "north"])
        result_output = stdout.getvalue()
        expected_output = "The end\nCongratulations Hero!\nYou are free. Do anything you want, be who you want to be.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual('0', str(e.exception))


    # -- Bad End --

    def test_hero_dead_bad_end(self):
        self.cr.execute(["go", "west"])
        for i in range(9):
            self.cr.execute(["attack", "dragon"])

        self.assertEqual(51, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(10, self.game_state.hero.health)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.cr.execute(["attack", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "You hit the green dragon for 1 damage! " \
                          "Green dragon has 50 HP left.\n" \
                          "Green dragon hit you for 10 damage! You have 0 HP left.\n" \
                          "GAME OVER. You were killed by green dragon. Better luck next time.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(50, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(0, self.game_state.hero.health)
        self.assertEqual('0', str(e.exception))

    def test_hero_dead_helmet_overkill_bad_end(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["go", "west"])
        for i in range(10):
            self.cr.execute(["attack", "dragon"])

        self.assertEqual(50, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(6, self.game_state.hero.health)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.cr.execute(["attack", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "You hit the green dragon for 1 damage! " \
                          "Green dragon has 49 HP left.\n" \
                          "Green dragon hit you for 10 damage! You have -4 HP left.\n" \
                          "GAME OVER. You were killed by green dragon. Better luck next time.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(49, self.game_state.creatures["#creature_dragon"].health)

        self.assertEqual(-4, self.game_state.hero.health)

        self.assertEqual('0', str(e.exception))


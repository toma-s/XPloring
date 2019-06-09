import unittest
import contextlib
import io


from InputHandler import InputHandler
from GameState import GameState


class TestInput(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.ih1 = InputHandler(self.game_state1)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

        del self.game_state1
        del self.ih1


    # -- Good End --

    def test_game1_escape_good_end(self):
        self.ih1.execute_commands(["take", "kitchen key"])
        self.ih1.execute_commands(["go", "north"])
        self.ih1.execute_commands(["unlock", "kitchen door"])
        self.ih1.execute_commands(["go", "east"])
        self.ih1.execute_commands(["take", "cake"])
        self.ih1.execute_commands(["eat", "cake"])
        self.ih1.execute_commands(["take", "key"])
        self.ih1.execute_commands(["unlock", "heavy metal door"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.ih1.execute_commands(["go", "east"])
        result_output = stdout.getvalue()
        expected_output = "The End\nCongratulations Hero!\nYou are free. Do anything you want, be who you want to be.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual('0', str(e.exception))


    def test_game0_escape_good_end(self):
        self.ih.execute_commands(["take", "sword"])
        self.ih.execute_commands(["equip", "sword"])
        self.ih.execute_commands(["go", "west"])
        for i in range(2):
            self.ih.execute_commands(["attack", "dragon"])
        self.ih.execute_commands(["take", "key"])
        self.ih.execute_commands(["unlock", "door"])


        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.ih.execute_commands(["go", "north"])
        result_output = stdout.getvalue()
        expected_output = "The end\nCongratulations Hero!\nYou are free. Do anything you want, be who you want to be.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual('0', str(e.exception))


    # -- Bad End --

    def test_hero_dead_bad_end(self):
        self.ih.execute_commands(["go", "west"])
        for i in range(9):
            self.ih.execute_commands(["attack", "dragon"])

        self.assertEqual(51, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(10, self.game_state.hero.health)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.ih.execute_commands(["attack", "dragon"])
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
        self.ih.execute_commands(["take", "helmet"])
        self.ih.execute_commands(["equip", "helmet"])
        self.ih.execute_commands(["go", "west"])
        for i in range(10):
            self.ih.execute_commands(["attack", "dragon"])

        self.assertEqual(50, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(6, self.game_state.hero.health)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.ih.execute_commands(["attack", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "You hit the green dragon for 1 damage! " \
                          "Green dragon has 49 HP left.\n" \
                          "Green dragon hit you for 10 damage! You have -4 HP left.\n" \
                          "GAME OVER. You were killed by green dragon. Better luck next time.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(49, self.game_state.creatures["#creature_dragon"].health)

        self.assertEqual(-4, self.game_state.hero.health)

        self.assertEqual('0', str(e.exception))


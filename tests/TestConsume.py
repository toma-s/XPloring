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

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def test_take_deadly_potion_mystery(self):
        self.cr.execute(["take", "mystery"])
        self.cr.execute(["use", "mystery"])
        self.assertEqual(25, self.game_state.hero.health)

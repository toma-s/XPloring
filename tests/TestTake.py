import unittest

from CommandRunner import CommandRunner
from GameState import GameState


class TestTake(unittest.TestCase):

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

    def test_take_deadly_potion_mystery(self):
        self.cr.execute(["take", "mystery"])
        self.cr.execute(["use", "mystery"])
        self.assertEqual(25, self.game_state.hero.health)
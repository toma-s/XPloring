from unittest import TestCase

from src.GameState import GameState
from src.CommandRunner import CommandRunner


class TestMoving(TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def testMoveInvalid(self):
        self.cr.execute(["go", "east"])
        self.assertEqual("#room_entrance", self.game_state.hero.location)

    def testMoveValid(self):
        self.cr.execute(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)

    def testMoveBackAndForth(self):
        self.cr.execute(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)
        self.cr.execute(["go", "east"])

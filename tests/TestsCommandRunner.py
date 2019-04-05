from unittest import TestCase

from src.GameState import GameState
from src.CommandRunner import CommandRunner


class TestCommandRunner(TestCase):

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
        self.assertEqual("#room_entrance", self.game_state.hero.location)

    def testInternalSpawnItem(self):
        self.cr.execute(["open", "envelope"])
        room_items = self.game_state.rooms[self.game_state.hero.location].items
        self.assertIn("#item_letter", room_items, "Letter should appear in room after opening an envelope")
        self.assertNotIn("#item_envelope", room_items, "After envelope was opened it should have disappeared")

    def testInternalTakeItem(self):
        self.cr.execute(["take", "sword"])
        room_items = self.game_state.rooms[self.game_state.hero.location].items
        self.assertNotIn("#equipment_steel_sword", room_items, "You took the sword, why is it in the room still???")

    def testGoThroughtLockedDoor(self):
        self.cr.execute(["go", "west"])
        self.assertEqual("#room_arena", self.game_state.hero.location)
        self.cr.execute(["go", "north"])
        self.assertEqual("#room_arena", self.game_state.hero.location)

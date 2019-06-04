import unittest

from src.GameState import GameState
from src.CommandRunner import CommandRunner


class TestItems(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

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

    def testTakeItemCheckInventory(self):
        self.cr.execute(["take", "sword"])
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.assertIn("#equipment_steel_sword", self.game_state.hero.inventory)

    def testEquipItemNotInInventory(self):
        self.cr.execute(["equip", "sword"])
        sword = [self.game_state.equipment[item] for item in self.game_state.equipment if
                 "sword" in self.game_state.equipment[item].alias]
        self.assertGreaterEqual(1, len(sword))
        self.assertFalse(sword[0].in_use)
        self.assertEqual("none", self.game_state.hero.right_hand)

    def testEquipItemInInventory(self):
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        sword = [self.game_state.equipment[item] for item in self.game_state.equipment if "sword" in self.game_state.equipment[item].alias]
        self.assertGreaterEqual(1, len(sword))
        self.assertTrue(sword[0].in_use)
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)

    def testEquipSameItemTwice(self):
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        self.cr.execute(["equip", "sword"])
        sword = [self.game_state.equipment[item] for item in self.game_state.equipment if
                 "sword" in self.game_state.equipment[item].alias]
        self.assertGreaterEqual(1, len(sword))
        self.assertTrue(sword[0].in_use)
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)

    def testTakeDeadlyPotionMystery(self):
        self.cr.execute(["take", "mystery"])
        self.cr.execute(["use", "mystery"])
        self.assertEqual(25, self.game_state.hero.health)

    def testEquipFullArmor(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)
        self.assertEqual("#equipment_golden_chestplate", self.game_state.hero.chest)
        self.assertEqual("#equipment_steel_helmet", self.game_state.hero.head)


if __name__ == '__main__':
    unittest.main()

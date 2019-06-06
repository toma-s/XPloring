import contextlib
import io
import unittest

from src.GameState import GameState
from src.CommandRunner import CommandRunner


class TestItems(unittest.TestCase):

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

    def testInternalSpawnItem(self):
        self.cr.execute(["open", "envelope"])
        room_items = self.game_state.rooms[self.game_state.hero.location].items
        self.assertIn("#item_letter", room_items, "Letter should appear in room after opening an envelope")
        self.assertNotIn("#item_envelope", room_items, "After envelope was opened it should have disappeared")


    def testInternalTakeItem(self):
        self.cr.execute(["take", "sword"])
        room_items = self.game_state.rooms[self.game_state.hero.location].items
        self.assertNotIn("#equipment_steel_sword", room_items, "You took the sword, why is it still in the room ???")

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

    def test_open_nonexisting_item(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["open", "envel"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"envel\".\n"
        self.assertEqual(expected_output, result_output)

    def test_nonexisting_action_ope(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["ope", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"Action \"ope\" is not allowed with \"envelope\".\n"
        self.assertEqual(expected_output, result_output)

    def test_both_nonexisting_ope_enveep(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["ope", "enveep"])
        result_output = stdout.getvalue()
        expected_output = "There is no such thing as \"enveep\".\n"
        self.assertEqual(expected_output, result_output)

    def test_nonexisting_action_read(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["read", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"Action \"read\" is not allowed with \"envelope\".\n"
        self.assertEqual(expected_output, result_output)


    def test_take_keys_with_same_alias(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["take", "key"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"key\"-s. You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_keys_with_same_alias(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["examine", "key"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"key\"-s. You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_nonexistent_action_keys_with_same_alias(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["read", "key"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"key\"-s. You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_open_doors_with_same_alias(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["open", "door"])
        result_output = stdout.getvalue()
        expected_output = f"There are 2 \"door\"-s. You have to be more specific.\n"
        self.assertEqual(expected_output, result_output)

    def test_examine_armory_door(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["examine", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Door to armory is locked, you need a key\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_armory_door_nokey(self):
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["unlock", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"You do not have a required item to do this action.\n"
        self.assertEqual(expected_output, result_output)

    def test_unlock_armory_door_has_key(self):
        self.cr2keys.execute(["take", "armory key"])
        self.cr2keys.execute(["go", "north"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["unlock", "armory door"])
        result_output = stdout.getvalue()
        expected_output = f"Unlocked, you may enter the armory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_envelope_room(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["equip", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"You don't have envelope in your inventory.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_envelope_inv(self):
        self.cr2keys.execute(["take", "envelope"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr2keys.execute(["equip", "envelope"])
        result_output = stdout.getvalue()
        expected_output = f"You don't have envelope in your inventory.\n"
        self.assertEqual(expected_output, result_output)


    def test_equip_already_equipped(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "helmet"])
            self.cr.execute(["equip", "chestplate"])
            self.cr.execute(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = f"You are already equipped with helmet\nYou are already equipped with chestplate\nYou are already equipped with sword\n"
        self.assertEqual(expected_output, result_output)


if __name__ == '__main__':
    unittest.main()

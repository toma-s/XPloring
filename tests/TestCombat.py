import unittest
import contextlib
import io

from src.GameState import GameState
from src.CommandHandler import CommandHandler


class TestCombat(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def test_attack_dragon(self):
        self.cr.execute(["go", "west"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["attack", "dragon"])
        result_output = stdout.getvalue()
        expected_output = "You hit the green dragon for 1 damage! Green dragon has 59 HP left.\n" \
                          "Green dragon hit you for 10 damage! You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def testHitCreatureWithFist(self):
        self.cr.execute(["go", "west"])
        self.assertEqual(60, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(100, self.game_state.hero.health)
        self.cr.execute(["attack", "dragon"])
        self.assertEqual(59, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)

    def testHitCreatureWithFistThanWithSword(self):
        self.cr.execute(["take", "sword"])
        self.cr.execute(["go", "west"])
        self.assertEqual(60, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(100, self.game_state.hero.health)
        self.cr.execute(["attack", "dragon"])
        self.assertEqual(59, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)
        self.cr.execute(["equip", "sword"])
        self.cr.execute(["attack", "dragon"])
        self.assertEqual(29, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(80, self.game_state.hero.health)

    def testKillDragon(self):
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        self.cr.execute(["go", "west"])
        self.assertEqual(60, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(100, self.game_state.hero.health)
        self.cr.execute(["attack", "dragon"])
        self.assertEqual(30, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)
        self.cr.execute(["attack", "dragon"])
        self.assertEqual(0, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)

    def testGetKey(self):
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        self.cr.execute(["go", "west"])
        self.assertEqual(60, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(100, self.game_state.hero.health)
        self.cr.execute(["attack", "dragon"])
        self.assertEqual(30, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)
        self.cr.execute(["attack", "dragon"])
        self.assertEqual(0, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)
        self.assertIn("#item_doorkey_exit", self.game_state.rooms[self.game_state.hero.location].items)

    def testKillCreatureHelmetDurability(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["go", "west"])
        for i in range(3):
            self.cr.execute(["attack", "dragon"])
        self.assertTrue(self.game_state.equipment["#equipment_steel_helmet"].durability <= 0)

    def testKillCreatureChestplateDurability(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["go", "west"])
        for i in range(4):
            self.cr.execute(["attack", "dragon"])
        self.assertTrue(self.game_state.equipment["#equipment_golden_chestplate"].durability <= 0)

    def testFullArmorCreatureKillGetKey(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)
        self.assertEqual("#equipment_golden_chestplate", self.game_state.hero.chest)
        self.assertEqual("#equipment_steel_helmet", self.game_state.hero.head)
        self.cr.execute(["go", "west"])
        for i in range(2):
            self.cr.execute(["attack", "dragon"])
        self.assertEqual(0, self.game_state.creatures["#creature_dragon"].health)
        self.cr.execute(["look"])
        self.cr.execute(["take", "key"])
        self.assertIn("#item_doorkey_exit", self.game_state.hero.inventory)

    def testFullArmorCreatureKillGetKeyOpenDoor(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)
        self.assertEqual("#equipment_golden_chestplate", self.game_state.hero.chest)
        self.assertEqual("#equipment_steel_helmet", self.game_state.hero.head)
        self.cr.execute(["go", "west"])
        for i in range(2):
            self.cr.execute(["attack", "dragon"])
        self.assertEqual(0, self.game_state.creatures["#creature_dragon"].health)
        self.cr.execute(["look"])
        self.cr.execute(["take", "key"])
        self.assertIn("#item_doorkey_exit", self.game_state.hero.inventory)
        self.cr.execute(["unlock", "door"])
        self.assertEqual("#room_arena", self.game_state.hero.location)

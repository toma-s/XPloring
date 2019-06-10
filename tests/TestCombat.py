import unittest
import contextlib
import io

from src.GameState import GameState
from src.InputHandler import InputHandler


class TestCombat(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

    def test_attack_dragon(self):
        self.ih.handle_user_input("go west")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("attack dragon")
        result_output = stdout.getvalue()
        expected_output = "You hit the green dragon for 1 damage! Green dragon has 59 HP left.\n" \
                          "Green dragon hit you for 10 damage! You have 90 HP left.\n"
        self.assertEqual(expected_output, result_output)

    def testHitCreatureWithFist(self):
        self.ih.handle_user_input("go west")
        self.assertEqual(60, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(100, self.game_state.hero.health)
        self.ih.handle_user_input("attack dragon")
        self.assertEqual(59, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)

    def testHitCreatureWithFistThanWithSword(self):
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("go west")
        self.assertEqual(60, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(100, self.game_state.hero.health)
        self.ih.handle_user_input("attack dragon")
        self.assertEqual(59, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)
        self.ih.handle_user_input("equip sword")
        self.ih.handle_user_input("attack dragon")
        self.assertEqual(29, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(80, self.game_state.hero.health)

    def testKillDragon(self):
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")
        self.ih.handle_user_input("go west")
        self.assertEqual(60, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(100, self.game_state.hero.health)
        self.ih.handle_user_input("attack dragon")
        self.assertEqual(30, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)
        self.ih.handle_user_input("attack dragon")
        self.assertEqual(0, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)

    def testGetKey(self):
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")
        self.ih.handle_user_input("go west")
        self.assertEqual(60, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(100, self.game_state.hero.health)
        self.ih.handle_user_input("attack dragon")
        self.assertEqual(30, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)
        self.ih.handle_user_input("attack dragon")
        self.assertEqual(0, self.game_state.creatures["#creature_dragon"].health)
        self.assertEqual(90, self.game_state.hero.health)
        self.assertIn("#item_doorkey_exit", self.game_state.rooms[self.game_state.hero.location].items)

    def testKillCreatureHelmetDurability(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("go west")
        for i in range(3):
            self.ih.handle_user_input("attack dragon")
        self.assertTrue(self.game_state.equipment["#equipment_gladiator_helmet"].durability <= 0)

    def testKillCreatureChestplateDurability(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("go west")
        for i in range(4):
            self.ih.handle_user_input("attack dragon")
        self.assertTrue(self.game_state.equipment["#equipment_steel_chestplate"].durability <= 0)

    def testFullArmorCreatureKillGetKey(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")
        self.assertEqual("#equipment_silver_sword", self.game_state.hero.weapon_slot)
        self.assertEqual("#equipment_steel_chestplate", self.game_state.hero.chest_slot)
        self.assertEqual("#equipment_gladiator_helmet", self.game_state.hero.head_slot)
        self.ih.handle_user_input("go west")
        for i in range(2):
            self.ih.handle_user_input("attack dragon")
        self.assertEqual(0, self.game_state.creatures["#creature_dragon"].health)
        self.ih.handle_user_input("take key")
        self.assertIn("#item_doorkey_exit", self.game_state.hero.inventory)

    def testFullArmorCreatureKillGetKeyOpenDoor(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")
        self.assertEqual("#equipment_silver_sword", self.game_state.hero.weapon_slot)
        self.assertEqual("#equipment_steel_chestplate", self.game_state.hero.chest_slot)
        self.assertEqual("#equipment_gladiator_helmet", self.game_state.hero.head_slot)
        self.ih.handle_user_input("go west")
        for i in range(2):
            self.ih.handle_user_input("attack dragon")
        self.assertEqual(0, self.game_state.creatures["#creature_dragon"].health)
        self.ih.handle_user_input("take key")
        self.assertIn("#item_doorkey_exit", self.game_state.hero.inventory)
        self.ih.handle_user_input("unlock door")
        self.assertEqual("#room_arena", self.game_state.hero.location)

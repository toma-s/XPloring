import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestInventory(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

    def test_durability_helmet(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        helmet_id = self.game_state.hero.head_slot
        result_durability = self.game_state.equipment[helmet_id].durability
        self.assertEqual(12, result_durability)
        self.assertEqual("#equipment_gladiator_helmet", helmet_id)
        self.assertEqual(1, len(self.game_state.hero.inventory))

    def test_durability_helmet_hit(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("hit dragon")
        helmet_id = self.game_state.hero.head_slot
        result_durability = self.game_state.equipment[helmet_id].durability
        self.assertEqual(7, result_durability)
        self.assertEqual("#equipment_gladiator_helmet", helmet_id)
        self.assertEqual(1, len(self.game_state.hero.inventory))

    def test_durability_helmet_broken(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("hit dragon")
        self.ih.handle_user_input("hit dragon")
        self.ih.handle_user_input("hit dragon")
        helmet_id = self.game_state.hero.head_slot
        self.assertEqual(None, helmet_id)
        self.assertEqual(0, len(self.game_state.hero.inventory))

    def test_durability_helmet_chestplate(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip chestplate")
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("hit dragon")
        self.ih.handle_user_input("hit dragon")
        self.ih.handle_user_input("status")
        helmet_id = self.game_state.hero.head_slot
        chestplate_id = self.game_state.hero.chest_slot
        self.assertEqual("#equipment_gladiator_helmet", helmet_id)
        self.assertEqual("#equipment_steel_chestplate", chestplate_id)
        self.assertEqual(2, len(self.game_state.hero.inventory))

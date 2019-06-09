import contextlib
import io
import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestInventory(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.ih1 = InputHandler(self.game_state1)

        self.map_capital_alias = '../game_states/game_capital_alias.json'
        self.game_state_capital_alias = GameState(self.map_capital_alias)
        self.ih_capital_alias = InputHandler(self.game_state_capital_alias)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

        del self.game_state1
        del self.ih1

        del self.game_state_capital_alias
        del self.ih_capital_alias

    def test_durability_helmet(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        helmet_id = self.game_state.hero.head
        result_durability = self.game_state.equipment[helmet_id].durability
        self.assertEqual(12, result_durability)

    def test_durability_helmet_hit(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("hit dragon")
        helmet_id = self.game_state.hero.head
        result_durability = self.game_state.equipment[helmet_id].durability
        self.assertEqual(7, result_durability)

    def test_durability_helmet_end(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("hit dragon")
        self.ih.handle_user_input("hit dragon")
        self.ih.handle_user_input("hit dragon")
        helmet_id = self.game_state.hero.head
        self.assertEqual(None, helmet_id)

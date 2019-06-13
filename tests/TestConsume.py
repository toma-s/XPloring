import contextlib
import io
import unittest

from InputHandler import InputHandler
from GameState import GameState
from game_items.Room import Room


class TestConsume(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map1 = '../game_states/game1_cake.json'
        self.game_state1 = GameState(self.map1)
        self.ih1 = InputHandler(self.game_state1)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

        del self.game_state1
        del self.ih1

    def test_use_bottle_entrance_room(self):
        self.ih.handle_user_input("take bottle")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use bottle")
        result_output = stdout.getvalue()
        expected_output = "The unlabelled bottle reduced your HP by 75. Your current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_bottle_arena_room(self):
        self.ih.handle_user_input("take bottle")
        self.ih.handle_user_input("go west")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use bottle")
        result_output = stdout.getvalue()
        expected_output = "The unlabelled bottle reduced your HP by 75. Your current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)

    def test_drink_bottle_entrance_room(self):
        self.ih.handle_user_input("take bottle")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drink bottle")
        result_output = stdout.getvalue()
        expected_output = "The unlabelled bottle reduced your HP by 75. Your current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)

    def test_drink_bottle_arena_room(self):
        self.ih.handle_user_input("take bottle")
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drink bottle")
        result_output = stdout.getvalue()
        expected_output = "The unlabelled bottle reduced your HP by 75. Your current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(25, self.game_state.hero.health)

    def test_use_bandage_full_hp(self):
        self.ih.handle_user_input("take bandage")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.assertEqual(100, self.game_state.hero.health)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use bandage")
        result_output = stdout.getvalue()
        expected_output = "Your health is already at 100 HP, you don't need healing.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.assertEqual(100, self.game_state.hero.health)

    def test_use_bandage_after_poison(self):
        self.ih.handle_user_input("take bottle")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        self.ih.handle_user_input("drink unlabelled bottle")
        self.assertEqual(0, len(self.game_state.hero.inventory))
        self.assertEqual(25, self.game_state.hero.health)

        self.ih.handle_user_input("take bandage")
        self.assertEqual(1, len(self.game_state.hero.inventory))
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use bandage")
        result_output = stdout.getvalue()
        expected_output = "The bandage healed you by 25 HP. Your current health is 50 HP.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(50, self.game_state.hero.health)
        self.assertEqual(0, len(self.game_state.hero.inventory))

    def test_eat_cake(self):
        self.ih1.handle_user_input("take kitchen key")
        self.ih1.handle_user_input("go north")
        self.ih1.handle_user_input("unlock kitchen door")
        self.ih1.handle_user_input("go east")
        self.ih1.handle_user_input("take cake")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("eat cake")
        result_output = stdout.getvalue()
        expected_output = "The cake reduced your HP by 15. Your current health is 85 HP.\n" \
                          "You found key. This key opens heavy metal door.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(85, self.game_state1.hero.health)
        hero_room: Room = self.game_state1.rooms[self.game_state1.hero.location]
        self.assertIn("#item_doorkey_exit", hero_room.items)

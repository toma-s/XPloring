import contextlib
import io
import unittest

from InputHandler import InputHandler
from GameState import GameState
from game_item.Room import Room


class TestConsume(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

        self.map_two_helmets = '../game_states/game_two_helmets.json'
        self.game_two_helmets = GameState(self.map_two_helmets)
        self.ih_two_helmets = InputHandler(self.game_two_helmets)

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
        expected_output = "You have consumed unlabelled bottle. -75 HP. " \
                          "Current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)

    def test_use_bottle_arena_room(self):
        self.ih.handle_user_input("take bottle")
        self.ih.handle_user_input("go west")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("use bottle")
        result_output = stdout.getvalue()
        expected_output = "You have consumed unlabelled bottle. -75 HP. " \
                          "Current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)

    def test_drink_bottle_entrance_room(self):
        self.ih.handle_user_input("take bottle")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drink bottle")
        result_output = stdout.getvalue()
        expected_output = "You have consumed unlabelled bottle. -75 HP. " \
                          "Current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)

    def test_drink_bottle_arena_room(self):
        self.ih.handle_user_input("take bottle")
        self.ih.handle_user_input("go west")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("drink bottle")
        result_output = stdout.getvalue()
        expected_output = "You have consumed unlabelled bottle. -75 HP. " \
                          "Current health is 25 HP.\n" \
                          "It was a poison.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(25, self.game_state.hero.health)

    def test_use_bandage(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("take bandage")
            self.ih.handle_user_input("use bandage")
        result_output = stdout.getvalue()
        expected_output = "Bandage has been added to your inventory.\n" \
                          "You are fully healed, you don't need healing.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(100, self.game_state.hero.health)

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
        expected_output = "You have consumed cake. -15 HP. Current health is 85 HP.\n" \
                          "You found key. This key opens heavy metal door.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual(85, self.game_state1.hero.health)
        hero_room: Room = self.game_state1.rooms[self.game_state1.hero.location]
        self.assertIn("#item_doorkey_exit", hero_room.items)

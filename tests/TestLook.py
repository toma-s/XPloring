import contextlib
import io
import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestLook(unittest.TestCase):

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

    def test_look_whatever(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("look whatever")
        result_output = stdout.getvalue()
        expected_output = "There is no whatever around.\n"
        self.assertEqual(expected_output, result_output)

    def test_look_entrance(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("look")
        result_output = stdout.getvalue()
        expected_output = "- Entrance room -\nYour journey to freedom begins here.\n\n" \
                          "There is a key. This key opens armory door.\n" \
                          "There is a key. This key opens kitchen door.\n" \
                          "There are no enemies around.\n" \
                          "The crossroad room is to the NORTH.\n"
        self.assertEqual(expected_output, result_output)

    def test_look_crossroad(self):
        self.ih1.handle_user_input("go north")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih1.handle_user_input("look")
        result_output = stdout.getvalue()
        expected_output = "- Crossroad room -\nA room with 3 doors.\n\n" \
                          "There are no enemies around.\n" \
                          "There is a armory door to the WEST.\n" \
                          "There is a kitchen door to the EAST.\n" \
                          "The entrance room is to the SOUTH.\n"
        self.assertEqual(expected_output, result_output)

    def test_look_game0_entrance(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("look")
        result_output = stdout.getvalue()
        expected_output = "- Entrance room -\nThere are some things just laying around in the room.\n\n" \
                          "There is a envelope. OPEN to get letter from inside.\n" \
                          "There is a sword. Sword made of pure silver with a straight double-edged blade " \
                          "and a grip for two-handed use.\n" \
                          "There is a bandage. You can USE bandage to reduce swelling or slow heavy bleeding.\n" \
                          "There is a helmet. Gladiator helmet made of steel.\n" \
                          "There is a unlabelled bottle. Small unlabelled bottle with strange liquid inside. " \
                          "USE may lead to bad consequences.\n" \
                          "There is a chestplate. Steel chestplate armor.\n" \
                          "There are no enemies around.\n" \
                          "The arena is to the WEST.\n"
        self.assertEqual(expected_output, result_output)

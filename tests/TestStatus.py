import contextlib
import io
import unittest

from GameState import GameState
from InputHandler import InputHandler


class TestStatus(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

    def test_status(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("status")
        result_output = stdout.getvalue()
        expected_output = "----- HERO STATUS -----\n" \
                          "Health: 100 HP\n" \
                          "Attack Power: 1 ATK\n" \
                          "Weapon: nothing\n" \
                          "Head: nothing\n" \
                          "Chest: nothing\n" \
                          "Legs: nothing\n" \
                          "-----------------------\n"
        self.assertEqual(expected_output, result_output)

    def test_status_health(self):
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("attack dragon")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("status")
        result_output = stdout.getvalue()
        expected_output = "----- HERO STATUS -----\n" \
                          "Health: 90 HP\n" \
                          "Attack Power: 1 ATK\n" \
                          "Weapon: nothing\n" \
                          "Head: nothing\n" \
                          "Chest: nothing\n" \
                          "Legs: nothing\n" \
                          "-----------------------\n"
        self.assertEqual(expected_output, result_output)

    def test_status_weapon_slot(self):
        self.ih.handle_user_input("take sword")
        self.ih.handle_user_input("equip sword")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("status")
        result_output = stdout.getvalue()
        expected_output = "----- HERO STATUS -----\n" \
                          "Health: 100 HP\n" \
                          "Attack Power: 30 ATK\n" \
                          "Weapon: Sword made of pure silver with a straight " \
                          "double-edged blade and a grip for two-handed use 30 ATK\n" \
                          "Head: nothing\n" \
                          "Chest: nothing\n" \
                          "Legs: nothing\n" \
                          "-----------------------\n"
        self.assertEqual(expected_output, result_output)

    def test_status_head_slot(self):
        self.ih.handle_user_input("take helmet")
        self.ih.handle_user_input("equip helmet")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("status")
        result_output = stdout.getvalue()
        expected_output = "----- HERO STATUS -----\n" \
                          "Health: 100 HP\n" \
                          "Attack Power: 1 ATK\n" \
                          "Weapon: nothing\n" \
                          "Head: Gladiator helmet made of steel 2 DEF 12 Durability\n" \
                          "Chest: nothing\n" \
                          "Legs: nothing\n" \
                          "-----------------------\n"
        self.assertEqual(expected_output, result_output)

    def test_status_chest(self):
        self.ih.handle_user_input("take chestplate")
        self.ih.handle_user_input("equip chestplate")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.ih.handle_user_input("status")
        result_output = stdout.getvalue()
        expected_output = "----- HERO STATUS -----\n" \
                          "Health: 100 HP\n" \
                          "Attack Power: 1 ATK\n" \
                          "Weapon: nothing\n" \
                          "Head: nothing\n" \
                          "Chest: Steel chestplate armor 3 DEF 18 Durability\n" \
                          "Legs: nothing\n" \
                          "-----------------------\n"
        self.assertEqual(expected_output, result_output)

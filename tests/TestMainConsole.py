import unittest
import contextlib
import io

import MainConsole


class TestInput(unittest.TestCase):

    def test_get_config_files(self):
        expected_value = [
            'game0_repr.json',
            'game_2_locked_doors_repr.json',
            'game_test_loader.json',
            'game_wrong_creatures.json',
            'game_wrong_equipment.json',
            'game_wrong_format.txt',
            'game_wrong_hero.json',
            'game_wrong_items.json',
            'game_wrong_rooms.json'
        ]
        result_value = MainConsole.get_config_files()
        self.assertListEqual(expected_value, result_value)

    def test_valid_choice_1(self):
        expected_value = True
        result_value = MainConsole.valid_choice("1", 1)
        self.assertEqual(expected_value, result_value)

    def test_valid_choice_one(self):
        expected_value = False
        expected_output = "Not a number\n\n"

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            result_value = MainConsole.valid_choice("one", 1)
        result_output = stdout.getvalue()

        self.assertEqual(expected_output, result_output)
        self.assertEqual(expected_value, result_value)

    def test_valid_choice_0(self):
        expected_value = False
        expected_output = "Number out of range\n\n"

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            result_value = MainConsole.valid_choice("0", 1)
        result_output = stdout.getvalue()

        self.assertEqual(expected_output, result_output)
        self.assertEqual(expected_value, result_value)

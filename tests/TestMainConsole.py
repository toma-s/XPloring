import unittest
import contextlib
import io

import MainConsole


class TestInput(unittest.TestCase):

    def test_valid_choice_1(self):
        expected_value = True
        result_value = MainConsole._valid_choice("1", 1)
        self.assertEqual(expected_value, result_value)

    def test_valid_choice_one(self):
        expected_value = False
        expected_output = "Not a number\n\n"

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            result_value = MainConsole._valid_choice("one", 1)
        result_output = stdout.getvalue()

        self.assertEqual(expected_output, result_output)
        self.assertEqual(expected_value, result_value)

    def test_valid_choice_0(self):
        expected_value = False
        expected_output = "Number out of range\n\n"

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            result_value = MainConsole._valid_choice("0", 1)
        result_output = stdout.getvalue()

        self.assertEqual(expected_output, result_output)
        self.assertEqual(expected_value, result_value)

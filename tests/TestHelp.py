import contextlib
import io
import unittest

from Game import Game


class TestHelp(unittest.TestCase):

    def test_help(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            Game.print_help()
        result_output = stdout.getvalue()
        expected_output = "Basic commands:\n" \
                          "Type LOOK for more information about the environment.\n" \
                          "Type INVENTORY to check out the collected items.\n" \
                          "Type TAKE <item> to add an item to the inventory.\n" \
                          "Type DROP <item> to remove item from the inventory.\n" \
                          "Type EQUIP <item> to arm yourself an item from the inventory.\n" \
                          "Type UNEQUIP <item> to disarm yourself an item from the inventory.\n" \
                          "Type STATUS to show your HP, Attack Power and equipment.\n" \
                          "Type EXAMINE <target> to learn more about an item.\n" \
                          "Type SAVE to save current game.\n" \
                          "Type QUIT or Q to quit game.\n"
        self.assertEqual(expected_output, result_output)

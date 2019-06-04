import unittest

from src.InputHandler import InputHandler


class TestInputHandler(unittest.TestCase):
    def testSynnonym(self):
        ih = InputHandler()
        self.assertEqual(["go"], ih.parse_user_input("run"))

    def testUnknownWord(self):
        ih = InputHandler()
        self.assertEqual(["runy"], ih.parse_user_input("runy"))

    def testMoreWordsWithSynnonym(self):
        ih = InputHandler()
        self.assertEqual(["go", "north"], ih.parse_user_input("move north"))


if __name__ == '__main__':
    unittest.main()
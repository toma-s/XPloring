from src.Game import Game
from src.GameState import GameState


from tests.TestsCommandRunner import TestCommandRunner

from tests.TestsInputHandler import TestInputHandler

import unittest

if __name__ == '__main__':
    testLoader = unittest.TestLoader()

    testtest = testLoader.loadTestsFromTestCase(TestCommandRunner)
    test_input_handler = testLoader.loadTestsFromTestCase(TestInputHandler)

    testy = unittest.TestSuite(
        [
            test_input_handler,
            testtest
        ]
    )
    unittest.TextTestRunner(verbosity=2).run(testy)

    map0 = '../game_states/game0_repr.json'
    game_state = GameState(map0)
    game = Game(game_state)
    game.run()

from src.Game import Game
from src.GameState import GameState

from tests.TestsInputHandler import TestInputHandler
from tests.TestCombat import TestCombat
from tests.TestItems import TestItems
from tests.TestMoving import TestMoving

import unittest

if __name__ == '__main__':
    testLoader = unittest.TestLoader()

    test_input_handler = testLoader.loadTestsFromTestCase(TestInputHandler)
    test_moving = testLoader.loadTestsFromTestCase(TestMoving)
    test_combat = testLoader.loadTestsFromTestCase(TestCombat)
    test_items = testLoader.loadTestsFromTestCase(TestItems)

    testy = unittest.TestSuite(
        [
            test_input_handler,
            test_moving,
            test_combat,
            test_items
        ]
    )
    # unittest.TextTestRunner(verbosity=2).run(testy)


    map0 = '../game_states/game0_repr.json'
    game_state = GameState(map0)
    game = Game(game_state)
    game.run()
    game.GUI.window.mainloop()


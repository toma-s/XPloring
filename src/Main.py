from src.Game import Game
from src.GameState import GameState

from tests.TestsInputHandler import TestInputHandler
from tests.TestCombat import TestCombat
from tests.TestItems import TestItems
from tests.TestMoving import TestMoving

import unittest

if __name__ == '__main__':

    map0 = '../game_states/game0_repr.json'
    game_state = GameState(map0)
    game = Game(game_state)
    game.run()
    game.GUI.window.mainloop()


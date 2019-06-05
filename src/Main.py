import sys

from src.Game import Game
from src.GameState import GameState


def init_game():
    config_path = sys.argv[0]
    game_state = GameState(config_path)
    return Game(game_state)


def run_by_environment(game):
    environment = sys.argv[1]
    if environment == "console":
        game.run_console()
    elif environment == "gui":
        game.run_gui()
        game.GUI.window.mainloop()


if __name__ == '__main__':
    inited_game = init_game()
    run_by_environment(inited_game)


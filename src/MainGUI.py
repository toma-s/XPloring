from src.Game import Game
from src.GameState import GameState


def _init_game():
    config_path = '../game_states/game0_repr.json'
    game_state = GameState(config_path)
    return Game(game_state)


def _run_by_environment(game):
    game.run_gui()
    game.GUI.window.mainloop()


if __name__ == '__main__':
    inited_game = _init_game()
    _run_by_environment(inited_game)

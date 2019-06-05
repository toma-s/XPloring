from src.Game import Game
from src.GameState import GameState


def init_game():
    config_path = '../game_states/game0_repr.json'
    game_state = GameState(config_path)
    return Game(game_state)


def run_by_environment(game):
    game.run_console()


if __name__ == '__main__':
    inited_game = init_game()
    run_by_environment(inited_game)

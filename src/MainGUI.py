from os import listdir
from os.path import isfile, join

from src.Game import Game
from src.GameState import GameState
from src.GUI import GamePickerGUI

parent_path = '..\\game_states'


def init_game(game_path):
    game_state = GameState(game_path)
    return Game(game_state)


def _run_by_environment(game):
    game.run_gui()
    game.GUI.window.mainloop()


def _get_config_files():
    files = []
    for file in listdir(parent_path):
        if isfile(join(parent_path, file)):
            files.append(file)
    return files


if __name__ == '__main__':
    config_files = _get_config_files()
    conf_arr = []
    for idx, element in enumerate(config_files):
        conf_arr.append(f"{element}")
    g = GamePickerGUI(conf_arr)
    g.window.mainloop()
    game_config = g.retun_val
    if (game_config is not None):
        inited_game = init_game(join(parent_path, game_config))
        _run_by_environment(inited_game)

import MainUtils
from GameGUI import GameGUI
from src.GameState import GameState
from src.GUI import GamePickerGUI


def _get_options():
    config_files = MainUtils.get_config_files()
    array = []
    for idx, element in enumerate(config_files):
        array.append(f"{element}")
    return array


def init_game(game_path):
    game_state = GameState(game_path)
    return GameGUI(game_state)


def _run_by_environment(game):
    game.run_gui()
    game.GUI.window.mainloop()


if __name__ == '__main__':
    options = _get_options()
    g = GamePickerGUI(options)
    g.window.mainloop()
    game_state_file = g.retun_val
    inited_game = init_game(MainUtils.get_game_state_path(game_state_file))
    _run_by_environment(inited_game)

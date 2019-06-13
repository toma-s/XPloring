from os import listdir
from os.path import isfile, join

parent_path = '..\\game_states'


def get_config_files():
    files = []
    for file in listdir(parent_path):
        if isfile(join(parent_path, file)):
            files.append(file)
    return files


def get_game_state_path(game_state):
    return join(parent_path, game_state)

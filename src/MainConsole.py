from os import listdir
from os.path import isfile, join

from src.Game import Game
from src.GameState import GameState


def get_config_files():
    parent_path = '../game_states'
    files = []
    for file in listdir(parent_path):
        file_path = join(parent_path, file)
        if isfile(file_path):
            files.append(file_path)
    return files


def let_user_pick(options, item_name):
    while True:
        print("Please choose %s:" % item_name)
        for idx, element in enumerate(options):
            print("{}) {}".format(idx + 1, element))
        i = input("Enter number: ")
        if 0 < int(i) <= len(options):
            return options[int(i) - 1]
        print("Number out of range\n")


if __name__ == '__main__':
    config_files = get_config_files()
    game_config = let_user_pick(config_files, "the game")
    game_state = GameState(game_config)
    game = Game(game_state)
    game.run_console()

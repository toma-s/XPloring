from os import listdir
from os.path import isfile, join

from src.Game import Game
from src.GameState import GameState


parent_path = '../game_states'


def get_config_files():
    files = []
    for file in listdir(parent_path):
        if isfile(join(parent_path, file)):
            files.append(file)
    return files


def let_user_pick(options, item_name):
    while True:
        print("Please choose %s:" % item_name)
        for idx, element in enumerate(options):
            print("{}) {}".format(idx + 1, element))
        i = input("Enter number: ")
        if not i.isdigit():
            print("Not a number\n")
            continue
        if 0 >= int(i) or int(i) > len(options):
            print("Number out of range\n")
            continue
        return options[int(i) - 1]



if __name__ == '__main__':
    config_files = get_config_files()
    game_config = let_user_pick(config_files, "the game")
    game_state = GameState(join(parent_path, game_config))
    game = Game(game_state)
    game.run_console()

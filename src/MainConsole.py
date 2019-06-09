from os import listdir
from os.path import isfile, join

from exceptions.GameStateFileException import GameStateFileException
from src.Game import Game
from src.GameState import GameState


parent_path = '..\\game_states'


def run():
    try:
        config_files = _get_config_files()
        game_config = let_user_pick(config_files, "the game")
        game_state = GameState(join(parent_path, game_config))
        game = Game(game_state)
        game.run_console()
    except GameStateFileException as e:
        print(f"Failed to read game configuration file: {e}")


def _get_config_files():
    files = []
    for file in listdir(parent_path):
        if isfile(join(parent_path, file)):
            files.append(file)
    return files


def let_user_pick(options, item_name):
    while True:
        print(f"Please choose {item_name}:")
        for idx, element in enumerate(options):
            print(f"{idx + 1}) {element}")
        chosen_i = input("Enter number: ")
        if not valid_choice(chosen_i, len(options)):
            continue
        return options[int(chosen_i) - 1]


def valid_choice(choice, max_limit):
    if not choice.isdigit():
        print("Not a number\n")
        return False
    if int(choice) <= 0 or int(choice) > max_limit:
        print("Number out of range\n")
        return False
    return True


if __name__ == '__main__':
    run()

import MainUtils
from GameConsole import GameConsole
from exceptions.GameStateFileException import GameStateFileException
from src.GameState import GameState


def run():
    try:
        config_files = MainUtils.get_config_files()
        game_state_file = _select(config_files, "the game")
        game_state = GameState(MainUtils.get_game_state_path(game_state_file))
        game = GameConsole(game_state)
        game.run_console()
    except GameStateFileException as e:
        print(f"Failed to read game configuration file: {e}")


def _select(options, item_name):
    while True:
        print(f"Please choose {item_name}:")
        for idx, element in enumerate(options):
            print(f"{idx + 1}) {element}")
        chosen_i = input("Enter number: ")
        if not _valid_choice(chosen_i, len(options)):
            continue
        return options[int(chosen_i) - 1]


def _valid_choice(choice, max_limit):
    if not choice.isdigit():
        print("Not a number\n")
        return False
    if int(choice) <= 0 or int(choice) > max_limit:
        print("Number out of range\n")
        return False
    return True


if __name__ == '__main__':
    run()

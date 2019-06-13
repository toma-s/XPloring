import re

from Game import Game
from GameState import GameState
from GameStateSaver import GameStateSaver


class GameConsole(Game):

    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run_console(self):
        self._on_load_introduction_print()

        while True:
            print(">>> ", end="")
            user_input = input()

            if re.match("^help$|^HELP$", user_input):
                self._print_help()
                continue

            if re.match("^save|^SAVE$", user_input):
                self._print_saving()
                GameStateSaver(self.game_state).save()
                self._print_saved()
                continue

            if re.match("^q$|^Q$|^quit$|^QUIT$", user_input):
                return

            self.input_handler.handle_user_input(user_input)

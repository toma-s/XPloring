import io
import re
import sys
from contextlib import redirect_stdout

from GUI import GUI
from Game import Game
from GameState import GameState
from GameStateSaver import GameStateSaver


class GameGUI(Game):

    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.GUI = GUI(self)

    def run_gui(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self._on_load_introduction_print()
            output = buffer.getvalue()
            self.GUI.set_output(output)

    def react_to_input(self, user_input):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            if re.match("^help$|^HELP$", user_input):
                self._print_help()

            elif re.match("^save$|^SAVE$", user_input):
                self._print_saving()
                GameStateSaver(self.game_state).save()
                self._print_saved()

            elif re.match("^q$|^Q$|^quit$|^QUIT$", user_input):
                sys.exit(0)

            else:
                self.input_handler.handle_user_input(user_input)

            output = buffer.getvalue()
            self.GUI.set_output(output)

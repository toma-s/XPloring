from src.GameState import GameState
from src.InputHandler import InputHandler
from src.CommandRunner import CommandRunner
from src.GUI import GUI
import re
import sys

import io
from contextlib import redirect_stdout

class Game:

    navigation = ["Type LOOK for more information about the environment.",
                  "Type QUIT or Q to quit game.",
                  "Press Enter to commit input."] # ...

    def __init__(self, map: GameState):
        self.GUI = GUI(self)
        self.game_state = map
        self.input_handler = InputHandler()
        self.command_runner = CommandRunner(self.game_state)

    def run(self):
        # mainloop
        room = self.game_state.rooms[self.game_state.hero.location]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print("Welcome, warrior!")
            print(f"You entered the {room.description.lower()}")
            print("What is your next step?")
            print('\n' + '\n'.join(self.navigation))

            print(">>> ")

            output = buffer.getvalue()
            self.GUI.setOutput(output)

    def react_to_input(self, user_input):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            if re.match("q|Q|quit|QUIT", user_input):
                sys.exit(0)

            commands_to_run = self.input_handler.parse_user_input(user_input)
            self.command_runner.execute(commands_to_run)

            output = buffer.getvalue()
            self.GUI.setOutput(output)
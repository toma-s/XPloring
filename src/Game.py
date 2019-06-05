from src.GameState import GameState
from src.InputHandler import InputHandler
from src.CommandRunner import CommandRunner
from src.GUI import GUI
import re
import sys


import io
from contextlib import redirect_stdout


class Game:

    navigation = ["Type HELP for manual.",
                  "Press Enter to commit input."]

    def __init__(self, map: GameState):
        self.GUI = GUI(self)
        self.game_state = map
        self.input_handler = InputHandler()
        self.command_runner = CommandRunner(self.game_state)

    def run_console(self):
        room = self.game_state.rooms[self.game_state.hero.location]

        print("\n-----------------------------\n")
        print("Welcome, warrior!")
        print(f"You entered the {room.description.lower()}")
        print("What is your next step?")
        print('\n' + '\n'.join(self.navigation))

        while True:
            print(">>> ", end="")
            user_input = input()

            if re.match("^help$|^HELP$", user_input):
                print_help()
                continue

            if re.match("^q$|^Q$|^quit$|^QUIT$", user_input):
                return

            commands_to_run = self.input_handler.parse_user_input(user_input)
            self.command_runner.execute(commands_to_run)

    def run_gui(self):
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
            if re.match("^help$|^HELP$", user_input):
                print_help()

            elif re.match("^q$|^Q$|^quit$|^QUIT$", user_input):
                sys.exit(0)

            else:
                commands_to_run = self.input_handler.parse_user_input(user_input)
                self.command_runner.execute(commands_to_run)

            output = buffer.getvalue()
            self.GUI.setOutput(output)


def print_help():
    print("Basic commands:")
    print("Type LOOK for more information about the environment.")
    print("Type INVENTORY to check out the collected items.")
    print("Type EQUIP to try on an game_item from the inventory.")
    print("Type STATUS to print out you current Hero status.")
    print("Type EXAMINE <game_item name> to learn more about an game_item.")
    print("Type QUIT or Q to quit game.")
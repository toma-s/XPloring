from GameStateSaver import GameStateSaver
from src.GameState import GameState
from src.InputHandler import InputHandler
from src.GUI import GUI
import re
import sys

import io
from contextlib import redirect_stdout


class Game:
    help_tooltip = "Type HELP for manual."
    enter_tooltip = "Press Enter to execute command."

    def __init__(self, game_state: GameState):
        self.GUI = GUI(self)
        self.game_state = game_state
        self.input_handler = InputHandler(game_state)

    def run_console(self):
        self._on_load_introduction_print()

        while True:
            print(">>> ", end="")
            user_input = input()

            if re.match("^help$|^HELP$", user_input):
                self.print_help()
                continue

            if re.match("^save|^SAVE$", user_input):
                self.print_saving()
                GameStateSaver(self.game_state).save()
                self.print_saved()
                continue

            if re.match("^q$|^Q$|^quit$|^QUIT$", user_input):
                return

            self.input_handler.handle_user_input(user_input)

    def run_gui(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self._on_load_introduction_print()

            print(">>> ")

            output = buffer.getvalue()
            self.GUI.setOutput(output)

    def react_to_input(self, user_input):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            if re.match("^help$|^HELP$", user_input):
                self.print_help()

            elif re.match("^save$|^SAVE$", user_input):
                self.print_saving()
                GameStateSaver(self.game_state).save()
                self.print_saved()

            elif re.match("^q$|^Q$|^quit$|^QUIT$", user_input):
                sys.exit(0)

            else:
                self.input_handler.handle_user_input(user_input)

            output = buffer.getvalue()
            self.GUI.setOutput(output)

    def _on_load_introduction_print(self):
        hero = self.game_state.hero
        room = self.game_state.rooms[hero.location]
        print("\n-----------------------------\n")
        print(f"You are in the {room.alias}. {room.description}")
        print("What is your next step?")
        print()
        print(self.help_tooltip)
        print(self.enter_tooltip)

    @staticmethod
    def print_help():
        print("Basic commands:")
        print("Type LOOK for more information about the environment.")
        print("Type INVENTORY to check out the collected items.")
        print("Type TAKE <item> to add an item to the inventory.")
        print("Type DROP <item> to remove item from the inventory.")
        print("Type EQUIP <item> to arm yourself an item from the inventory.")
        print("Type UNEQUIP <item> to disarm yourself an item from the inventory.")
        print("Type STATUS to show your HP, Attack Power and equipment.")
        print("Type EXAMINE <target> to learn more about an item.")
        print("Type SAVE to save current game.")
        print("Type QUIT or Q to quit game.")

    @staticmethod
    def print_saved():
        print("Game state has been saved successfully.")

    @staticmethod
    def print_saving():
        print("Saving ...")

from src.GameState import GameState
from src.InputHandler import InputHandler
from src.CommandRunner import CommandRunner
import re

class Game:

    navigation = ["Type LOOK for more information about the environment.",
                  "Type QUIT or Q to quit game."] # ...

    def __init__(self, map: GameState):
        self.game_state = map
        self.input_handler = InputHandler()
        self.command_runner = CommandRunner(self.game_state)

    def run(self):
        # mainloop
        room = self.game_state.rooms[self.game_state.hero.location]

        print("Welcome, warrior!")
        print(f"You entered the {room.description.lower()}")
        print("What is your next step?")
        print('\n' + '\n'.join(self.navigation))

        while True:
            print(">>> ", end="")
            user_input = input()

            if re.match("q|Q|quit|QUIT", user_input):
                return

            commands_to_run = self.input_handler.parse_user_input(user_input)
            self.command_runner.execute(commands_to_run)

from src.GameState import GameState
from src.InputHandle import InputHandle
from src.CommandRunner import CommandRunner

class Game:

    def __init__(self, map: GameState):
        self.game_state = map
        self.input_handler = InputHandle()
        self.command_runner = CommandRunner(self.game_state)

    def run(self):
        # mainloop
        room = self.game_state.rooms[self.game_state.hero.location]
        print(room.description)
        while True:
            print(">>> ", end="")
            inp = input()

            if inp == "q":
                return

            commands_to_run = self.input_handler.parse_user_input(inp)
            self.command_runner.execute(commands_to_run)

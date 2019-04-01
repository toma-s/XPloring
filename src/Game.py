from src.GameState import GameState
from src.InputHandle import InputHandle


class Game:

    def __init__(self, GameState):
        self.game_state = GameState
        self.input_handle = InputHandle(GameState)
        ...

    def run(self):
        # mainloop
        while True:
            print(">>> ")
            inp = input()

            commands_to_run = self.input_handle.parse_user_input(inp)

            self.input_handle.run_commands(commands_to_run)

            print(self.game_state.items[self.game_state.rooms[self.game_state.hero.location].items[0]].actions)

            if not commands_to_run:
                print("Wrong input")
            else :
                print(commands_to_run)

            ...

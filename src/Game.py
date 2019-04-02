from src.GameState import GameState
from src.InputHandle import InputHandle

class Game:

    def __init__(self, map: GameState):
        self.game_state = map
        self.input_handle = InputHandle(map)
        ...

    def run(self):
        # mainloop
        room = self.game_state.rooms[self.game_state.hero.location]
        print(room.description)
        while True:
            print(">>> ", end="")
            inp = input()

            if inp == "q":
                return

            commands_to_run = self.input_handle.parse_user_input(inp)

            self.input_handle.run_commands(commands_to_run)

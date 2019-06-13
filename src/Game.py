from src.GameState import GameState
from src.InputHandler import InputHandler


class Game:
    help_tooltip = "Type HELP for manual."
    enter_tooltip = "Press Enter to execute command."

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.input_handler = InputHandler(game_state)

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
    def _print_help():
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
    def _print_saved():
        print("Game state has been saved successfully.")

    @staticmethod
    def _print_saving():
        print("Saving ...")

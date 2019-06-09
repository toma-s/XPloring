from Finder import Finder
from InternalCommandHandler import InternalCommandHandler
from commands import commands_directions
from game_item.Hero import Hero
from src.GameState import GameState
from game_item.Weapon import Weapon
from game_item.Armour import Armour


class CommandHandler:

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        # TODO
        self.internal_command_handler = InternalCommandHandler(game_state)
        self.finder = Finder(game_state)

    def handle_commands(self, commands: [str]) -> None:
        ignored = {"the", "on", "a", "an", "this", "that"}
        commands = [command for command in commands if command not in ignored]
        action_name = commands[0]
        target_alias = " ".join(commands[1:])
        if len(commands) == 1:
            self.single_command(action_name)
        else:
            self.double_command(action_name, target_alias)

    def single_command(self, action_name: str) -> None:
        hero = self.game_state.hero
        if action_name not in hero.actions:
            print(f"I don't understand that command.")
            return
        action_data = hero.actions[action_name]
        self.internal_command_handler.handle_internal_command(action_data)

    def double_command(self, action_name: str, target_alias: str) -> None:
        hero = self.game_state.hero
        if action_name in hero.actions:
            action_data = hero.actions[action_name]
            self.internal_command_handler.handle_internal_command(action_data, target_alias)
            return

        if self._is_keyword(target_alias):
            print(f"This action is not allowed with the {target_alias}.")
            return
        found_ids = self.finder.find_ids_by_alias(target_alias)
        if not self._check_found_one_id_only(found_ids, target_alias):
            return

        target_id = found_ids[0]
        data = self.finder.get_data_by_id(target_id)

        if data is None or action_name not in data.actions:
            print(f"Action \"{action_name}\" is not allowed with the {target_alias}.")
            return

        action_data = data.actions[action_name]
        self.internal_command_handler.handle_internal_command(action_data, target_id)

    def _check_found_one_id_only(self, ids, target_alias) -> bool:
        if len(ids) == 0:
            print(f"There is no such thing as {target_alias}.")
            return False
        if len(ids) > 1:
            print(f"There are {len(ids)} \"{target_alias}\". You have to be more specific.")
            return False
        return True


    @staticmethod
    def _capitalize_first(input: str):
        return input[0].capitalize() + input[1:]

    @staticmethod
    def _is_keyword(target_alias):
        if target_alias == "inventory":
            return True
        if target_alias in commands_directions:
            return True

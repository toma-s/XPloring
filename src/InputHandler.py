from Finder import Finder
from InternalCommandHandler import InternalCommandHandler
from commands import commands_directions, commands_actions
from game_item.Hero import Hero
from src.GameState import GameState
from game_item.Weapon import Weapon
from game_item.Armour import Armour


class InputHandler:

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.internal_command_handler = InternalCommandHandler(game_state)
        self.finder = Finder(game_state)

    def handle_user_input(self, user_input: str) -> None:
        commands_to_run = self.parse_user_input(user_input)
        self.execute_commands(commands_to_run)

    def parse_user_input(self, user_input):
        user_input_words = user_input.strip().lower().split(" ")
        ignored_words = {"the", "to", "on", "a", "an", "this", "that", "these", "those"}
        parsed_words = []
        for word in user_input_words:
            if word in ignored_words:
                continue
            checked_word = self.match_keyword(word)
            parsed_words.append(checked_word)
        return parsed_words

    def execute_commands(self, commands: [str]) -> None:
        action_name = commands[0]
        target_alias = " ".join(commands[1:])
        if len(commands) == 1:
            self.single_command(action_name)
        else:
            self.double_command(action_name, target_alias)

    def single_command(self, action_name: str) -> None:
        hero = self.game_state.hero
        if action_name in hero.actions:
            action_data = hero.actions[action_name]
            self.internal_command_handler.handle_internal_command(action_data)
        else:
            print(f"I don't understand that command.")

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
    def match_keyword(input_word) -> str:
        keywords = dict()
        keywords.update(commands_directions)
        keywords.update(commands_actions)

        for command, synonyms in keywords.items():
            if input_word == command or input_word in synonyms: # in synonyms
                return command

        return input_word


    @staticmethod
    def _capitalize_first(input: str):
        return input[0].capitalize() + input[1:]

    @staticmethod
    def _is_keyword(target_alias):
        if target_alias == "inventory":
            return True
        if target_alias in commands_directions:
            return True



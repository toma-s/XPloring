from src.commands import commands_directions, commands_actions

class InputHandler:

    def __init__(self):
        pass

    def parse_user_input(self, user_input):
        user_input_words = user_input.strip().split(" ")

        for i in range(len(user_input_words)):
            checked_word = self.check_word(user_input_words[i])
            if checked_word is not None:
                user_input_words[i] = checked_word
        return user_input_words

    def check_word(self, word):
        actions = commands_actions.keys()
        directions = commands_directions.keys()
        correct_commands = actions | directions

        if word in correct_commands:
            return word

        for command in commands_actions:
            if word in commands_actions[command]: # in synonyms
                return command

        return None

from src.commands import commands_directions, commands_actions

class InputHandle:

    def __init__(self):
        pass

    def parse_user_input(self, input):
        x = input.strip().split(" ")

        for i in range(len(x)):
            tmp = self.check_word(x[i])
            if tmp:
                x[i] = tmp
        return x

    def check_word(self, word):
        if word in commands_actions or word in commands_directions:
            return word

        for command in commands_actions:
            if word in commands_actions[command]:
                return command

        return None

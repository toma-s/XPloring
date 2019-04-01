from src.GameState import GameState
from src.Commands import commands_directions, commands_actions


class InputHandle:

    def __init__(self, GameState):
        self.gs = GameState

    def parse_user_input(self, input):
        res = []

        x = input.strip().split(" ")
        for word in x:
            word = word.lower()
            tmp = self.check_word(word)
            if tmp:
                res.append(tmp)

        if self.check_commands(res):
            return res

        return []

    def check_word(self, word):
        if word in commands_actions or word in commands_directions:
            return word

        for command in commands_actions:
            if word in commands_actions[command]:
                return command

        return None

    def check_commands(self, commands):
        i = 0
        last_command = ""
        for command in commands:

            if i == 0 and command not in commands_actions:
                return False
            elif i == 0:
                last_command = command
                i += 1
                continue

            if i == 1:
                # ak go -> direction
                if last_command == "go":
                    if command not in commands_directions:
                        return False
                    else:
                        i += 1
                        continue

                # ak "eat" -> "item:food" ?


        return True


    def run_commands(self, commands):
        ...


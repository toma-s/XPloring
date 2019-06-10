import json

from GameStateSaver import GameStateSaver


class TestingGameStateSaver(GameStateSaver):

    def __init__(self, game_state):
        super().__init__(game_state)

    def save(self):
        data = super()._load_data()
        return self._store(data)

    @staticmethod
    def _store(data):
        return json.dumps(data, indent=2)

from GameState import GameState
from game_items.Room import Room
from game_items.TransitionObject import TransitionObject


class Finder:

    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def get_data_by_id(self, id):
        if id in self.game_state.items:
            return self.game_state.items[id]
        if id in self.game_state.equipment:
            return self.game_state.equipment[id]
        if id in self.game_state.creatures:
            return self.game_state.creatures[id]
        if id in self.game_state.transition_objects:
            return self.game_state.transition_objects[id]
        return None

    def find_ids_by_alias(self, target_alias) -> [str]:
        hero = self.game_state.hero
        found_ids = []
        found_ids += self._find_item_ids_by_alias_in_inventory(target_alias)
        found_ids += self._find_item_ids_by_alias_in_room(hero.location, target_alias)
        found_ids += self._find_trans_obj_ids_by_alias(target_alias)
        found_ids += self._find_creature_ids_by_alias(target_alias)
        return found_ids

    def _find_item_ids_by_alias_in_inventory(self, target_alias) -> [str]:
        item_ids_in_inventory = self.game_state.hero.inventory

        found_ids = []
        for item_id in item_ids_in_inventory:
            if item_id in self.game_state.items:
                item_data = self.game_state.items[item_id]
                if target_alias in [alias.lower() for alias in item_data.alias]:
                    found_ids.append(item_id)
            if item_id in self.game_state.equipment:
                item_data = self.game_state.equipment[item_id]
                if target_alias in [alias.lower() for alias in item_data.alias]:
                    found_ids.append(item_id)
        return found_ids

    def _find_item_ids_by_alias_in_room(self, room_id, target_alias) -> [str]:
        room: Room = self.game_state.rooms[room_id]
        item_ids_in_room = room.items

        found_ids = []
        for item_id in item_ids_in_room:
            if item_id in self.game_state.items:
                item_data = self.game_state.items[item_id]
                if target_alias in [alias.lower() for alias in item_data.alias]:
                    found_ids.append(item_id)
            if item_id in self.game_state.equipment:
                item_data = self.game_state.equipment[item_id]
                if target_alias in [alias.lower() for alias in item_data.alias]:
                    found_ids.append(item_id)
        return found_ids

    def _find_trans_obj_ids_by_alias(self, target_alias) -> [str]:
        found_ids = []

        hero = self.game_state.hero
        hero_room = self.game_state.rooms[hero.location]

        for direction in hero_room.directions:
            if "trans_obj_id" in hero_room.directions[direction]:
                trans_obj_id = hero_room.directions[direction]["trans_obj_id"]
                trans_obj_data: TransitionObject = self.game_state.transition_objects[trans_obj_id]
                if target_alias in [alias.lower() for alias in trans_obj_data.alias]:
                    found_ids.append(trans_obj_id)
        return found_ids

    def _find_creature_ids_by_alias(self, target_alias) -> [str]:
        found_ids = []

        hero = self.game_state.hero
        hero_room = self.game_state.rooms[hero.location]

        for creature_id in hero_room.creatures:
            if creature_id in self.game_state.creatures:
                creature_data = self.game_state.creatures[creature_id]
                if target_alias in [alias.lower() for alias in creature_data.alias]:
                    found_ids.append(creature_id)
        return found_ids

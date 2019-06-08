import unittest

from GameStateLoader import GameStateLoader
from game_item.Armour import Armour
from game_item.Consumable import Consumable
from game_item.Creature import Creature
from game_item.Hero import Hero
from game_item.Item import Item
from game_item.Room import Room
from game_item.Weapon import Weapon


class TestGameStateLoader(unittest.TestCase):

    file_path = "../game_states/game_test_loader.json"
    game_data = GameStateLoader.read_file(file_path)
    loader = GameStateLoader(game_data)

    def test_create_rooms(self):
        result = self.loader.create_rooms()
        self.assertSetEqual({"#room1", "#room2"}, set(result.keys()))

        room1 = result["#room1"]
        self.assertIsInstance(room1, Room)
        self.assertEqual("Room #1", room1.description)
        self.assertListEqual(["#item1"], room1.items)
        self.assertListEqual(["#creature1"], room1.creatures)
        self.assertDictEqual(
            {
                "west":
                {
                    "room_id": "#room2"
                }
            },
            room1.directions
        )

        room2 = result["#room2"]
        self.assertIsInstance(room2, Room)
        self.assertEqual("Room #2", room2.description)
        self.assertListEqual(["#item2"], room2.items)
        self.assertListEqual(["#creature2"], room2.creatures)
        self.assertDictEqual(
            {
                "east":
                {
                     "room_id": "#room1"
                }
            },
            room2.directions
        )

    def test_create_creatures(self):
        result = self.loader.create_creatures()
        self.assertSetEqual({"#creature1", "#creature2"}, set(result.keys()))

        creature1 = result["#creature1"]
        self.assertIsInstance(creature1, Creature)
        self.assertEqual("Creature #1", creature1.description)
        self.assertListEqual(["beast 1"], creature1.alias)
        self.assertEqual(50, creature1.health)
        self.assertEqual(10, creature1.damage)
        self.assertListEqual(["#item1"], creature1.drops)

        creature2 = result["#creature2"]
        self.assertIsInstance(creature2, Creature)
        self.assertEqual("Creature #2", creature2.description)
        self.assertListEqual(["beast 2"], creature2.alias)
        self.assertEqual(100, creature2.health)
        self.assertEqual(50, creature2.damage)
        self.assertListEqual(["#item2"], creature2.drops)

    def test_create_transition_objects(self):
        result = self.loader.create_transition_objects()
        self.assertDictEqual(dict(), result)

    def test_create_items(self):
        result = self.loader.create_items()
        self.assertSetEqual({"#item1", "#item2"}, set(result.keys()))

        item1 = result["#item1"]
        self.assertIsInstance(item1, Item)
        self.assertEqual("Regular Item #1", item1.description)
        self.assertListEqual(["regular item 1"], item1.alias)
        self.assertDictEqual(
            {
                "open": {
                    "command_spawn_item": "#item2"
                },
                "take": {
                    "command_add_item_to_inventory": None
                },
                "examine": {
                    "command_show_description": None
                }
            }, item1.actions
        )

        item2 = result["#item2"]
        self.assertIsInstance(item2, Consumable)
        self.assertEqual("Consumable Item #2", item2.description)
        self.assertListEqual(["consumable item 2"], item2.alias)
        self.assertDictEqual(
            {
                "use": {
                    "command_required_item": "#item1",
                    "command_use_item": True
                },
                "take": {
                    "command_add_item_to_inventory": None
                },
                "examine": {
                    "command_show_description": None
                }
            }, item2.actions
        )
        self.assertEqual(50, item2.value)

    def test_create_equipment(self):
        result = self.loader.create_equipment()
        self.assertSetEqual({"#weapon1", "#armour1"}, set(result.keys()))

        armour1 = result["#armour1"]
        self.assertIsInstance(armour1, Armour)
        self.assertEqual("Armour Equipment", armour1.description)
        self.assertListEqual(["armour equipment"], armour1.alias)
        self.assertEqual("head", armour1.slot)
        self.assertEqual(False, armour1.in_use)
        self.assertEqual(5, armour1.resistance)
        self.assertEqual(10, armour1.durability)

        weapon1 = result["#weapon1"]
        self.assertIsInstance(weapon1, Weapon)
        self.assertEqual("Weapon Equipment", weapon1.description)
        self.assertListEqual(["weapon equipment"], weapon1.alias)
        self.assertEqual("hand", weapon1.slot)
        self.assertEqual(False, weapon1.in_use)
        self.assertEqual(50, weapon1.damage)

    def test_create_hero(self):
        hero = self.loader.create_hero()
        self.assertIsInstance(hero, Hero)
        self.assertEqual(100, hero.health)
        self.assertEqual("#room1", hero.location)
        self.assertEqual("#weapon1", hero.right_hand)
        self.assertEqual("none", hero.left_hand)
        self.assertEqual("#armour1", hero.head)
        self.assertEqual("none", hero.chest)
        self.assertEqual("none", hero.legs)
        self.assertDictEqual(dict(), hero.actions)
        self.assertListEqual(["#item1"], hero.inventory)

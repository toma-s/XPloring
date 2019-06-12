import unittest
import contextlib
import io
from sys import stdout

from InputHandler import InputHandler
from GameState import GameState
from game_item.Creature import Creature
from game_item.Hero import Hero
from game_item.Room import Room


class TestCave(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/cave-of-awakening.json'
        self.game_state = GameState(self.map0)
        self.ih = InputHandler(self.game_state)

    def tearDown(self) -> None:
        del self.game_state
        del self.ih

    def test_full_game(self):
        hero = self.game_state.hero
        self.ih.handle_user_input("go north")
        self.ih.handle_user_input("go east")

        self.assertEqual("#room_abandoned_campsite", hero.location)

        campsite: Room = self.game_state.rooms["#room_abandoned_campsite"]

        self.ih.handle_user_input("examine tent")

        self.assertIn("#item_wooden_box_full", campsite.items)
        self.assertNotIn("#item_wooden_box_empty", campsite.items)

        self.ih.handle_user_input("open box")

        self.assertNotIn("#item_wooden_box_full", campsite.items)
        self.assertIn("#item_wooden_box_empty", campsite.items)

        self.ih.handle_user_input("take lighter")
        self.ih.handle_user_input("go west")
        self.ih.handle_user_input("go north")
        self.ih.handle_user_input("examine dead body")
        for i in range(6):
            self.ih.handle_user_input("attack dead adventurer")
        self.ih.handle_user_input("take lantern")
        self.ih.handle_user_input("light lantern")
        self.ih.handle_user_input("light darkness")
        self.ih.handle_user_input("go north")

        self.assertEqual("#room_darkroom", hero.location)

        self.ih.handle_user_input("go west")
        self.assertEqual("#room_ancient_temple", hero.location)

        temple_room: Room = self.game_state.rooms["#room_ancient_temple"]
        self.ih.handle_user_input("whip staff")
        self.assertIn("#equipment_artifact_staff_of_awakening", hero.inventory)

        self.ih.handle_user_input("equip staff")
        self.assertEqual("#equipment_artifact_staff_of_awakening", hero.weapon_slot)

        self.ih.handle_user_input("attack demon")

        self.assertIn("#item_thank_you_letter", temple_room.items)


    def test_light_lantern(self):
        hero: Hero = self.game_state.hero
        hero.inventory.append("#item_lantern_extinguished")
        hero.inventory.append("#item_lighter")

        self.assertIn("#item_lantern_extinguished", hero.inventory)
        self.assertNotIn("#item_lantern_lit", hero.inventory)

        self.ih.handle_user_input("light lantern")

        self.assertNotIn("#item_lantern_extinguished", hero.inventory)
        self.assertIn("#item_lantern_lit", hero.inventory)


    def test_dead_body_zombie(self):
        self.game_state.hero.location = "#room_passage_level_2"
        room2: Room = self.game_state.rooms["#room_passage_level_2"]
        self.assertNotIn("#item_lantern_extinguished", room2.items)
        self.assertIn("#item_dead_body", room2.items)
        self.assertNotIn("#creature_zombie_adventurer", room2.creatures)

        self.ih.handle_user_input("examine dead body")

        self.assertNotIn("#item_lantern_extinguished", room2.items)
        self.assertNotIn("#item_dead_body", room2.items)
        self.assertIn("#creature_zombie_adventurer", room2.creatures)

        for i in range(6):
            self.ih.handle_user_input("attack dead adventurer")

        self.assertEqual(0, self.game_state.creatures["#creature_zombie_adventurer"].health)

        self.assertIn("#item_lantern_extinguished", room2.items)
        self.assertNotIn("#item_dead_body", room2.items)
        self.assertIn("#creature_zombie_adventurer", room2.creatures)

    def test_artifact_fight(self):
        hero = self.game_state.hero
        hero.location = "#room_ancient_temple"

        self.ih.handle_user_input("whip staff")
        self.assertIn("#equipment_artifact_staff_of_awakening", hero.inventory)

        self.ih.handle_user_input("equip staff")
        self.assertEqual("#equipment_artifact_staff_of_awakening", hero.weapon_slot)

        self.ih.handle_user_input("attack demon")
        demon = self.game_state.creatures["#creature_temple_demon"]
        self.assertEqual(0, demon.health)
        self.assertEqual(100, hero.health)

        self.ih.handle_user_input("attack demon")
        demon = self.game_state.creatures["#creature_temple_demon"]
        self.assertEqual(0, demon.health)
        self.assertEqual(100, hero.health)

    def test_bad_end(self):
        hero = self.game_state.hero
        hero.location = "#room_ancient_temple"

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.ih.handle_user_input("attack demon")
        result_output = stdout.getvalue()
        expected_output = "You hit the guardian of the artifact for 5 damage! Guardian of the artifact has 95 HP left.\n" \
                          "Guardian of the artifact hit you for 100 damage! You have 0 HP left.\n" \
                          "GAME OVER. You were killed by guardian of the artifact. Better luck next time.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual('0', str(e.exception))

        demon: Creature = self.game_state.creatures["#creature_temple_demon"]
        self.assertEqual(95, demon.health)
        self.assertEqual(0, hero.health)

    def test_good_end(self):
        hero: Hero = self.game_state.hero
        hero.inventory.append("#item_thank_you_letter")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as e:
            self.ih.handle_user_input("read letter")
        result_output = stdout.getvalue()
        expected_output = "If you are reading this, it means you have solved my puzzles\nand collected the artifact.\nThank you for your time, it means a lot to me.\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual('0', str(e.exception))


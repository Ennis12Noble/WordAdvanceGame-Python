import unittest
from random import random

from treasure_hunt import *


class TestTreasureHunt(unittest.TestCase):
    def test_create_room(self):
        room = Room(12)
        self.assertEqual(12, room.number, "Room number does not match!")
        self.assertEqual([], room.neighbors, "Room should have no neighbors")
        self.assertEqual([], room.hazards, "Room should have no hazards")

    def test_room_hazard_present(self):
        room = Room(12)
        room.hazards.append("bats")
        room.hazards.append("pits")
        self.assertTrue(room.has("pits"), "Expected pits hazard but not found!")

    def test_room_hazard_absent(self):
        room = Room(12)
        room.hazards.append("bats")
        self.assertFalse(room.has("pits"), "Pits not in room but found!")

    def test_room_add_hazard(self):
        hazards = ["bats", "dogs"]
        room = Room(12)
        room.add("bats")
        room.add("dogs")
        self.assertEqual(hazards, room.hazards, "Failed to add hazards")

    def test_room_remove_hazard(self):
        room = Room(12)
        room.hazards = ["bats", "dogs"]
        room.remove("dogs")
        self.assertNotIn("dogs", room.hazards, "Failed to remove hazard in room!")

    def test_room_remove_absent_hazard(self):
        room = Room(12)
        room.hazards = ["bats", "dogs"]
        with self.assertRaises(ValueError):
            room.remove("guard")

    def test_room_empty(self):
        room = Room(12)
        self.assertTrue(room.empty(), "Expected room to have no hazards!")

    def test_room_not_empty(self):
        room = Room(12)
        room.hazards = ["bats", "dogs"]
        self.assertFalse(room.empty(), "Expected room to have hazards!")

    def test_room_is_not_safe_1(self):
        room = Room(12)
        room.hazards = ["bats", "dogs"]
        self.assertFalse(room.safe(), "Room has hazards; expected not to be safe!")

    def test_room_is_not_safe_2(self):
        room = Room(12)
        room1 = Room(8)
        room2 = Room(4)
        room1.hazards = ["bats", "pits", "guard"]
        room.neighbors = [room1, room2]
        room1.neighbors = [room]
        room2.neighbors = [room]
        self.assertFalse(room.safe(), "Room has hazards; expected not to be safe!")

    def test_room_is_not_safe_3(self):
        room = Room(12)
        room1 = Room(8)
        room2 = Room(4)
        room2.hazards = ["bats", "pits", "guard"]
        room.neighbors = [room1, room2]
        room1.neighbors = [room]
        room2.neighbors = [room]
        self.assertFalse(room.safe(), "Room has hazards; expected not to be safe!")

    def test_room_is_not_safe_4(self):
        room = Room(12)
        room1 = Room(8)
        room2 = Room(4)
        room1.hazards = ["bats", "pits", "guard"]
        room2.hazards = ["pits", "guard"]
        room.neighbors = [room1, room2]
        room1.neighbors = [room]
        room2.neighbors = [room]
        self.assertFalse(room.safe(), "Room has hazards; expected not to be safe!")

    def test_room_is_safe_1(self):
        room = Room(12)
        self.assertTrue(room.safe(), "Room has no hazards and no neighbors; expected to be safe!")

    def test_room_is_safe_2(self):
        room = Room(12)
        room1 = Room(8)
        room2 = Room(4)
        room1.hazards = []
        room2.hazards = []
        room.neighbors = [room1, room2]
        room1.neighbors = [room]
        room2.neighbors = [room]
        self.assertTrue(room.safe(), "Room and its neighbors have no hazards; expected not to be safe!")

    def test_room_connect(self):
        room1 = Room(10)
        room2 = Room(2)
        room1.connect(room2)
        self.assertIn(room2, room1.neighbors, "Expected room 2 to be neighbor of room 10")
        self.assertIn(room1, room2.neighbors, "Expected room 10 to be neighbor of room 2")

    def test_room_exits(self):
        room = Room(10)
        room1 = Room(5)
        room2 = Room(15)
        room3 = Room(18)
        room.neighbors = [room1, room2, room3]
        room1.neighbors = [room]
        room2.neighbors = [room]
        room3.neighbors = [room]
        self.assertIn(5, room.exits(), "Expected room 5 to be in exits of room 10")
        self.assertIn(15, room.exits(), "Expected room 15 to be in exits of room 10")
        self.assertIn(18, room.exits(), "Expected room 18 to be in exits of room 10")

    def test_room_exits_absent(self):
        room = Room(10)
        room1 = Room(5)
        room2 = Room(15)
        room3 = Room(18)
        room4 = Room(20)
        room.neighbors = [room1, room2, room3]
        room1.neighbors = [room]
        room2.neighbors = [room]
        room3.neighbors = [room, room4]
        room4.neighbors = [room3]
        self.assertIn(5, room.exits(), "Expected room 5 to be in exits of room 10")
        self.assertIn(15, room.exits(), "Expected room 15 to be in exits of room 10")
        self.assertIn(18, room.exits(), "Expected room 18 to be in exits of room 10")
        self.assertNotIn(20, room.exits(), "Expected room 20 not to be in exits of room 10")

    def test_room_empty_exits(self):
        room = Room(10)
        self.assertEqual(0, len(room.exits()), "Expected room to have no exits")

    def test_room_neighbor(self):
        room = Room(17)
        room1 = Room(5)
        room2 = Room(15)
        room3 = Room(18)
        room.neighbors = [room1, room2, room3]
        room1.neighbors = [room]
        room2.neighbors = [room]
        room3.neighbors = [room]
        self.assertEqual(room1, room.neighbor(5), "Expected room 5!")
        self.assertEqual(room2, room.neighbor(15), "Expected room 15!")
        self.assertEqual(room3, room.neighbor(18), "Expected room 18!")

    def test_room_neighbor_none(self):
        room = Room(17)
        room1 = Room(5)
        room2 = Room(15)
        room3 = Room(18)
        room.neighbors = [room1, room2, room3]
        room1.neighbors = [room]
        room2.neighbors = [room]
        room3.neighbors = [room]
        self.assertIsNone(room.neighbor(21), "Room 17 does not have neighbor room 21!")

    def test_room_random_neighbor(self):
        room = Room(17)
        room1 = Room(5)
        room2 = Room(15)
        room3 = Room(18)
        room.neighbors = [room1, room2, room3]
        room1.neighbors = [room]
        room2.neighbors = [room]
        room3.neighbors = [room]
        self.assertIn(room.random_neighbor(), room.neighbors, "Expected random neighbor of room 17")

    def test_room_no_neighbors_random_neighbor(self):
        room = Room(17)
        with self.assertRaises(IndexError):
            room.random_neighbor()

    def test_cave_rooms(self):
        cave = Cave()
        for room_number in cave.rooms:
            self.assertEqual(room_number, cave.rooms[room_number].number, f"Expected Room {room_number} to be in cave")

    def test_cave_connections(self):
        cave = Cave()
        for edge in cave.edges:
            self.assertIn(edge[0], [n.number for n in cave.rooms[edge[1]].neighbors], f"Room {edge[0]} not connected to Room {edge[1]}")
            self.assertIn(edge[1], [n.number for n in cave.rooms[edge[0]].neighbors], f"Room {edge[1]} not connected to Room {edge[0]}")

    def test_cave_random_room(self):
        cave = Cave()
        rooms = [cave.rooms[r] for r in cave.rooms]
        self.assertIn(cave.random_room(), rooms, "Expected random room to be in cave!")

    def test_case_add_hazards_1(self):
        cave = Cave()
        cave.add_hazard("bats", 5)
        self.assertEqual(5, len([True for hazard in [room.hazards for room in [cave.rooms[rn] for rn in cave.rooms]] if "bats" in hazard]), "Expected 5 bats in cave!")

    def test_case_add_hazards_2(self):
        cave = Cave()
        cave.add_hazard("pits", 8)
        self.assertEqual(8, len([True for hazard in [room.hazards for room in [cave.rooms[rn] for rn in cave.rooms]] if "pits" in hazard]), "Expected 8 pits in cave!")

    def test_cave_room_with_bats(self):
        cave = Cave()
        room = random.choice([cave.rooms[rn] for rn in cave.rooms])
        room.hazards.append("bats")
        cave.rooms[room.number] = room
        self.assertEqual(room, cave.room_with("bats"), f"Expected room {room.number} in cave to have bats")

    def test_cave_has_no_bats(self):
        cave = Cave()
        self.assertIsNone(cave.room_with("bats"), "Expected cave to have no bats!")

    def test_cave_move(self):
        cave = Cave()
        rooms = [cave.rooms[rn] for rn in cave.rooms]
        room1 = rooms[0]
        room2 = rooms[1]
        room1.hazards.append("guard")
        self.assertNotIn("guard", room2.hazards, f"Room {room2.number} should not have guard!")
        cave.move("guard", room1, room2)
        self.assertIn("guard", room2.hazards, f"Room {room2.number} should have guard!")
        self.assertNotIn("guard", room1.hazards, f"Room {room1.number} should not have guard!")

    def test_cave_move_absent_hazard(self):
        cave = Cave()
        rooms = [cave.rooms[rn] for rn in cave.rooms]
        room1 = rooms[0]
        room2 = rooms[1]
        self.assertNotIn("guard", room1.hazards, f"Room {room1.number} should not have guard!")
        with self.assertRaises(ValueError):
            cave.move("guard", room1, room2)

    def test_cave_room_present(self):
        cave = Cave()
        rooms = [cave.rooms[rn] for rn in cave.rooms]
        self.assertIn(cave.room(9), rooms, "Expected room 9 to be in cave")

    def test_cave_room_absent(self):
        cave = Cave()
        with self.assertRaises(KeyError):
            cave.room(89)

    def test_cave_entrance(self):
        cave = Cave()
        room = cave.entrance()
        self.assertTrue(len(room.hazards) == 0, "Expected room to have no hazards")
        safe_neighbors = [n for n in room.neighbors if len(n.hazards) != 0]
        self.assertTrue(len(safe_neighbors) == 0, "Expected neighbors to have no hazards")

    def test_player_enter_empty_room(self):
        encountered = set()
        player = Player()
        room = Room(18)
        player.encounter("guard", lambda : encountered.add('The Guard killed you!'))
        player.encounter("bats", lambda : encountered.add('The Bats whisked you away!'))
        player.enter(room)
        self.assertTrue(len(encountered) == 0, 'Expected no encounters in empty room')

    def test_player_enter_empty_room_with_nonempty_neighbors(self):
        encountered = set()
        player = Player()
        room = Room(18)
        room1 = Room(15)
        room1.hazards.append("pits")
        room.neighbors.append(room1)
        room1.neighbors.append(room)
        room2 = Room(7)
        room2.hazards.append("guard")
        room.neighbors.append(room2)
        room2.neighbors.append(room)
        player.encounter("guard", lambda : encountered.add('The Guard killed you!'))
        player.encounter("bats", lambda : encountered.add('The Bats whisked you away!'))
        player.enter(room)
        self.assertTrue(len(encountered) == 0, 'Expected no encounters in empty room')

    def test_player_enter_guard_room(self):
        encountered = set()
        player = Player()
        room = Room(18)
        room.hazards.append("guard")
        player.encounter("guard", lambda : encountered.add('The Guard killed you!'))
        player.encounter("bats", lambda : encountered.add('The Bats whisked you away!'))
        player.enter(room)
        self.assertTrue(encountered == {'The Guard killed you!'}, 'Expected to encounter guard in guard room')

    def test_player_enter_bats_room(self):
        encountered = set()
        player = Player()
        room = Room(18)
        room.hazards.append("bats")
        player.encounter("guard", lambda : encountered.add('The Guard killed you!'))
        player.encounter("bats", lambda : encountered.add('The Bats whisked you away!'))
        player.enter(room)
        self.assertTrue(encountered == {'The Bats whisked you away!'}, 'Expected to encounter bats in bats room')

    def test_player_enter_multihazards_room_1(self):
        encountered = set()
        player = Player()
        room = Room(18)
        room.hazards.append("bats")
        room.hazards.append("guard")
        player.encounter("guard", lambda : encountered.add('The Guard killed you!'))
        player.encounter("bats", lambda : encountered.add('The Bats whisked you away!'))
        player.enter(room)
        self.assertTrue(encountered == {'The Guard killed you!'}, 'Expected to encounter guard in room')

    def test_player_enter_multihazards_room_2(self):
        encountered = set()
        player = Player()
        room = Room(18)
        room.hazards.append("bats")
        room.hazards.append("guard")
        player.encounter("bats", lambda : encountered.add('The Bats whisked you away!'))
        player.encounter("guard", lambda : encountered.add('The Guard killed you!'))
        player.enter(room)
        self.assertTrue(encountered == {'The Bats whisked you away!'}, 'Expected to encounter bats in room')

    def test_player_explore_room_with_empty_neighbors(self):
        sensed = set()
        player = Player()
        player.sense("pits", lambda : sensed.add("You feel a cold wind blowing from a nearby cavern."))
        room = Room(17)
        room1 = Room(7)
        room.neighbors.append(room1)
        room1.neighbors.append(room)
        room2 = Room(9)
        room.neighbors.append(room2)
        room2.neighbors.append(room)
        player.room = room
        player.explore_room()
        self.assertTrue(len(sensed) == 0, "Expected to sense nothing!")

    def test_player_explore_room_with_pit_neighbors(self):
        sensed = set()
        player = Player()
        player.sense("pits", lambda : sensed.add("You feel a cold wind blowing from a nearby cavern."))
        room = Room(17)
        room1 = Room(7)
        room.neighbors.append(room1)
        room1.neighbors.append(room)
        room2 = Room(9)
        room.neighbors.append(room2)
        room2.neighbors.append(room)
        room2.hazards.append("pits")
        player.room = room
        player.explore_room()
        self.assertTrue(sensed == {"You feel a cold wind blowing from a nearby cavern."}, "Expected to sense pits!")

    def test_player_explore_room_with_multihazard_neighbors(self):
        sensed = set()
        player = Player()
        player.sense("pits", lambda : sensed.add("You feel a cold wind blowing from a nearby cavern."))
        player.sense("bats", lambda : sensed.add("Bats whisked you away."))
        room = Room(17)
        room1 = Room(7)
        room1.hazards.append("bats")
        room.neighbors.append(room1)
        room1.neighbors.append(room)
        room2 = Room(9)
        room.neighbors.append(room2)
        room2.neighbors.append(room)
        room2.hazards.append("pits")
        player.room = room
        player.explore_room()
        self.assertTrue(sensed == {"You feel a cold wind blowing from a nearby cavern.", "Bats whisked you away."}, "Expected to sense pits and bats!")

    def test_player_act_1(self):
        acted = set()
        player = Player()
        player.action("move", lambda dest : acted.add(f"Player moved to {dest}"))
        player.action("shoot", lambda dest : acted.add(f"Player shot at {dest}"))
        room = Room(19)
        player.act("move", room)
        self.assertTrue(acted == {f"Player moved to {room}"}, f"Expected to move to room {room.number}")

    def test_player_act_2(self):
        acted = set()
        player = Player()
        player.action("move", lambda dest : acted.add(f"Player moved to {dest}"))
        player.action("shoot", lambda dest : acted.add(f"Player shot at {dest}"))
        room = Room(11)
        player.act("shoot", room)
        self.assertTrue(acted == {f"Player shot at {room}"}, f"Expected to shoot at room {room.number}")

    def test_player_act_absent(self):
        acted = set()
        player = Player()
        player.action("move", lambda dest : acted.add(f"Player moved to {dest}"))
        player.action("shoot", lambda dest : acted.add(f"Player shot at {dest}"))
        room = Room(13)
        with self.assertRaises(KeyError):
            player.act("startle", room)

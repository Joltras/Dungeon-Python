import unittest

from floors.floor import Floor
from globals import RoomType, DoorFace
from rooms.room import Room


class FloorTest(unittest.TestCase):

    def setUp(self) -> None:
        self._floor = Floor(20, 30)
        self._floor_with_rooms = Floor(30, 30)
        self._floor_with_rooms.add_room(2, 2)
        self._floor_with_rooms.add_room(1, 2)
        self._floor_with_rooms.add_room(3, 2)
        self._floor_with_rooms.add_room(5, 5)

    def test_to_json(self):
        expected = '{\n  "_rooms": []\n}'
        self.assertEqual(expected, self._floor.to_json(1))

    def test_contains_room(self):
        self.assertFalse(self._floor.contains_room(1, 1))

    def test_add_to_floor_grid_error(self):
        with self.assertRaises(IndexError):
            self._floor.add_to_floor_grid(31, 0)

    def test_add_two_floor_grid(self):
        self._floor.add_to_floor_grid(2, 3)
        self.assertTrue(self._floor.contains_room(2, 3))

    def test_add_room(self):
        self._floor.add_room(1, 1)
        self.assertTrue(self._floor.contains_room(1, 1))
        self.assertEqual(Room(1, 1, 0, RoomType.NORMAL_ROOM), self._floor.get_rooms()[0])

    def test_get_rooms(self):
        rooms = [Room(2, 2, 0, RoomType.NORMAL_ROOM),
                 Room(1, 2, 1, RoomType.NORMAL_ROOM),
                 Room(3, 2, 2, RoomType.NORMAL_ROOM),
                 Room(5, 5, 3, RoomType.NORMAL_ROOM)]
        self.assertEqual(rooms, self._floor_with_rooms.get_rooms())

    def test_get_rooms2(self):
        self.assertEqual([], self._floor.get_rooms())

    def test_add_doors(self):
        self._floor_with_rooms.add_doors_to_rooms()
        self.assertEqual([DoorFace.EAST, DoorFace.WEST], self._floor_with_rooms.get_rooms()[0].get_doors())

    def test_add_doors2(self):
        self._floor_with_rooms.add_doors_to_rooms()
        self.assertEqual([], self._floor_with_rooms.get_rooms()[3].get_doors())

    def test_count_neighbours(self):
        self.assertEqual(2, self._floor_with_rooms.count_neighbours(2, 2))

    def test_count_neighbours2(self):
        self.assertEqual(0, self._floor_with_rooms.count_neighbours(5, 5))

    def test_is_dead_end(self):
        self.assertTrue(self._floor_with_rooms.is_dead_end(1, 2))

    def test_is_dead_end_false(self):
        self.assertFalse(self._floor_with_rooms.is_dead_end(2, 2))


if __name__ == '__main__':
    unittest.main()

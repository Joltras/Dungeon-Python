import unittest

from Globals import RoomType, DoorFace
from rooms.Room import Room


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._room = Room(10, 20, 1, RoomType.NORMAL_ROOM)

    def test_to_json(self):
        ecpected = \
            """{
    "_doors": [],
    "_id": 1,
    "_room_type": 0,
    "_x": 10,
    "_y": 20
}"""
        self.assertEqual(ecpected, self._room.toJSON())

    def test_get_doors(self):
        self.assertEqual([], self._room.get_doors())

    def test_add_door(self):
        self._room.add_door(DoorFace.TOP)
        expected = [DoorFace.TOP]
        self.assertEqual(expected, self._room.get_doors())

    def test_add_doors(self):
        self._room.add_door(DoorFace.TOP)
        self._room.add_door(DoorFace.BOTTOM)
        self._room.add_door(DoorFace.EAST)
        self._room.add_door(DoorFace.WEST)
        expected = [DoorFace.TOP, DoorFace.BOTTOM, DoorFace.EAST, DoorFace.WEST]
        self.assertEqual(expected, self._room.get_doors())

    def test_get_x(self):
        self.assertEqual(10, self._room.get_x())

    def test_get_y(self):
        self.assertEqual(20, self._room.get_y())

    def test_get_id(self):
        self.assertEqual(1, self._room.get_id())

    def test_get_room_type(self):
        self.assertEqual(RoomType.NORMAL_ROOM, self._room.get_type())

    def test_set_type(self):
        self._room.set_type(RoomType.BOSS_ROOM)
        self.assertEqual(RoomType.BOSS_ROOM, self._room.get_type())

    def test_set_cord(self):
        self._room.set_cord(50, 20)
        self.assertEqual(50, self._room.get_x())
        self.assertEqual(20, self._room.get_y())

    def test_eql(self):
        room = Room(10, 20, 1, RoomType.NORMAL_ROOM)
        self.assertTrue(room == self._room)

    def test_eql_false(self):
        room = Room(10, 30, 1, RoomType.NORMAL_ROOM)
        self.assertFalse(room == self._room)


if __name__ == '__main__':
    unittest.main()

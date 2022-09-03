import unittest

from pygame import Rect

import Globals
from Globals import Color, RoomType, DoorFace
from Room import Room


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._room = Room(10, 20, Color.ORANGE, 1, RoomType.NORMAL_ROOM)

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

    def test_get_color(self):
        self.assertEqual(Color.ORANGE, self._room.get_color())

    def test_get_rect(self):
        expected = Rect(10 * Globals.room_width + Globals.x_offset, 20 * Globals.room_height + Globals.y_offset,
                        Globals.room_width, Globals.room_height)
        self.assertEqual(expected, self._room.get_rect())

    def test_get_id(self):
        self.assertEqual(1, self._room.get_id())


if __name__ == '__main__':
    unittest.main()

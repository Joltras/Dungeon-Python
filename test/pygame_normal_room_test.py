import unittest

import globals
from rooms.pygame.pygame_normal_room import PygameNormalRoom
from globals import RoomType
from pygame import Rect


class PygameRoomTest(unittest.TestCase):
    def setUp(self) -> None:
        self._room1 = PygameNormalRoom(1, 2, 3, RoomType.NORMAL_ROOM)
        self._room2 = PygameNormalRoom(4, 5, 6, RoomType.SHOP_ROOM, 25, 36)

    def test_get_height1(self):
        self.assertEqual(globals.ROOM_HEIGHT, self._room1.get_height())

    def test_get_height2(self):
        self.assertEqual(36, self._room2.get_height())

    def test_get_width1(self):
        self.assertEqual(globals.ROOM_WIDTH, self._room1.get_width())

    def test_get_width2(self):
        self.assertEqual(25, self._room2.get_width())

    def test_get_rect(self):
        expected = Rect(
            1 * globals.ROOM_WIDTH + globals.x_offset,
            2 * globals.ROOM_HEIGHT + globals.y_offset,
            globals.ROOM_WIDTH,
            globals.ROOM_HEIGHT,
        )
        self.assertEqual(expected, self._room1.get_rect())

    def test_get_rect2(self):
        expected = Rect(4 * 25 + globals.x_offset, 5 * 36 + globals.y_offset, 25, 36)
        self.assertEqual(expected, self._room2.get_rect())

    def test_set_coordinates1(self):
        self._room1.set_cord(6, 7)
        expected = Rect(
            6 * globals.ROOM_WIDTH + globals.x_offset,
            7 * globals.ROOM_HEIGHT + globals.y_offset,
            globals.ROOM_WIDTH,
            globals.ROOM_HEIGHT,
        )
        self.assertEqual(expected, self._room1.get_rect())

    def test_set_coordinates2(self):
        self._room2.set_cord(20, 55)
        expected = Rect(20 * 25 + globals.x_offset, 55 * 36 + globals.y_offset, 25, 36)
        self.assertEqual(expected, self._room2.get_rect())


if __name__ == "__main__":
    unittest.main()

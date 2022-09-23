import os
import unittest
import Globals
from Globals import RoomType, Color, Direction

class GlobalsTest(unittest.TestCase):

    def test_directions(self):
        expected = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (-1, -1), (1, 1), (-1, 1)]
        self.assertEqual(expected, Direction.list())

    def test_up(self):
        self.assertEqual((0, -1), Direction.UP.value)

    def test_right(self):
        self.assertEqual((1, 0), Direction.RIGHT.value)

    def test_down(self):
        self.assertEqual((0, 1), Direction.DOWN.value)

    def test_left(self):
        self.assertEqual((-1, 0), Direction.LEFT.value)

    def test_up_right(self):
        self.assertEqual((1, -1), Direction.UP_RIGHT.value)

    def test_up_left(self):
        self.assertEqual((-1, -1), Direction.UP_LEFT.value)

    def test_down_right(self):
        self.assertEqual((1, 1), Direction.DOWN_RIGHT.value)

    def test_down_left(self):
        self.assertEqual((-1, 1), Direction.DOWN_LEFT.value)

    def test_door_faces(self):
        expected = [0, 1, 2, 3]
        self.assertEqual(expected, Globals.DoorFace.list())

    def test_room_types(self):
        expected = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(expected, RoomType.list())

    def test_special_rooms(self):
        self.assertEqual((RoomType.ITEM_ROOM, RoomType.SHOP_ROOM), Globals.SPECIAL_ROOMS)

    def test_door_color(self):
        self.assertEqual(Color.BLACK, Globals.DOOR_COLOR)

    def test_room_colors(self):
        expected = {
            RoomType.NORMAL_ROOM: Color.VIOLET,
            RoomType.DEAD_END: Color.VIOLET,
            RoomType.ITEM_ROOM: Color.GREEN,
            RoomType.SHOP_ROOM: Color.YELLOW,
            RoomType.START_ROOM: Color.ORANGE,
            RoomType.BOSS_TELEPORT_ROOM: Color.GRAY,
            RoomType.BOSS_ROOM: Color.RED
            }
        self.assertEqual(expected, Globals.Room_Colors)

    def test_room_width(self):
        self.assertEqual(120, Globals.ROOM_WIDTH)

    def test_room_height(self):
        self.assertEqual(60, Globals.ROOM_HEIGHT)

    def test_floor_height(self):
        self.assertEqual(8, Globals.FLOOR_HEIGHT)

    def test_floor_width(self):
        self.assertEqual(9, Globals.FLOOR_WIDTH)

    def test_base_indent(self):
        self.assertEqual("  ", Globals.BASE_INDENT)

    def test_json_suffix(self):
        self.assertEqual(".json", Globals.JSON_SUFFIX)

    def test_path(self):
        self.assertEqual(os.path.realpath(os.path.dirname(__file__).replace("\\test", "")), Globals.APPLICATION_PATH)


if __name__ == '__main__':
    unittest.main()

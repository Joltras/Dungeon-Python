import os
from enum import Enum


class Direction(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP_RIGHT = (1, -1)
    UP_LEFT = (-1, -1)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (-1, 1)


class DoorFace(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    TOP = 0
    EAST = 1
    BOTTOM = 2
    WEST = 3


class RoomType(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    NORMAL_ROOM = 0
    DEAD_END = 1
    ITEM_ROOM = 2
    SHOP_ROOM = 3
    START_ROOM = 4
    TELEPORT_ROOM = 5
    BOSS_ROOM = 6


class Color(Enum):
    ORANGE = (255, 140, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (150, 150, 150)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)
    YELLOW = (250, 250, 55)
    VIOLET = (148, 0, 211)


DOOR_COLOR = Color.BLACK

# Room constants
MAX_DOOR_AMOUNT: int = 4
ROOM_WIDTH: int = 120
ROOM_HEIGHT: int = 60
Room_Colors = {
    RoomType.NORMAL_ROOM: Color.VIOLET,
    RoomType.DEAD_END: Color.VIOLET,
    RoomType.ITEM_ROOM: Color.GREEN,
    RoomType.SHOP_ROOM: Color.YELLOW,
    RoomType.START_ROOM: Color.ORANGE,
    RoomType.TELEPORT_ROOM: Color.GRAY,
    RoomType.BOSS_ROOM: Color.RED
}
SPECIAL_ROOMS = (RoomType.ITEM_ROOM, RoomType.SHOP_ROOM)

# Json
BASE_INDENT = "  "
JSON_SUFFIX = ".json"
APPLICATION_PATH = os.path.realpath(os.path.dirname(__file__).replace("\\src", ""))

# Floor
# Width and height in number of rooms
FLOOR_WIDTH: int = 9
FLOOR_HEIGHT: int = 8
MAX_ROOMS: int = 15
# Distance between start and boss room
MIN_DISTANCE = 6
x_offset = (FLOOR_WIDTH * ROOM_WIDTH) / 2
y_offset = 0
floor_plan_coordinates = (y_offset, x_offset)

# Window
window_multiplier: float = 2
window_height = FLOOR_HEIGHT * ROOM_HEIGHT * window_multiplier
window_width = FLOOR_WIDTH * ROOM_WIDTH * window_multiplier

LINE_THICKNESS = 5

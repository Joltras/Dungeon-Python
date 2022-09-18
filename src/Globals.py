import os
from enum import Enum

room_width: int = 120
room_height: int = 60

window_multiplier: float = 2

width: int = 9
height: int = 8
MAX_ROOMS: int = 15
MIN_DISTANCE = 4

window_height = height * room_height * window_multiplier
window_width = width * room_width * window_multiplier

floor_plan_coordinates = ((height * room_height) / 2, (width * room_width) / 2)
x_offset = (width * room_width) / 2
y_offset = (height * room_height) / 2

MAX_DOOR_AMOUNT: int = 4
LINE_THICKNESS = 5

APPLICATION_PATH = os.path.realpath(os.path.dirname(__file__).replace("\\src", ""))

class Directions(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP_RIGHT = (1, -1)
    UP_LEFT = (-1, -1)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (-1, 1)


class DoorFace(Enum):
    TOP = 0
    EAST = 1
    BOTTOM = 2
    WEST = 3


class RoomType(Enum):
    NORMAL_ROOM = 0
    DEAD_END = 1
    ITEM_ROOM = 2
    SHOP_ROOM = 3
    START_ROOM = 4
    BOSS_TELEPORT_ROOM = 5
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
Room_Colors = {
    RoomType.NORMAL_ROOM: Color.VIOLET,
    RoomType.DEAD_END: Color.VIOLET,
    RoomType.ITEM_ROOM: Color.GREEN,
    RoomType.SHOP_ROOM: Color.YELLOW,
    RoomType.START_ROOM: Color.ORANGE,
    RoomType.BOSS_TELEPORT_ROOM: Color.GRAY,
    RoomType.BOSS_ROOM: Color.RED
}

SPECIAL_ROOMS = (RoomType.ITEM_ROOM, RoomType.SHOP_ROOM)

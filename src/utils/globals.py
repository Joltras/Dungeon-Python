"""
This file contains all the global constants used in the project.
"""
import os
from enum import Enum
from utils.room_type import RoomType


class DoorFace(Enum):
    """
    Enum for the door faces.
    """

    @classmethod
    def list(cls):
        """
        Returns a list of all the door faces.
        """
        return list(map(lambda c: c.value, cls))

    TOP = 0
    EAST = 1
    BOTTOM = 2
    WEST = 3


class Color(Enum):
    """
    Enum for the colors.
    """

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
    RoomType.BOSS_ROOM: Color.RED,
    RoomType.SECRET_ROOM: Color.LIGHT_GRAY,
}
SPECIAL_ROOMS = (RoomType.ITEM_ROOM, RoomType.SHOP_ROOM)

# Json
BASE_INDENT = "  "
JSON_SUFFIX = ".json"
APPLICATION_PATH = os.path.realpath(
    os.path.dirname(__file__).replace("\\src", "").replace("\\utils", "")
)
DEFAULT_FLOOR_NAME = "floor"
DEFAULT_FLOOR_DIRECTORY = "generation"

# Floor
# Width and height in number of rooms
FLOOR_WIDTH: int = 9
FLOOR_HEIGHT: int = 8
MAX_ROOMS: int = 15
# Distance between start and boss room
X_OFFSET = (FLOOR_WIDTH * ROOM_WIDTH) / 2
Y_OFFSET = 0

# Window
WINDOW_MULTIPLIER: float = 2
WINDOW_HEIGHT = FLOOR_HEIGHT * ROOM_HEIGHT * WINDOW_MULTIPLIER
WINDOW_WIDTH = FLOOR_WIDTH * ROOM_WIDTH * WINDOW_MULTIPLIER

LINE_THICKNESS = 5

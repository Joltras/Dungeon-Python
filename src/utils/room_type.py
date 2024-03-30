"""
This file contains the RoomType enum.
"""

from enum import Enum
from typing import List

from utils.globals import Color


class RoomType(Enum):
    """
    Enum for the room types.
    """

    @classmethod
    def list(cls) -> List[int]:
        """
        Returns a list of all the room types.
        """
        return list(map(lambda c: c.value, cls))

    @classmethod
    def get_all(cls) -> List:
        """
        Returns a list of all the room types.
        """
        return list(cls)

    def is_special(self) -> bool:
        """
        Checks if the room type is special.
        Special rooms are rooms that have a special function.
        Special rooms are:
        - Item room
        - Shop room
        - Boss room
        - Secret room
        @return: True if special otherwise False
        """
        switcher = {
            self.NORMAL_ROOM: False,
            self.DEAD_END: False,
            self.ITEM_ROOM: True,
            self.SHOP_ROOM: True,
            self.START_ROOM: False,
            self.TELEPORT_ROOM: False,
            self.BOSS_ROOM: True,
            self.SECRET_ROOM: True,
        }
        return switcher[self]

    def get_color(self) -> Color:
        """
        Returns the color of the room type.
        @return: color of the room type
        """
        return Room_Colors[self]

    NORMAL_ROOM = 0
    DEAD_END = 1
    ITEM_ROOM = 2
    SHOP_ROOM = 3
    START_ROOM = 4
    TELEPORT_ROOM = 5
    BOSS_ROOM = 6
    SECRET_ROOM = 7


Room_Colors = {
    RoomType.NORMAL_ROOM: Color.LIGHT_GRAY,
    RoomType.DEAD_END: Color.LIGHT_GRAY,
    RoomType.ITEM_ROOM: Color.GREEN,
    RoomType.SHOP_ROOM: Color.YELLOW,
    RoomType.START_ROOM: Color.ORANGE,
    RoomType.TELEPORT_ROOM: Color.VIOLET,
    RoomType.BOSS_ROOM: Color.RED,
    RoomType.SECRET_ROOM: Color.BLUE,
}

Room_Names = {
    RoomType.NORMAL_ROOM: "Normal Room",
    RoomType.DEAD_END: "Dead End",
    RoomType.ITEM_ROOM: "Item Room",
    RoomType.SHOP_ROOM: "Shop Room",
    RoomType.START_ROOM: "Start Room",
    RoomType.TELEPORT_ROOM: "Teleport Room",
    RoomType.BOSS_ROOM: "Boss Room",
    RoomType.SECRET_ROOM: "Secret Room",
}

SPECIAL_ROOMS = (RoomType.ITEM_ROOM, RoomType.SHOP_ROOM)

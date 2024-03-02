"""
Module for the TkinterTeleportRoom class.
"""

from globals import RoomType
import globals as my_globals
from rooms.teleport_room import TeleportRoom
from rooms.tkinter.tkinter_room import TkinterRoom


class TkinterTeleportRoom(TkinterRoom, TeleportRoom):
    """
    Tkinter version of teleport room.
    """
    def __init__(
        self,
        x: int,
        y: int,
        room_id: int,
        teleport_room_id: int,
        width=my_globals.ROOM_WIDTH,
        height=my_globals.ROOM_HEIGHT,
    ):
        """
        Creates a new teleport room with the given values.
        """
        super().__init__(x, y, room_id, RoomType.TELEPORT_ROOM, width, height)
        self._teleport_room_id = teleport_room_id

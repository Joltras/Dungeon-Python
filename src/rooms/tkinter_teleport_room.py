from globals import RoomType
import globals
from rooms.teleport_room import TeleportRoom
from rooms.tkinter_room import TkinterRoom


class TkinterTeleportRoom(TkinterRoom, TeleportRoom):
    def __init__(self, x: int, y: int, room_id: int, teleport_room_id: int,
                 width=globals.ROOM_WIDTH,
                 height=globals.ROOM_HEIGHT):
        super().__init__(x, y, room_id, RoomType.TELEPORT_ROOM, width, height)
        self._teleport_room_id = teleport_room_id
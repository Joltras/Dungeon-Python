import globals
from globals import RoomType
from rooms.pygame_normal_room import PygameNormalRoom
from rooms.teleport_room import TeleportRoom


class PygameTeleportRoom(PygameNormalRoom, TeleportRoom):

    def __init__(self, x: int, y: int, room_id: int, teleport_room_id: int,
                 room_type: RoomType = RoomType.TELEPORT_ROOM,
                 width=globals.ROOM_WIDTH,
                 height=globals.ROOM_HEIGHT):
        super().__init__(x, y, room_id, room_type, width, height)
        self._teleport_room_id = teleport_room_id

import Globals
from Globals import RoomType, Color
from rooms.PygameNormalRoom import PygameNormalRoom


class PygameTeleportRoom(PygameNormalRoom):

    def __init__(self, x: int, y: int, room_id: int, teleport_room_id: int,
                 room_type: RoomType = RoomType.BOSS_TELEPORT_ROOM,
                 width=Globals.room_width,
                 height=Globals.room_height):
        super().__init__(x, y, room_id, room_type, width, height)
        self._teleport_room_id = teleport_room_id

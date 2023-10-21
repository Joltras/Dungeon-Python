import globals
from globals import RoomType
from rooms.pygame.pygame_normal_room import PygameNormalRoom
from rooms.teleport_room import TeleportRoom


class PygameTeleportRoom(PygameNormalRoom, TeleportRoom):

    def __init__(self, x: int, y: int, room_id: int, teleport_room_id: int,
                 width=globals.ROOM_WIDTH,
                 height=globals.ROOM_HEIGHT):
        """
        Creates a new pygame teleport room with the given values
        @param x: x coordinate of the room
        @param y: y coordinate of the room
        @param room_id: id of the linked room
        @param teleport_room_id: id of the teleport room
        @param width: width of the room
        @param height: height of the room
        """
        super().__init__(x, y, room_id, RoomType.TELEPORT_ROOM, width, height)
        self._teleport_room_id = teleport_room_id

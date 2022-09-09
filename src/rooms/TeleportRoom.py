from Globals import RoomType
from rooms.Room import Room


class TeleportRoom(Room):

    def __init__(self, x: int, y: int, room_id: int, teleport_room: int):
        super().__init__(x, y, room_id, RoomType.BOSS_TELEPORT_ROOM)
        self._teleport_room_id = teleport_room

    def get_teleport_room_ide(self):
        return self._teleport_room_id

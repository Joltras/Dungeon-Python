from Globals import RoomType
from rooms.Room import Room


class TeleportRoom(Room):

    def __init__(self, x: int, y: int, room_id: int, teleport_room_id: int):
        """
        Creates a new teleport room with the given values.
        :param x: x position for the room
        :param y: y position of the room
        :param room_id: 
        :param teleport_room_id: id of the room the teleport room is connected to
        """
        super().__init__(x, y, room_id, RoomType.BOSS_TELEPORT_ROOM)
        self._teleport_room_id = teleport_room_id

    def get_teleport_room_ide(self) -> int:
        """
        Returns the id of the room the teleport room is connected to.
        :return: room id
        """
        return self._teleport_room_id

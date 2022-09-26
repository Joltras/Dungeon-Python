from Globals import RoomType
from rooms.Room import Room


class TeleportRoom(Room):

    def __init__(self, x: int, y: int, room_id: int, connected_room_id: int):
        """
        Creates a new teleport room with the given values.
        :param x: x position for the room
        :param y: y position of the room
        :param room_id: 
        :param connected_room_id: id of the room the teleport room is connected to
        """
        super().__init__(x, y, room_id, RoomType.TELEPORT_ROOM)
        self._connected_room = connected_room_id

    def get_connected_room_id(self) -> int:
        """
        Returns the id of the room the teleport room is connected to.
        :return: room id
        """
        return self._connected_room

import json

from Globals import RoomType, DoorFace, MAX_DOOR_AMOUNT


class Room:

    def __init__(self, x: int, y: int, room_id: int, room_type: RoomType):
        self._x: int = x
        self._y: int = y
        self._id: int = room_id
        self._room_type = room_type
        self._doors = []

    def __getitem__(self, index: int) -> int:
        if index < 0 or index > 1:
            raise ValueError(str(index) + "is not a valid index")
        if index == 0:
            return self._x
        if index == 1:
            return self._y

    def __eq__(self, other):
        are_equal = False
        if isinstance(other, Room):
            if other._x == self._x and other._y == self._y and other._room_type == self._room_type and self._id == other._id:
                are_equal = True
        return are_equal

    def __getstate__(self):
        state = dict(self.__dict__)
        doors = []
        for door in self._doors:
            doors.append(door.value)
        state["_doors"] = doors
        state["_room_type"] = self._room_type.value
        return state

    def to_json(self) -> str:
        """
        Creates a json representation of the room object.
        :return: json string
        """
        return json.dumps(self.__getstate__(), sort_keys=True, indent=4)

    def set_type(self, room_type: RoomType) -> None:
        """
        Sets the type of the room.
        :param room_type: type for the room
        """
        self._room_type = room_type

    def get_type(self) -> RoomType:
        """
        Returns the type of the room.
        :return: type
        """
        return self._room_type

    def get_x(self) -> int:
        """
        Returns the x coordinate of the room.
        :return: x coordinate
        """
        return self._x

    def get_y(self) -> int:
        """
        Returns the y coordinate of the room.
        :return: y coordinate
        """
        return self._y

    def get_id(self) -> int:
        """
        Returns the id of a room.
        :return: id
        """
        return self._id

    def set_cord(self, x: int, y: int) -> None:
        """
        Sets the coordinates of a room.
        :param x: new x coordinate
        :param y: new y coordinate
        """
        self._x = x
        self._y = y

    def get_doors(self) -> list:
        """
        Returns a list of all doors
        :return: list of doors
        """
        return self._doors

    def add_door(self, door_face: DoorFace) -> None:
        """
        Adds a door at the given location to the room.
        :param door_face: position to place the door
        """
        if len(self._doors) < MAX_DOOR_AMOUNT:
            self._doors.append(door_face)




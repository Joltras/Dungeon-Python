import globals
from globals import RoomType, DoorFace, MAX_DOOR_AMOUNT


class Room:
    def __init__(self, x: int, y: int, room_id: int, type: RoomType):
        """
        Creates a new room with the given values.
        @param x: x coordinate of the room
        @param y: y coordinate of the room
        @param room_id: id of the room
        @param type: type of the room
        """
        self._x: int = x
        self._y: int = y
        self._id: int = room_id
        self._type = type
        self._doors = []

    def __getitem__(self, index: int) -> int:
        """
        Provides an easier method to access the x and y coordinate of the room.
        If the index is not 0 or 1 the method raises an exception.
        @param index: 0 for x 1 for y
        @return: Returns x if index equals 0 and y if index equals 1
        """
        if index < 0 or index > 1:
            raise ValueError(str(index) + "is not a valid index")
        if index == 0:
            return self._x
        if index == 1:
            return self._y

    def to_json(self, indent: int) -> str:
        """
        Creates a json representation of the room object.
        @param indent: Amount of indentation the json representation should have
        @return: json string
        """
        indent_s: str = globals.BASE_INDENT * indent
        json_string: str = (
            str(globals.BASE_INDENT * (indent - 1)) + "{\n" + indent_s + '"_doors": [\n'
        )
        i = 0
        while i < len(self._doors):
            json_string += indent_s + globals.BASE_INDENT + str(self._doors[i].value)
            if i != len(self._doors) - 1:
                json_string += ",\n"
            i += 1
        json_string += (
            "\n"
            + indent_s
            + "],\n"
            + indent_s
            + '"_id": '
            + str(self._id)
            + ",\n"
            + indent_s
            + '"_type": '
            + str(self._type.value)
            + ",\n"
            + indent_s
            + '"_x": '
            + str(self._x)
            + ",\n"
            + indent_s
            + '"_y": '
            + str(self._y)
            + "\n"
            + str(globals.BASE_INDENT * (indent - 1))
            + "}"
        )
        return json_string

    @classmethod
    def from_dict(cls, json_dict: dict):
        room = Room(
            json_dict["_x"],
            json_dict["_y"],
            json_dict["_id"],
            RoomType(json_dict["_type"]),
        )
        for door in json_dict["_doors"]:
            room._doors.append(DoorFace(door))
        return room

    def set_type(self, room_type: RoomType) -> None:
        """
        Sets the type of the room.
        @param room_type: type for the room
        """
        self._type = room_type

    def get_type(self) -> RoomType:
        """
        Returns the type of the room.
        @return: type
        """
        return self._type

    def get_id(self) -> int:
        """
        Returns the id of a room.
        @return: id
        """
        return self._id

    def set_cord(self, x: int, y: int) -> None:
        """
        Sets the coordinates of a room.
        @param x: new x coordinate
        @param y: new y coordinate
        """
        self._x = x
        self._y = y

    def get_doors(self) -> list:
        """
        Returns a list of all doors
        @return: list of doors
        """
        return self._doors

    def add_door(self, door_face: DoorFace) -> None:
        """
        Adds a door at the given location to the room.
        @param door_face: position to place the door
        """
        if len(self._doors) < MAX_DOOR_AMOUNT:
            self._doors.append(door_face)

    def __eq__(self, other) -> bool:
        """
        Compares two rooms which each other.
        Two rooms are equal if they are at the same coordinates and have the same type.
        @param other: Other object to compare
        @return: True if other is a room and they are equal otherwise false.
        """
        if type(other) is not Room:
            return False
        other_room: Room = other
        return (
            self._x == other_room._x
            and self._y == other_room._y
            and self._type == other_room._type
        )

    def __str__(self) -> str:
        """
        Returns a string representation of a room object.
        @return: String representation
        """
        return self.to_json(0)

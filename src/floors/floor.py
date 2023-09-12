from typing import List, Tuple, TypeVar

import numpy as np

import globals
from globals import RoomType, Direction, DoorFace
from rooms.room import Room
from rooms.teleport_room import TeleportRoom

T = TypeVar('T', bound=Room)


class Floor:
    """
    Objects of this class are representing floors.
    A floor manges the creation of rooms and contains them.
    """

    def __init__(self, height: int, width: int):
        """
        Creates a new floor with the given width and height.
        @param height: height for the floor
        @param width: width for the floor
        """
        self._rooms: List[T] = []
        self._floor_grid = np.zeros((height, width))
        self._width: int = width
        self._height: int = height
        self._room_id: int = 0

    def to_json(self, indent: int):
        """
        Creates a json string for the current room object.
        @return: json string
        """
        indent_s: str = globals.BASE_INDENT * indent
        current_index: int = 0
        max_index: int = len(self._rooms)
        json_string = "{\n" + indent_s + '"_rooms"' + ": ["
        if len(self._rooms) == 0:
            json_string += "]"
        else:
            json_string += "\n"
            for room in self._rooms:
                if current_index < max_index - 1:
                    json_string += room.to_json(indent + 2) + ",\n"
                else:
                    json_string += room.to_json(indent + 2)
                current_index += 1
            json_string += "\n" + indent_s + "]"
        return json_string + "\n}"

    def add_to_floor_grid(self, x: int, y: int) -> None:
        """
        Adds a room to the floor grid at the given location.
        @param x: x coordinate of the room
        @param y: y coordinate of the room
        """
        self._floor_grid[y][x] = 1

    def add_room(self, x: int, y: int, type: RoomType = RoomType.NORMAL_ROOM) -> None:
        """
        Creates and adds a room to the floor.
        @param x: x coordinate of the room
        @param y: y coordinate of the room
        @param type: type of the room (default = normal room)
        """
        self.add_to_floor_grid(x, y)
        self._rooms.append(Room(x=x, y=y, type=type, room_id=self._room_id))
        self._room_id += 1

    def add_room_next_to(self, room: Room, direction: Direction, room_type: RoomType) -> None:
        """
        Creates and adds a room next to a given room.
        @param room: room where the new room is placed next to
        @param direction: direction in which the new room is placed
        @param room_type: type for the room
        """
        if direction == Direction.UP:
            self.add_room(room[0], room[1] - 1, room_type)
        elif direction == Direction.DOWN:
            self.add_room(room[0], room[1] + 1, room_type)
        elif direction == Direction.LEFT:
            self.add_room(room[0] - 1, room[1], room_type)
        elif direction == Direction.RIGHT:
            self.add_room(room[0] + 1, room[1], room_type)
        elif direction == Direction.UP_RIGHT:
            self.add_room(room[0] + 1, room[1] - 1, room_type)
        elif direction == Direction.UP_LEFT:
            self.add_room(room[0] - 1, room[1] - 1, room_type)
        elif direction == Direction.DOWN_RIGHT:
            self.add_room(room[0] + 1, room[1] + 1, room_type)
        elif direction == Direction.DOWN_LEFT:
            self.add_room(room[0] - 1, room[1] + 1, room_type)

    def add_teleport_room(self, room: Room) -> None:
        """
        Creates and adds a new Teleport room to the floor.
        The new teleport room is placed at the position from the given room.
        @param room: Room which is connected to the teleport room.
        """
        t_room = TeleportRoom(x=room[0], y=room[1], room_id=self._room_id, connected_room_id=room.get_id())
        self._rooms.append(t_room)
        self._room_id += 1

    def get_rooms(self) -> List[Room]:
        """
        Returns a list containing all the rooms of the floor.
        @return: rooms
        """
        return self._rooms

    def get_floor_grid(self) -> np.ndarray:
        """
        Returns the floor grid of the floor.
        @return: floor grid
        """
        return self._floor_grid

    def contains_room(self, coordinates: Tuple[int, int]) -> bool:
        """
        Checks if there is a room at the given coordinates.
        @param coordinates: coordinates to check
        @return: true if a there is a room otherwise false
        """
        return self._floor_grid[coordinates[1]][coordinates[0]] == 1

    def add_doors_to_rooms(self) -> None:
        """
        Adds doors to all rooms on the floor.
        """
        for room in self._rooms:
            x = room[0]
            y = room[1]
            if x + 1 < len(self._floor_grid[y]) and self._floor_grid[y][x + 1] == 1:
                room.add_door(DoorFace.EAST)
            if x - 1 >= 0 and self._floor_grid[y][x - 1] == 1:
                room.add_door(DoorFace.WEST)
            if y - 1 >= 0 and self._floor_grid[y - 1][x] == 1:
                room.add_door(DoorFace.TOP)
            if y + 1 < len(self._floor_grid) and self._floor_grid[y + 1][x] == 1:
                room.add_door(DoorFace.BOTTOM)

    def count_neighbours(self, x: int, y: int) -> int:
        """
        Counts how many rooms are next to the room.
        @param x: x coordinate  of the room
        @param y: y coordinate of the room
        @return: number of neighbour rooms
        """
        neighbours = 0
        if y + 1 < len(self._floor_grid):
            neighbours += self._floor_grid[y + 1][x]
        if y - 1 >= 0:
            neighbours += self._floor_grid[y - 1][x]
        if x + 1 < len(self._floor_grid[y]):
            neighbours += self._floor_grid[y][x + 1]
        if x - 1 >= 0:
            neighbours += self._floor_grid[y][x - 1]
        return neighbours

    def is_dead_end(self, x: int, y: int) -> bool:
        """
        Returns if the room at the given coordinates is a dead end.
        @param x: x coordinate
        @param y: y coordinate
        @return: true if the room is a dead end otherwise false
        """
        return self.count_neighbours(x, y) == 1

    def has_no_neighbours(self, x: int, y: int) -> bool:
        """
        Checks if they are zero neighbours at the given location.
        @param x: x pos
        @param y: y pos
        @return: True if the location has zero neighbours otherwise False
        """
        return self.count_neighbours(x, y) == 0

    def is_within_border(self, coordinates: Tuple[int, int]) -> bool:
        """
        Checks if the given coordinates are within the floor.
        @param coordinates: coordinates to check
        @return: True if the coordinates are within the floor otherwise False
        """
        return 0 <= coordinates[0] < self._width and 0 <= coordinates[1] < self._height

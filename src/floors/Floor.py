import numpy as np

from Globals import Color, RoomType, Directions, DoorFace
from rooms.PygameNormalRoom import PygameNormalRoom
from rooms.PygameTeleportRoom import PygameTeleportRoom


class Floor:

    def __init__(self, height: int, width: int):
        self._rooms = []
        self._floor_grid = np.zeros((height, width))
        self._room_id = 0

    def __getstate__(self):
        state = dict(self.__dict__)
        del state['_floor_grid']
        del state['_room_id']
        return state

    def add_to_floor_grid(self, x: int, y: int) -> None:
        """
        Adds a room to the floor grid at the given location.
        :param x: x coordinate of the room
        :param y: y coordinate of the room
        :return:
        """
        self._floor_grid[y][x] = 1

    def add_room(self, x: int, y: int, color: Color = Color.VIOLET, room_type=RoomType.NORMAL_ROOM):
        """
        Creates and adds a room to the floor.
        :param x: x coordinate of the room
        :param y: y coordinate of the room
        :param color: color of the room (default = violet)
        :param room_type: type of the room (default = normal room)
        """
        self._rooms.append(PygameNormalRoom(x=x, y=y, color=color, room_type=room_type, room_id=self._room_id))
        self._room_id += 1

    def add_room_next_to(self, room: PygameNormalRoom, direction: Directions, color: Color, room_type: RoomType) -> None:
        """
        Creates and adds a room next to a given room.
        :param room: room where the new room is placed next to
        :param direction: direction in which the new room is placed
        :param color: color for the room
        :param room_type: type for the room
        """
        if direction == Directions.UP:
            self.add_room(room.get_x(), room.get_y() - 1, color, room_type)
        elif direction == Directions.DOWN:
            self.add_room(room.get_x(), room.get_y() + 1, color, room_type)
        elif direction == Directions.LEFT:
            self.add_room(room.get_x() - 1, room.get_y(), color, room_type)
        elif direction == Directions.RIGHT:
            self.add_room(room.get_x() + 1, room.get_y(), color, room_type)
        elif direction == Directions.UP_RIGHT:
            self.add_room(room.get_x() + 1, room.get_y() - 1, color, room_type)
        elif direction == Directions.UP_LEFT:
            self.add_room(room.get_x() - 1, room.get_y() - 1, color, room_type)
        elif direction == Directions.DOWN_RIGHT:
            self.add_room(room.get_x() + 1, room.get_y() + 1, color, room_type)
        elif direction == Directions.DOWN_LEFT:
            self.add_room(room.get_x() - 1, room.get_y() + 1, color, room_type)

    def add_teleport_room(self, room: PygameNormalRoom, color=Color.DARK_GRAY) -> None:
        """
        Creates and adds a new Teleport room to the floor.
        :param room: Room which is connected to the teleport room.
        :param color: color for the room (default = gray)
        """
        t_room = PygameTeleportRoom(x=room.get_x(), y=room.get_y(), color=color, room_id=self._room_id,
                                    room_type=RoomType.BOSS_TELEPORT_ROOM, teleport_room_id=room.get_id())
        self._rooms.append(t_room)
        self._room_id += 1

    def get_rooms(self) -> list:
        """
        Returns a list containing all the rooms of the floor.
        :return: rooms
        """
        return self._rooms

    def get_floor_grid(self) -> np.ndarray:
        """
        Returns the floor grid of the floor.
        :return: floor grid
        """
        return self._floor_grid

    def contains_room(self, x: int, y: int) -> bool:
        """
        Checks if there is a room at the given coordinates.
        :param x: x coordinate
        :param y: y coordinate
        :return: true if a there is a room otherwise false
        """
        return self._floor_grid[y][x] == 1

    def add_doors_to_rooms(self) -> None:
        """
        Adds doors to all rooms on the floor.
        """
        for room in self._rooms:
            x = room.get_x()
            y = room.get_y()
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
        :param x: x coordinate  of the room
        :param y: y coordinate of the room
        :return: number of neighbour rooms
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
        :param x: x coordinate
        :param y: y coordinate
        :return: true if the room is a dead end otherwise false
        """
        return self.count_neighbours(x, y) == 1

"""
Pygame version of the floor.
This version is used to draw the floor and the rooms on the screen.
"""

import pygame
import globals as my_globals
from globals import Color, RoomType
from floors.floor import Floor
from rooms.pygame.pygame_normal_room import PygameNormalRoom
from rooms.pygame.pygame_teleport_room import PygameTeleportRoom
from rooms.room import Room


class PygameFloor(Floor):
    """
    A pygame version of the floor.
    """

    def __init__(self, height: int, width: int, seed: str):
        """
        Creates a new floor width the given width and height.
        @param height: height of the floor
        @param width: width of the floor
        """
        super().__init__(height, width, seed)
        self._rect = pygame.Rect(
            my_globals.X_OFFSET,
            my_globals.Y_OFFSET,
            width * my_globals.ROOM_WIDTH,
            height * my_globals.ROOM_HEIGHT,
        )

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the floor with all the rooms on the screen.
        @param screen: screen to draw on
        """
        for room in self._rooms:
            room.draw(screen)
        for room in self._rooms:
            room.draw_doors(screen)
        pygame.draw.rect(screen, Color.DARK_GRAY.value, self._rect, 2)

    def add_room(self, x: int, y: int, room_type=RoomType.NORMAL_ROOM):
        """
        Creates and adds a room to the floor.
        @param x: x coordinate of the room
        @param y: y coordinate of the room
        @param room_type: type of the room (default = normal room)
        """
        self.add_to_floor_grid(x, y)
        self._rooms.append(PygameNormalRoom(x=x, y=y, room_type=room_type, room_id=self._room_id))
        self._room_id += 1

    def add_teleport_room(self, room: Room) -> None:
        """
        Creates and adds a new Teleport room to the floor.
        New teleport room is placed at the location from the given room.
        @param room: Room which is connected to the teleport room.
        """
        t_room = PygameTeleportRoom(
            x=room[0], y=room[1], room_id=self._room_id, teleport_room_id=room.get_id()
        )
        self._rooms.append(t_room)
        self._room_id += 1

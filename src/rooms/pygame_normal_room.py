import pygame
import globals
from globals import DoorFace, RoomType
from rooms.room import Room


class PygameNormalRoom(Room):
    """
    Pygame version of room.
    """

    def __init__(self, x: int, y: int, room_id: int, type: RoomType, width=globals.ROOM_WIDTH,
                 height=globals.ROOM_HEIGHT):
        """
        Creates a new room with the given arguments.
        :param x: x coordinate of the room
        :param y: y coordinate of the room
        :param room_id: id of the room
        :param type: type of room
        :param width: room width
        :param height: room height
        """
        super().__init__(x, y, room_id, type)
        self._height = height
        self._width = width
        self._rect = pygame.Rect(self._x * width + globals.x_offset,
                                 self._y * height + globals.y_offset,
                                 width, height)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the room on the screen.
        :param screen: screen to draw on
        """
        color = globals.Room_Colors[self._type]
        pygame.draw.rect(screen, color.value, self._rect)

    def draw_doors(self, screen: pygame.Surface) -> None:
        """
        Draws all the doors of the room on the given screen.
        :param screen: screen to draw on
        """
        door_color = globals.DOOR_COLOR
        for door in self._doors:
            if door == DoorFace.WEST:
                pygame.draw.line(screen, door_color.value,
                                 (self._rect.left, self._rect.top + globals.ROOM_HEIGHT / 4),
                                 (self._rect.left, self._rect.top + globals.ROOM_HEIGHT / 4 * 3),
                                 globals.LINE_THICKNESS)
            elif door == DoorFace.EAST:
                pygame.draw.line(screen, door_color.value,
                                 (self._rect.left + globals.ROOM_WIDTH, self._rect.top + globals.ROOM_HEIGHT / 4),
                                 (self._rect.left + globals.ROOM_WIDTH, self._rect.top + globals.ROOM_HEIGHT / 4 * 3),
                                 globals.LINE_THICKNESS)
            elif door == DoorFace.TOP:
                pygame.draw.line(screen, door_color.value,
                                 (self._rect.left + globals.ROOM_WIDTH / 4, self._rect.top),
                                 (self._rect.left + globals.ROOM_WIDTH / 4 * 3, self._rect.top), globals.LINE_THICKNESS)
            elif door == DoorFace.BOTTOM:
                pygame.draw.line(screen, door_color.value,
                                 (self._rect.left + globals.ROOM_WIDTH / 4, self._rect.top + globals.ROOM_HEIGHT),
                                 (self._rect.left + globals.ROOM_WIDTH / 4 * 3, self._rect.top + globals.ROOM_HEIGHT),
                                 globals.LINE_THICKNESS)

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rectangle of a room.
        :return: rectangle
        """
        return self._rect

    def get_height(self) -> int:
        """
        Returns the height of the room.
        :return: height of the room
        """
        return self._height

    def get_width(self) -> int:
        """
        Returns the width of the room.
        :return: width of the room
        """
        return self._width

    def set_cord(self, x: int, y: int) -> None:
        """
        Sets the coordinates of a room.
        :param x: new x coordinate
        :param y: new y coordinate
        """
        super().set_cord(x, y)
        self._rect = pygame.Rect(self._x * self._width + globals.x_offset,
                                 self._y * self._height + globals.y_offset,
                                 self._width, self._height)

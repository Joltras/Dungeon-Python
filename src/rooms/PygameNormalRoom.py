import json

import pygame

import Globals
from Globals import DoorFace, RoomType
from rooms.Room import Room


class PygameNormalRoom(Room):

    def __init__(self, x: int, y: int, room_id: int, room_type: RoomType, width=Globals.room_width,
                 height=Globals.room_height):
        """
        Creates a new room with the given arguments.
        :param x: x coordinate of the room
        :param y: y coordinate of the room
        :param room_id: id of the room
        :param room_type: type of room
        :param width: room width
        :param height: room height
        """
        super().__init__(x, y, room_id, room_type)
        self._rect = pygame.Rect(self._x * Globals.room_width + Globals.x_offset,
                                 self._y * Globals.room_height + Globals.y_offset,
                                 width, height)

    def __getstate__(self):
        state = dict(self.__dict__)
        del state["_rect"]
        doors = []
        for door in self._doors:
            doors.append(door.value)
        state["_doors"] = doors
        state["_room_type"] = self._room_type.value
        return state

    def toJSON(self) -> str:
        """
        Creates a json string for the room object.
        :return: json string
        """
        json_string = json.dumps(self.__getstate__(), sort_keys=True, indent=4)
        return json_string

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the room on the screen.
        :param screen: screen to draw on
        """
        color = Globals.Room_Colors[self._room_type]
        pygame.draw.rect(screen, color.value, self._rect)

    def draw_doors(self, screen: pygame.Surface) -> None:
        """
        Draws all the doors of the room on the given screen.
        :param screen: screen to draw on
        """
        door_color = Globals.DOOR_COLOR
        for door in self._doors:
            if door == DoorFace.WEST:
                pygame.draw.line(screen, door_color.value,
                                 (self._rect.left, self._rect.top + Globals.room_height / 4),
                                 (self._rect.left, self._rect.top + Globals.room_height / 4 * 3),
                                 Globals.LINE_THICKNESS)
            elif door == DoorFace.EAST:
                pygame.draw.line(screen, door_color.value,
                                 (self._rect.left + Globals.room_width, self._rect.top + Globals.room_height / 4),
                                 (self._rect.left + Globals.room_width, self._rect.top + Globals.room_height / 4 * 3),
                                 Globals.LINE_THICKNESS)
            elif door == DoorFace.TOP:
                pygame.draw.line(screen, door_color.value,
                                 (self._rect.left + Globals.room_width / 4, self._rect.top),
                                 (self._rect.left + Globals.room_width / 4 * 3, self._rect.top), Globals.LINE_THICKNESS)
            elif door == DoorFace.BOTTOM:
                pygame.draw.line(screen, door_color.value,
                                 (self._rect.left + Globals.room_width / 4, self._rect.top + Globals.room_height),
                                 (self._rect.left + Globals.room_width / 4 * 3, self._rect.top + Globals.room_height),
                                 Globals.LINE_THICKNESS)

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rectangle of a room.
        :return: rectangle
        """
        return self._rect

    def set_cord(self, x: int, y: int) -> None:
        """
        Sets the coordinates of a room.
        :param x: new x coordinate
        :param y: new y coordinate
        """
        self._x = x
        self._y = y
        self._rect = pygame.Rect(self._x * Globals.room_width + Globals.floor_plan_coordinates[1],
                                 self._y * Globals.room_height + Globals.floor_plan_coordinates[0],
                                 Globals.room_width, Globals.room_height)

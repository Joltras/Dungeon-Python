import json

import pygame
from Globals import Color, DoorFace, RoomType
import Globals

MAX_DOOR_AMOUNT: int = 4
LINE_THICKNESS = 5
DOOR_COLOR = Color.BLACK.value


class Room:

    def __init__(self, x: int, y: int, color: Color, room_id: int, room_type: RoomType, width=Globals.room_width,
                 height=Globals.room_height):
        """
        Creates a new room with the given arguments.
        :param x: x coordinate of the room
        :param y: y coordinate of the room
        :param color: color for the room
        :param room_id: id of the room
        :param room_type: type of room
        :param width: room width
        :param height: room height
        """
        self.__x: int = x
        self.__y: int = y
        self.room_type = room_type
        self.color = color
        self.doors = []
        self.rect = pygame.Rect(self.__x * Globals.room_width + Globals.floor_plan_coordinates[1],
                                self.__y * Globals.room_height + Globals.floor_plan_coordinates[0],
                                width, height)
        self.__id = room_id

    def __getstate__(self):
        state = dict(self.__dict__)
        del state["color"]
        del state["rect"]
        doors = []
        for door in self.doors:
            doors.append(door.value)
        state["doors"] = doors
        state["room_type"] = self.room_type.value
        print(state)
        return state

    def toJSON(self) -> str:
        """
        Creates a json string for the room object.
        :return: json string
        """
        return json.dumps(self.__getstate__(), sort_keys=True, indent=4)

    def add_door(self, door_face: DoorFace) -> None:
        """
        Adds a door to the given side of the room to the room.
        :param door_face: Side where the door is placed
        """
        if len(self.doors) < MAX_DOOR_AMOUNT:
            self.doors.append(door_face)

    def set_type(self, room_type: RoomType) -> None:
        """
        Sets the type of the room.
        :param room_type: type for the room
        """
        self.room_type = room_type

    def get_type(self):
        return self.room_type

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the room on the screen.
        :param screen: screen to draw on
        """
        pygame.draw.rect(screen, self.color.value, self.rect)

    def draw_doors(self, screen: pygame.Surface) -> None:
        """
        Draws all the doors of the room on the given screen.
        :param screen: screen to draw on
        """
        for door in self.doors:
            if door == DoorFace.WEST:
                pygame.draw.line(screen, DOOR_COLOR,
                                 (self.rect.left, self.rect.top + Globals.room_height / 4),
                                 (self.rect.left, self.rect.top + Globals.room_height / 4 * 3), LINE_THICKNESS)
            elif door == DoorFace.EAST:
                pygame.draw.line(screen, DOOR_COLOR,
                                 (self.rect.left + Globals.room_width, self.rect.top + Globals.room_height / 4),
                                 (self.rect.left + Globals.room_width, self.rect.top + Globals.room_height / 4 * 3),
                                 LINE_THICKNESS)
            elif door == DoorFace.TOP:
                pygame.draw.line(screen, DOOR_COLOR,
                                 (self.rect.left + Globals.room_width / 4, self.rect.top),
                                 (self.rect.left + Globals.room_width / 4 * 3, self.rect.top), LINE_THICKNESS)
            elif door == DoorFace.BOTTOM:
                pygame.draw.line(screen, DOOR_COLOR,
                                 (self.rect.left + Globals.room_width / 4, self.rect.top + Globals.room_height),
                                 (self.rect.left + Globals.room_width / 4 * 3, self.rect.top + Globals.room_height),
                                 LINE_THICKNESS)

    def get_x(self) -> int:
        """
        Returns the x coordinate of the room.
        :return: x coordinate
        """
        return self.__x

    def get_y(self) -> int:
        """
        Returns the y coordinate of the room.
        :return: y coordinate
        """
        return self.__y

    def get_color(self) -> Color:
        """
        Returns the color of a room.
        :return: color
        """
        return self.color

    def set_color(self, color: Color) -> None:
        """
        Sets the color of a room.
        :param color: new color for the room
        """
        self.color = color

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rectangle of a room.
        :return: rectangle
        """
        return self.rect

    def get_id(self) -> int:
        """
        Returns the id of a room.
        :return: id
        """
        return self.__id

    def set_cord(self, x: int, y: int) -> None:
        """
        Sets the coordinates of a room.
        :param x: new x coordinate
        :param y: new y coordinate
        """
        self.__x = x
        self.__y = y
        self.rect = pygame.Rect(self.__x * Globals.room_width + Globals.floor_plan_coordinates[1],
                                self.__y * Globals.room_height + Globals.floor_plan_coordinates[0],
                                Globals.room_width, Globals.room_height)


class TeleportRoom(Room):

    def __init__(self, x: int, y: int, room_id: int, teleport_room_id:int,  color: Color = Color.GRAY,
                 room_type: RoomType = RoomType.BOSS_TELEPORT_ROOM,
                 width=Globals.room_width,
                 height=Globals.room_height):
        super().__init__(x, y, color, room_id, room_type, width, height)
        self.t_id = teleport_room_id

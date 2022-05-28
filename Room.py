import json

import pygame
from Globals import Color, DoorFace, RoomType
import Globals
import numpy as np

MAX_DOOR_AMOUNT: int = 4
LINE_THICKNESS = 5
DOOR_COLOR = Color.BLACK.value


class Room:

    def __init__(self, x: int, y: int, color: Color, room_id: int, room_type: RoomType, width=Globals.room_width,
                 height=Globals.room_height):
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

    def toJSON(self):
        return json.dumps(self.__getstate__(), sort_keys=True, indent=4)

    def add_door(self, door_face: DoorFace):
        if len(self.doors) < MAX_DOOR_AMOUNT:
            self.doors.append(door_face)

    def set_type(self, room_type: RoomType):
        self.room_type = room_type

    def get_type(self):
        return self.room_type

    def draw(self, screen):
        pygame.draw.rect(screen, self.color.value, self.rect)

    def draw_doors(self, screen):
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
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def get_color(self):
        return self.color

    def set_color(self, color: Color) -> None:
        self.color = color

    def get_rect(self):
        return self.rect

    def get_id(self) -> int:
        return self.__id

    def set_cord(self, x: int, y: int) -> None:
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

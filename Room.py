import pygame
from Globals import Color, DoorFace, RoomType
import Globals
import numpy as np

MAX_DOOR_AMOUNT: int = 4
LINE_THICKNESS = 5
DOOR_COLOR = Color.BLACK.value


class Room:
    def __init__(self, x: int, y: int, color: Color, room_type, width=Globals.room_width, height=Globals.room_height):
        self.__x: int = x
        self.__y: int = y
        self.__room_type = room_type
        self.__color = color
        self.__doors = []
        self.__rect = pygame.Rect(self.__x * Globals.room_width + Globals.floor_plan_coordinates[1],
                                  self.__y * Globals.room_height + Globals.floor_plan_coordinates[0],
                                  width, height)

    def add_door(self, door_face: DoorFace):
        if len(self.__doors) < MAX_DOOR_AMOUNT:
            self.__doors.append(door_face)

    def set_type(self, room_type: RoomType):
        self.__room_type = room_type

    def get_type(self):
        return self.__room_type

    def draw(self, screen):
        pygame.draw.rect(screen, self.__color.value, self.__rect)

    def draw_doors(self, screen):
        for door in self.__doors:
            if door == DoorFace.LEFT:
                pygame.draw.line(screen, DOOR_COLOR,
                                 (self.__rect.left, self.__rect.top + Globals.room_height / 4),
                                 (self.__rect.left, self.__rect.top + Globals.room_height / 4 * 3), LINE_THICKNESS)
            elif door == DoorFace.RIGHT:
                pygame.draw.line(screen, DOOR_COLOR,
                                 (self.__rect.left + Globals.room_width, self.__rect.top + Globals.room_height / 4),
                                 (self.__rect.left + Globals.room_width, self.__rect.top + Globals.room_height / 4 * 3), LINE_THICKNESS)
            elif door == DoorFace.UP:
                pygame.draw.line(screen, DOOR_COLOR,
                                 (self.__rect.left + Globals.room_width / 4, self.__rect.top),
                                 (self.__rect.left + Globals.room_width / 4 * 3, self.__rect.top), LINE_THICKNESS)
            elif door == DoorFace.DOWN:
                pygame.draw.line(screen, DOOR_COLOR,
                                 (self.__rect.left + Globals.room_width / 4, self.__rect.top + Globals.room_height),
                                 (self.__rect.left + Globals.room_width / 4 * 3, self.__rect.top + Globals.room_height), LINE_THICKNESS)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_color(self):
        return self.__color

    def set_color(self, color: Color):
        self.__color = color

    def get_rect(self):
        return self.__rect

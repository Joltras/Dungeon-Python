import pygame
from Globals import Color, DoorFace, RoomTypes
import Globals
import numpy as np

MAX_DOOR_AMOUNT: int = 4

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

    def draw(self, screen):
        pygame.draw.rect(screen, self.__color.value, self.__rect)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_color(self):
        return self.__color

    def get_rect(self):
        return self.__rect




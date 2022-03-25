import pygame
import Globals
from Globals import Color
from Room import Room
import numpy as np


class Floor:

    def __init__(self, height: int, width: int):
        self.__height = height
        self.__width = width
        self.__rooms: list = []
        self.__floor = np.zeros((height, width))
        self.__rect = pygame.Rect(Globals.floor_plan_coordinates[1], Globals.floor_plan_coordinates[0], width * Globals.room_width, height * Globals.room_height)

    def draw(self, screen):
        for room in self.__rooms:
            room.draw(screen)
        pygame.draw.rect(screen, Color.DARK_GRAY.value, self.__rect, 2)

    def add_room(self, x, y, color: Color = Color.VIOLET):
        self.__floor[y][x] = 1
        self.__rooms.append(Room(x, y, color))

    def get_rooms(self):
        return self.__rooms

    def contains_room(self, x, y):
        return self.__floor[y][x] == 1

    def count_neighbours(self, x, y):
        neighbours = 0
        if y + 1 < len(self.__floor):
            neighbours += self.__floor[y + 1][x]
        if y - 1 > 0:
            neighbours += self.__floor[y - 1][x]
        if x + 1 < len(self.__floor):
            neighbours += self.__floor[y][x + 1]
        if x - 1 > 0:
            neighbours += self.__floor[y][x - 1]
        return neighbours

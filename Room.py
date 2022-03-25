import pygame
from Globals import Color
import Globals


class Room:
    def __init__(self, x: int, y: int, color: Color):
        self.__x: int = x
        self.__y: int = y
        self.__color = color
        self.__rect = pygame.Rect(self.__x * Globals.room_width + Globals.floor_plan_coordinates[1], self.__y * Globals.room_height + Globals.floor_plan_coordinates[0], Globals.room_width, Globals.room_height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.__color.value, self.__rect)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

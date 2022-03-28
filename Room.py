import pygame
from Globals import Color
import Globals


class Room:
    def __init__(self, x: int, y: int, color: Color, width=Globals.room_width, height=Globals.room_height):
        self.__x: int = x
        self.__y: int = y
        self.__color = color
        self.__rect = pygame.Rect(self.__x * Globals.room_width + Globals.floor_plan_coordinates[1],
                                  self.__y * Globals.room_height + Globals.floor_plan_coordinates[0],
                                  width, height)

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




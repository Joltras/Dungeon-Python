import pygame
from Pygame.Snake.Enums import Color
import Globals


class Room:
    def __init__(self, x: int, y: int):
        self.__x: int = x
        self.__y: int = y
        self.__rect = pygame.Rect(self.__x * Globals.width, self.__y * Globals.height, Globals.width, Globals.height)

    def draw(self, screen):
        pygame.draw.rect(screen, Color.VIOLET.value, self.__rect, 2)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

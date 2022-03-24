import random
from enum import Enum

import numpy as np

import Globals
from Pygame.Snake.Enums import Color
from Floor import Floor
import pygame

number_of_rooms: int = 10
width: int = 9
height: int = 8
screen = pygame.display.set_mode((width * Globals.width * 2, height * Globals.height * 2))
clock = pygame.time.Clock()
floor = Floor(height, width)


def run():
    active: bool = True
    floor.add_room(random.randint(0, 8), random.randint(0, 7))
    number_of_current_rooms = 1
    while number_of_current_rooms < number_of_rooms:
        for room in floor.get_rooms():
            if room.get_y() - 1 > 0:
                if not floor.contains_room(room.get_x(), room.get_y() - 1) and (
                        floor.count_neighbours(room.get_x(), room.get_y() - 1) <= 1):
                    floor.add_room(room.get_x(), room.get_y() - 1)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

            if room.get_y() + 1 < height:
                if not floor.contains_room(room.get_x(), room.get_y() + 1) and floor.count_neighbours(room.get_x(),
                                                                                                      room.get_y() + 1) <= 1:
                    floor.add_room(room.get_x(), room.get_y() + 1)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

            if room.get_x() + 1 < width:
                if not floor.contains_room(room.get_x() + 1, room.get_y()) and floor.count_neighbours(room.get_x() + 1,
                                                                                                      room.get_y()) <= 1:
                    floor.add_room(room.get_x() + 1, room.get_y())
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

            if room.get_x() - 1 > 0:
                if not floor.contains_room(room.get_x() - 1, room.get_y()) and floor.count_neighbours(room.get_x() - 1,
                                                                                                      room.get_y()) <= 1:
                    floor.add_room(room.get_x() - 1, room.get_y())
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
        screen.fill(Color.WHITE.value)
        floor.draw(screen)
        pygame.display.flip()
        clock.tick(5)


run()

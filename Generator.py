import math
import random
import sys
from enum import Enum

import numpy as np

import Globals
from Globals import Color
from Floor import Floor
import pygame

number_of_rooms: int
max_rooms: int = 15
stage_id = 2

screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
clock = pygame.time.Clock()
floor: Floor


def get_room_amount(stage_id: int) -> int:
    if stage_id == -1:
        stage_id = 1
    return min(max_rooms, int(random.randint(0, 1) + 5 + math.floor(stage_id * 10) / 3.0))


def generate():
    global number_of_rooms
    global floor
    number_of_rooms = get_room_amount(stage_id)
    print(number_of_rooms)
    floor = Floor(Globals.height, Globals.width)
    floor.add_room(random.randint(0, 8), random.randint(0, 7), Color.ORANGE)
    number_of_current_rooms = 1
    while number_of_current_rooms < number_of_rooms:
        for room in floor.get_rooms():
            if room.get_y() - 1 > 0:
                if not floor.contains_room(room.get_x(), room.get_y() - 1) and (
                        floor.count_neighbours(room.get_x(), room.get_y() - 1) <= 1):
                    if random.randint(1, 2) == 2:
                        floor.add_room(room.get_x(), room.get_y() - 1)
                        number_of_current_rooms += 1
                        if number_of_rooms == number_of_current_rooms:
                            break

            if room.get_y() + 1 < Globals.height:
                if not floor.contains_room(room.get_x(), room.get_y() + 1) and floor.count_neighbours(room.get_x(),
                                                                                                      room.get_y() + 1) <= 1:
                    if random.randint(1, 2) == 2:
                        floor.add_room(room.get_x(), room.get_y() + 1)
                        number_of_current_rooms += 1
                        if number_of_rooms == number_of_current_rooms:
                            break

            if room.get_x() + 1 < Globals.width:
                if not floor.contains_room(room.get_x() + 1, room.get_y()) and floor.count_neighbours(room.get_x() + 1,
                                                                                                      room.get_y()) <= 1:
                    if random.randint(1, 2) == 2:
                        floor.add_room(room.get_x() + 1, room.get_y())
                        number_of_current_rooms += 1
                        if number_of_rooms == number_of_current_rooms:
                            break

            if room.get_x() - 1 > 0:
                if not floor.contains_room(room.get_x() - 1, room.get_y()) and floor.count_neighbours(room.get_x() - 1,
                                                                                                      room.get_y()) <= 1:
                    if random.randint(1, 2) == 2:
                        floor.add_room(room.get_x() - 1, room.get_y())
                        number_of_current_rooms += 1
                        if number_of_rooms == number_of_current_rooms:
                            break


def run():
    active: bool = True
    generate()
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                generate()
        screen.fill(Color.WHITE.value)
        floor.draw(screen)
        pygame.display.flip()
        clock.tick(5)

if __name__ == "__main__":
    if(len(sys.argv[1:]) < 1):
        seed = None
    else:
        seed = sys.argv[1]
    random.seed(seed)
    run()

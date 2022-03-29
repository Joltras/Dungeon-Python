import math
import random
import Globals
from Globals import Color
from Floor import Floor
import pygame
from collections import deque

MAX_ROOMS: int = 15


class Generator:
    def __init__(self):
        self.__clock = pygame.display.set_mode((Globals.window_width, Globals.window_height))
        self.__floor: Floor = None
        self.__screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
        self.__clock = pygame.time.Clock()
        self.__stage_id = 2
        self.__number_of_rooms: int

    def get_room_amount(self) -> int:
        if self.__stage_id == -1:
            self.__stage_id = 1
        return min(MAX_ROOMS, int(random.randint(0, 1) + 5 + math.floor(self.__stage_id * 10) / 3.0))

    def generate(self):
        number_of_rooms = self.get_room_amount()
        print(number_of_rooms)
        self.__floor = Floor(Globals.height, Globals.width)
        start_room: tuple = (random.randint(0, 8), random.randint(0, 7))
        self.__floor.add_room(start_room[0], start_room[1], Color.ORANGE, 5)
        self.__floor.add_to_floor_grid(start_room[0], start_room[1])
        number_of_current_rooms = 1
        room_queue: deque = deque([])
        room_queue.append(start_room)

        while number_of_current_rooms < number_of_rooms:

            while number_of_current_rooms < number_of_rooms:
                room = room_queue.pop()
                room_queue.appendleft(room)
                if room[1] - 1 > 0:
                    if not self.__floor.contains_room(room[0], room[1] - 1) and (
                            self.__floor.count_neighbours(room[0], room[1] - 1) <= 1):
                        if random.randint(1, 2) == 2:
                            room_queue.append((room[0], room[1] - 1))
                            self.__floor.add_to_floor_grid(room[0], room[1] - 1)
                            number_of_current_rooms += 1
                            if number_of_rooms == number_of_current_rooms:
                                break

                if room[1] + 1 < Globals.height:
                    if not self.__floor.contains_room(room[0], room[1] + 1) and self.__floor.count_neighbours(room[0],
                                                                                                              room[
                                                                                                                  1] + 1) <= 1:
                        if random.randint(1, 2) == 2:
                            room_queue.append((room[0], room[1] + 1))
                            self.__floor.add_to_floor_grid(room[0], room[1] + 1)
                            number_of_current_rooms += 1
                            if number_of_rooms == number_of_current_rooms:
                                break

                if room[0] + 1 < Globals.width:
                    if not self.__floor.contains_room(room[0] + 1, room[1]) and self.__floor.count_neighbours(
                            room[0] + 1,
                            room[1]) <= 1:
                        if random.randint(1, 2) == 2:
                            room_queue.append((room[0] + 1, room[1]))
                            self.__floor.add_to_floor_grid(room[0] + 1, room[1])
                            number_of_current_rooms += 1
                            if number_of_rooms == number_of_current_rooms:
                                break

                if room[0] - 1 > 0:
                    if not self.__floor.contains_room(room[0] - 1, room[1]) and self.__floor.count_neighbours(
                            room[0] - 1,
                            room[1]) <= 1:
                        if random.randint(1, 2) == 2:
                            room_queue.append((room[0] - 1, room[1]))
                            self.__floor.add_to_floor_grid(room[0] - 1, room[1])
                            number_of_current_rooms += 1
                            if number_of_rooms == number_of_current_rooms:
                                break
        room_queue.remove(start_room)
        while len(room_queue) > 0:
            room = room_queue.pop()
            self.__floor.add_room(room[0], room[1])

        print(self.__floor.get_floor())

    def run(self):
        active: bool = True
        self.generate()
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.generate()
            self.__screen.fill(Color.WHITE.value)
            self.__floor.draw(self.__screen)
            pygame.display.flip()
            self.__clock.tick(5)

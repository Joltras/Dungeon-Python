import math
import random
import Globals
from Globals import Color, RoomType
from Floor import Floor
import pygame
from collections import deque

MAX_ROOMS: int = 15
NORMAL_ROOM_COLOR = Color.VIOLET
START_ROOM_COLOR = Color.ORANGE
BOSS_ROOM_COLOR = Color.RED
ITEM_ROOM_COLOR = Color.GREEN
SPECIAL_ROOMS = (RoomType.BOSS_ROOM, RoomType.ITEM_ROOM)


class Generator:
    def __init__(self, seed):
        self.__clock = pygame.display.set_mode((Globals.window_width, Globals.window_height))
        self.__floor: Floor = None
        self.__screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
        self.__clock = pygame.time.Clock()
        self.__stage_id = 2
        self.__number_of_rooms: int
        self.__seed = seed
        random.seed(seed)

    def get_room_amount(self) -> int:
        if self.__stage_id == -1:
            self.__stage_id = 1
        return min(MAX_ROOMS, int(random.randint(0, 1) + 5 + math.floor(self.__stage_id * 10) / 3.0))

    def generate(self):
        number_of_rooms = self.get_room_amount()
        print(number_of_rooms)
        self.__floor = Floor(Globals.height, Globals.width)
        start_room: tuple = (random.randint(0, 8), random.randint(0, 7))
        self.__floor.add_room(start_room[0], start_room[1], START_ROOM_COLOR, RoomType.START_ROOM)
        self.__floor.add_to_floor_grid(start_room[0], start_room[1])
        number_of_current_rooms = 1
        room_queue: deque = deque([])
        room_queue.append(start_room)

        while number_of_current_rooms < number_of_rooms:

            while number_of_current_rooms < number_of_rooms:
                room = room_queue.pop()
                room_queue.appendleft(room)
                if room[1] - 1 >= 0:
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

                if room[0] - 1 >= 0:
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
            self.__floor.add_room(room[0], room[1], NORMAL_ROOM_COLOR)

        dead_ends = self.mark_dead_ends()
        self.add_special_rooms(dead_ends)
        self.__floor.add_doors_to_rooms()

        print(self.__floor.get_floor())

    def mark_dead_ends(self):
        dead_end_index = ()
        i = 0
        while i < len(self.__floor.get_rooms()):
            room = self.__floor.get_rooms()[i]
            if self.__floor.is_dead_end(room.get_x(), room.get_y()):
                if not room.get_type() == RoomType.START_ROOM:
                    room.set_type(RoomType.DEAD_END)
                    dead_end_index += (i,)
            i += 1
        return dead_end_index

    def add_special_rooms(self, dead_ends):
        i = 0
        while i < len(SPECIAL_ROOMS) and i < len(dead_ends):
            self.__floor.get_rooms()[dead_ends[i]].set_type = SPECIAL_ROOMS[i]
            if SPECIAL_ROOMS[i] == RoomType.BOSS_ROOM:
                self.__floor.get_rooms()[dead_ends[i]].set_color(BOSS_ROOM_COLOR)
            elif SPECIAL_ROOMS[i] == RoomType.ITEM_ROOM:
                self.__floor.get_rooms()[dead_ends[i]].set_color(ITEM_ROOM_COLOR)
            i += 1

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

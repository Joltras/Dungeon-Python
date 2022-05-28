import math
import random
import Globals
from Globals import Color, RoomType, Directions
from Floor import Floor
import pygame
from Room import Room
from collections import deque

MAX_ROOMS: int = 15
NORMAL_ROOM_COLOR = Color.VIOLET
START_ROOM_COLOR = Color.ORANGE
BOSS_ROOM_COLOR = Color.RED
ITEM_ROOM_COLOR = Color.GREEN
SHOP_ROOM_COLOR = Color.YELLOW
TELEPORT_ROOM_COLOR = Color.GRAY
SPECIAL_ROOMS = (RoomType.ITEM_ROOM, RoomType.SHOP_ROOM)
MIN_DISTANCE = 4


class Generator:
    def __init__(self, seed):
        self.floor: Floor = None
        self.screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
        self.clock = pygame.time.Clock()
        self.__stage_id = 2
        self.__number_of_rooms: int
        self.__seed = seed
        random.seed(seed)

    def toJSON(self):
        j = "{\n" + '"seed": "' + self.__seed + '",\n' + '"width": ' + str(Globals.width) + ',\n"height": ' + \
            str(Globals.height) + ',\n"floor": ' + self.floor.toJSON() + "\n}"
        return j

    def get_room_amount(self) -> int:
        """
        Calculates the room amount.
        :return: room amount
        """
        if self.__stage_id == -1:
            self.__stage_id = 1
        return min(MAX_ROOMS, int(random.randint(0, 1) + 5 + math.floor(self.__stage_id * 10) / 3.0))

    def generate(self):
        number_of_rooms = self.get_room_amount()
        print(number_of_rooms)
        self.floor = Floor(Globals.height, Globals.width)
        start_room: tuple = (random.randint(0, 8), random.randint(0, 7))
        self.floor.add_room(start_room[0], start_room[1], START_ROOM_COLOR, RoomType.START_ROOM)
        self.floor.add_to_floor_grid(start_room[0], start_room[1])
        number_of_current_rooms = 1
        room_queue: deque = deque([])
        room_queue.append(start_room)

        while number_of_current_rooms < number_of_rooms:

            while number_of_current_rooms < number_of_rooms:
                room = room_queue.pop()
                room_queue.appendleft(room)
                if room[1] - 1 >= 0:
                    if not self.floor.contains_room(room[0], room[1] - 1) and (
                            self.floor.count_neighbours(room[0], room[1] - 1) <= 1):
                        if random.randint(1, 2) == 2:
                            room_queue.append((room[0], room[1] - 1))
                            self.floor.add_to_floor_grid(room[0], room[1] - 1)
                            number_of_current_rooms += 1
                            if number_of_rooms == number_of_current_rooms:
                                break

                if room[1] + 1 < Globals.height:
                    if not self.floor.contains_room(room[0], room[1] + 1) and self.floor.count_neighbours(room[0],
                                                                                                          room[
                                                                                                              1] + 1) <= 1:
                        if random.randint(1, 2) == 2:
                            room_queue.append((room[0], room[1] + 1))
                            self.floor.add_to_floor_grid(room[0], room[1] + 1)
                            number_of_current_rooms += 1
                            if number_of_rooms == number_of_current_rooms:
                                break

                if room[0] + 1 < Globals.width:
                    if not self.floor.contains_room(room[0] + 1, room[1]) and self.floor.count_neighbours(
                            room[0] + 1,
                            room[1]) <= 1:
                        if random.randint(1, 2) == 2:
                            room_queue.append((room[0] + 1, room[1]))
                            self.floor.add_to_floor_grid(room[0] + 1, room[1])
                            number_of_current_rooms += 1
                            if number_of_rooms == number_of_current_rooms:
                                break

                if room[0] - 1 >= 0:
                    if not self.floor.contains_room(room[0] - 1, room[1]) and self.floor.count_neighbours(
                            room[0] - 1,
                            room[1]) <= 1:
                        if random.randint(1, 2) == 2:
                            room_queue.append((room[0] - 1, room[1]))
                            self.floor.add_to_floor_grid(room[0] - 1, room[1])
                            number_of_current_rooms += 1
                            if number_of_rooms == number_of_current_rooms:
                                break
        room_queue.remove(start_room)
        while len(room_queue) > 0:
            room = room_queue.pop()
            self.floor.add_room(room[0], room[1], NORMAL_ROOM_COLOR)

        dead_ends = self.mark_dead_ends()
        self.add_boss_room(dead_ends, start_room)
        self.add_special_rooms(dead_ends)
        self.floor.add_doors_to_rooms()

        print(self.floor.get_floor())

    def mark_dead_ends(self) -> list:
        """
        Searches for dead ends in the floor and marks them ands returns their indices in a list.
        :return: indices of all dead ends
        """
        dead_end_indices = []
        i = 0
        while i < len(self.floor.get_rooms()):
            room = self.floor.get_rooms()[i]
            if self.floor.is_dead_end(room.get_x(), room.get_y()):
                if not (room.get_type() == RoomType.START_ROOM):
                    room.set_type(RoomType.DEAD_END)
                    dead_end_indices += (i,)
            i += 1
        return dead_end_indices

    def add_boss_room(self, dead_end_indices: list, start_room: tuple) -> None:
        """
        Marks a room as the boss room depending on the location of the start room.
        :param dead_end_indices: indices for all dead ends
        :param start_room: coordinates of the start room in a tuple
        """
        boss_room: Room = None
        boss_room_index: int = None
        boss_room_x: int
        boss_room_y: int
        possible_locations: list = []

        for index in dead_end_indices:
            dead_end = self.floor.get_rooms()[index]
            if (abs(start_room[0] - dead_end.get_x()) >= MIN_DISTANCE) and (
                    abs(start_room[1] - dead_end.get_y()) >= MIN_DISTANCE):
                boss_room = dead_end
                boss_room_index = index
        if boss_room is None:
            boss_room = self.floor.get_rooms()[dead_end_indices[0]]
            boss_room_index = dead_end_indices[0]

        boss_room_x = boss_room.get_x()
        boss_room_y = boss_room.get_y()
        if (boss_room_x + 1 < Globals.width) and (
                self.floor.count_neighbours(boss_room_x + 1, boss_room_y) == 1) and not (
                self.floor.contains_room(boss_room_x + 1, boss_room_y)):
            possible_locations.append(Directions.RIGHT)

        if (boss_room_x - 1 >= 0) and (self.floor.count_neighbours(boss_room_x - 1, boss_room_y) == 1) and \
                not (self.floor.contains_room(boss_room_x - 1, boss_room_y)):
            possible_locations.append(Directions.LEFT)

        if (boss_room_y + 1 < Globals.height) and (self.floor.count_neighbours(boss_room_x, boss_room_y + 1) == 1) and \
                not (self.floor.contains_room(boss_room_x, boss_room_y + 1)):
            possible_locations.append(Directions.DOWN)

        if (boss_room_y - 1 >= 0) and (self.floor.count_neighbours(boss_room_x, boss_room_y - 1) == 1) and \
                not (self.floor.contains_room(boss_room_x, boss_room_y - 1)):
            possible_locations.append(Directions.UP)

        if len(possible_locations) == 0:
            self.floor.add_teleport_room(boss_room)
            if not (self.floor.contains_room(0, 0)):
                boss_room.set_cord(0, 0)
            elif not (self.floor.contains_room(0, Globals.height - 1)):
                boss_room.set_cord(0, Globals.height - 1)
            elif not (self.floor.contains_room(Globals.width - 1, Globals.height - 1)):
                boss_room.set_cord(Globals.width - 1, Globals.height - 1)
            elif not (self.floor.contains_room(Globals.width - 1, 0)):
                boss_room.set_cord(Globals.width - 1, 0)

        elif len(possible_locations) >= 2:
            if possible_locations.__contains__(Directions.UP) and \
                    (possible_locations.__contains__(Directions.LEFT) or possible_locations.__contains__(Directions.RIGHT)):
                self.floor.add_room_next_to(boss_room, Directions.UP, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)


                if possible_locations.__contains__(Directions.LEFT):
                    self.floor.add_room_next_to(boss_room, Directions.LEFT, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)
                    self.floor.add_room_next_to(boss_room, Directions.UP_LEFT, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)

                elif possible_locations.__contains__(Directions.RIGHT):
                    self.floor.add_room_next_to(boss_room, Directions.RIGHT, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)
                    self.floor.add_room_next_to(boss_room, Directions.UP_RIGHT, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)

            elif possible_locations.__contains__(Directions.DOWN) and \
                    (possible_locations.__contains__(Directions.LEFT) or possible_locations.__contains__(Directions.RIGHT)):
                self.floor.add_room_next_to(boss_room, Directions.DOWN, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)

                if possible_locations.__contains__(Directions.LEFT):
                    self.floor.add_room_next_to(boss_room, Directions.LEFT, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)
                    self.floor.add_room_next_to(boss_room, Directions.DOWN_LEFT, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)

                elif possible_locations.__contains__(Directions.RIGHT):
                    self.floor.add_room_next_to(boss_room, Directions.RIGHT, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)
                    self.floor.add_room_next_to(boss_room, Directions.DOWN_RIGHT, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)
        else:
            self.floor.add_room_next_to(boss_room, possible_locations[0], BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)




        boss_room.set_type(RoomType.BOSS_ROOM)
        boss_room.set_color(BOSS_ROOM_COLOR)
        dead_end_indices.remove(boss_room_index)

    def add_special_rooms(self, dead_ends):
        i = 0
        while i < len(SPECIAL_ROOMS) and i < len(dead_ends):
            self.floor.get_rooms()[dead_ends[i]].set_type(SPECIAL_ROOMS[i])
            if SPECIAL_ROOMS[i] == RoomType.SHOP_ROOM:
                self.floor.get_rooms()[dead_ends[i]].set_color(SHOP_ROOM_COLOR)
            elif SPECIAL_ROOMS[i] == RoomType.ITEM_ROOM:
                self.floor.get_rooms()[dead_ends[i]].set_color(ITEM_ROOM_COLOR)
            i += 1

    def run(self):
        active: bool = True
        self.generate()
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        f = open("generator.json", "w")
                        f.write(self.toJSON())
                        f.close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.generate()
            self.screen.fill(Color.WHITE.value)
            self.floor.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(5)

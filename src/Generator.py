import math
import random
import Globals
from Globals import Color, RoomType, Directions
from Floor import Floor
import pygame
from rooms.PygameNormalRoom import PygameNormalRoom
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
    def __init__(self, seed: str, output_file: str, ui: bool):
        """
        Creates a new generator.
        :param seed: seed for the random generator
        :param output_file: file to save the floor to
        :param ui: whether to show the floor or not
        """
        if ui:
            self.screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
            self.clock = pygame.time.Clock()
        self._stage_id = 2
        self._number_of_rooms: int
        self._seed = seed
        self._output_file = output_file
        self._floors = deque()
        self._current_floor = -1
        random.seed(seed)

    def toJSON(self):
        j = "{\n" + '"seed": "' + self._seed + '",\n' + '"width": ' + str(Globals.width) + ',\n"height": ' + \
            str(Globals.height) + ',\n"floor": ' + self._floors[self._current_floor].toJSON() + "\n}"
        return j

    def get_room_amount(self) -> int:
        """
        Calculates the room amount.
        :return: room amount
        """
        if self._stage_id == -1:
            self._stage_id = 1
        return min(MAX_ROOMS, int(random.randint(0, 1) + 5 + math.floor(self._stage_id * 10) / 3.0))

    def generate(self) -> None:
        """
        Generates the rooms for the floor.
        """

        self._floors.append(Floor(Globals.height, Globals.width))
        self._current_floor = len(self._floors) - 1
        floor = self._floors[self._current_floor]

        number_of_rooms = self.get_room_amount()
        start_room: tuple = (random.randint(0, 8), random.randint(0, 7))
        floor.add_room(start_room[0], start_room[1], START_ROOM_COLOR, RoomType.START_ROOM)
        floor.add_to_floor_grid(start_room[0], start_room[1])
        number_of_current_rooms = 1

        room_queue: deque = deque([])  # Room coordinates
        room_queue.append(start_room)

        while number_of_current_rooms < number_of_rooms:

            while number_of_current_rooms < number_of_rooms:
                room = room_queue.pop()
                room_queue.appendleft(room)

                # Up
                if room[1] - 1 >= 0 and \
                        not floor.contains_room(room[0], room[1] - 1) and (
                        floor.count_neighbours(room[0], room[1] - 1) <= 1) and \
                        self._place_room():
                    self._append_and_add_to_floor_grid(room_queue, room, Directions.UP)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

                # Down
                if room[1] + 1 < Globals.height and \
                        not floor.contains_room(room[0], room[1] + 1) and floor.count_neighbours(
                    room[0], room[1] + 1) <= 1 and \
                        self._place_room():
                    self._append_and_add_to_floor_grid(room_queue, room, Directions.DOWN)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

                # Right
                if room[0] + 1 < Globals.width and \
                        not floor.contains_room(room[0] + 1, room[1]) and floor.count_neighbours(
                    room[0] + 1, room[1]) <= 1 and self._place_room():
                    self._append_and_add_to_floor_grid(room_queue, room, Directions.RIGHT)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

                # Left
                if room[0] - 1 >= 0 and \
                        not floor.contains_room(room[0] - 1, room[1]) and floor.count_neighbours(
                    room[0] - 1, room[1]) <= 1 and \
                        self._place_room():
                    self._append_and_add_to_floor_grid(room_queue, room, Directions.LEFT)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break
        room_queue.remove(start_room)
        while len(room_queue) > 0:
            room = room_queue.pop()
            floor.add_room(room[0], room[1], NORMAL_ROOM_COLOR)

        dead_ends = self.mark_dead_ends()
        self.add_boss_room(dead_ends, start_room)
        self.add_special_rooms(dead_ends)
        floor.add_doors_to_rooms()

    def _place_room(self) -> bool:
        return random.randint(1, 2) == 2

    def _append_and_add_to_floor_grid(self, room_queue, room, direction):
        floor = self._floors[self._current_floor]
        room_to_add: tuple
        if direction == Directions.UP:
            room_to_add = (room[0], room[1] - 1)
        elif direction == Directions.DOWN:
            room_to_add = (room[0], room[1] + 1)
        elif direction == Directions.LEFT:
            room_to_add = (room[0] - 1, room[1])
        elif direction == Directions.RIGHT:
            room_to_add = (room[0] + 1, room[1])
        else:
            raise ValueError(direction + "is not a valid direction!")
        room_queue.append(room_to_add)
        floor.add_to_floor_grid(room_to_add[0], room_to_add[1])

    def mark_dead_ends(self) -> list:
        """
        Searches for dead ends in the floor and marks them ands returns their indices in a list.
        :return: indices of all dead ends
        """
        dead_end_indices = []
        floor = self._floors[self._current_floor]
        i = 0
        while i < len(floor.get_rooms()):
            room = floor.get_rooms()[i]
            if floor.is_dead_end(room.get_x(), room.get_y()):
                if room.get_type() != RoomType.START_ROOM:
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
        floor = self._floors[self._current_floor]
        boss_room: PygameNormalRoom = None
        boss_room_index: int = None
        boss_room_x: int
        boss_room_y: int
        possible_locations: list = []

        for index in dead_end_indices:
            dead_end = floor.get_rooms()[index]
            if (abs(start_room[0] - dead_end.get_x()) >= MIN_DISTANCE) and (
                    abs(start_room[1] - dead_end.get_y()) >= MIN_DISTANCE):
                boss_room = dead_end
                boss_room_index = index
        if boss_room is None:
            boss_room = floor.get_rooms()[dead_end_indices[0]]
            boss_room_index = dead_end_indices[0]

        boss_room_x = boss_room.get_x()
        boss_room_y = boss_room.get_y()
        if (boss_room_x + 1 < Globals.width) and (
                floor.count_neighbours(boss_room_x + 1, boss_room_y) == 1) and not (
                floor.contains_room(boss_room_x + 1, boss_room_y)):
            possible_locations.append(Directions.RIGHT)

        if (boss_room_x - 1 >= 0) and (floor.count_neighbours(boss_room_x - 1, boss_room_y) == 1) and \
                not (floor.contains_room(boss_room_x - 1, boss_room_y)):
            possible_locations.append(Directions.LEFT)

        if (boss_room_y + 1 < Globals.height) and (floor.count_neighbours(boss_room_x, boss_room_y + 1) == 1) and \
                not (floor.contains_room(boss_room_x, boss_room_y + 1)):
            possible_locations.append(Directions.DOWN)

        if (boss_room_y - 1 >= 0) and (floor.count_neighbours(boss_room_x, boss_room_y - 1) == 1) and \
                not (floor.contains_room(boss_room_x, boss_room_y - 1)):
            possible_locations.append(Directions.UP)

        if len(possible_locations) == 0:
            # Place a teleport-room to the boss-room
            floor.add_teleport_room(boss_room)
            if not (floor.contains_room(0, 0)):
                boss_room.set_cord(0, 0)
            elif not (floor.contains_room(0, Globals.height - 1)):
                boss_room.set_cord(0, Globals.height - 1)
            elif not (floor.contains_room(Globals.width - 1, Globals.height - 1)):
                boss_room.set_cord(Globals.width - 1, Globals.height - 1)
            elif not (floor.contains_room(Globals.width - 1, 0)):
                boss_room.set_cord(Globals.width - 1, 0)

        elif len(possible_locations) >= 2:
            # Create a 4 * 4 boss-room
            if Directions.UP in possible_locations and Directions.RIGHT in possible_locations:
                self._add_rooms_next_to_room(boss_room, [Directions.UP, Directions.RIGHT, Directions.UP_RIGHT])

            elif Directions.UP in possible_locations and Directions.LEFT in possible_locations:
                self._add_rooms_next_to_room(boss_room, [Directions.LEFT, Directions.UP, Directions.UP_LEFT])

            elif Directions.DOWN in possible_locations and Directions.RIGHT in possible_locations:
                self._add_rooms_next_to_room(boss_room, [Directions.DOWN, Directions.RIGHT, Directions.DOWN_RIGHT])

            elif Directions.DOWN in possible_locations and Directions.LEFT in possible_locations:
                self._add_rooms_next_to_room(boss_room, [Directions.LEFT, Directions.DOWN, Directions.DOWN_LEFT])

        else:
            # Create a 2 * 2 boss-room
            floor.add_room_next_to(boss_room, possible_locations[0], BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)

        boss_room.set_type(RoomType.BOSS_ROOM)
        boss_room.set_color(BOSS_ROOM_COLOR)
        dead_end_indices.remove(boss_room_index)

    def _add_rooms_next_to_room(self, room, directions):
        floor = self._floors[self._current_floor]
        for direction in directions:
            floor.add_room_next_to(room, direction, BOSS_ROOM_COLOR, RoomType.BOSS_ROOM)

    def add_special_rooms(self, dead_ends: list) -> None:
        """
        Places the special rooms on the floor
        :param dead_ends: indices of all dead ends
        """
        floor = self._floors[self._current_floor]
        i = 0
        while i < len(SPECIAL_ROOMS) and i < len(dead_ends):
            floor.get_rooms()[dead_ends[i]].set_type(SPECIAL_ROOMS[i])
            if SPECIAL_ROOMS[i] == RoomType.SHOP_ROOM:
                floor.get_rooms()[dead_ends[i]].set_color(SHOP_ROOM_COLOR)
            elif SPECIAL_ROOMS[i] == RoomType.ITEM_ROOM:
                floor.get_rooms()[dead_ends[i]].set_color(ITEM_ROOM_COLOR)
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
                            self.save()
                        if event.key == pygame.K_LEFT:
                            if self._current_floor > 0:
                                self._current_floor -= 1
                        if event.key == pygame.K_RIGHT:
                            if self._current_floor < len(self._floors) - 1:
                                self._current_floor += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.generate()
            self.screen.fill(Color.WHITE.value)
            self._floors[self._current_floor].draw(self.screen)
            pygame.display.flip()
            self.clock.tick(5)

    def save(self):
        f = open(self._output_file, "w")
        f.write(self.toJSON())
        f.close()

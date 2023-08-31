import random
from collections import deque
from datetime import datetime
from typing import List

import utils
from globals import RoomType, Direction
import globals
from floors.floor import Floor
from rooms.room import Room


class Generator:
    """
    Objects of this class are representing generators.
    They generate a Floor object that contains all rooms.
    """

    def __init__(self, seed: str, output_file: str, stage_id: int = 2):
        """
        Creates a new generator with the given arguments.
        @param seed: seed for generating the floor
        @param output_file: file name for saving the result
        @param stage_id: id for the floor
        """
        self._stage_id = stage_id
        self._seed = seed
        self._output_file = output_file
        self._floor = Floor(globals.FLOOR_WIDTH, globals.FLOOR_HEIGHT)

    def to_json(self, indent: int) -> str:
        """
        Creates a string representation of the generator object.
        @return: json string of the generator
        """
        indent_s = globals.BASE_INDENT * indent

        j = "{\n" + \
            indent_s + '"_seed": "' + self._seed + '",\n' + \
            indent_s + '"_width": ' + str(globals.FLOOR_WIDTH) + ',\n' + \
            indent_s + '"_height": ' + str(globals.FLOOR_HEIGHT) + ',\n' + \
            indent_s + '"_floor": ' + self._floor.to_json(indent + 1) + ",\n" + \
            indent_s + '"_generated_by": "python"' + \
            "\n}"
        return j

    def _create_floor(self) -> None:
        """
        Creates a new floor.
        """
        self._floor = Floor(globals.FLOOR_HEIGHT, globals.FLOOR_WIDTH)

    def _add_new_room(self, new_room_tuple, room_tuple_queue: deque) -> bool:
        """
        Checks if a room can be added at the new position.
        @param new_room_tuple: position for the new room
        @param room_tuple_queue: queue for the rooms
        @return: True if the position was added to the queue otherwise False
        """
        print(str(new_room_tuple))
        if self._floor.is_within_border(new_room_tuple) and (not self._floor.contains_room(new_room_tuple)) and (
                self._floor.count_neighbours(new_room_tuple[0], new_room_tuple[1]) <= 1) and utils.place_room():
            room_tuple_queue.append(new_room_tuple)
            self._floor.add_to_floor_grid(new_room_tuple[0], new_room_tuple[1])
            return True
        return False

    def generate(self) -> None:
        """
        Generates the rooms for the floor.
        """
        self._create_floor()
        floor = self._floor
        number_of_rooms = utils.calculate_room_amount(self._stage_id)

        # Add start room
        start_room: tuple = (random.randint(0, 8), random.randint(0, 7))
        floor.add_room(start_room[0], start_room[1], RoomType.START_ROOM)
        number_of_current_rooms = 1
        room_tuple_queue: deque = deque([])  # Room coordinates
        room_tuple_queue.append(start_room)
        room_tuple_list = []
        while number_of_current_rooms < number_of_rooms and len(room_tuple_queue) > 0:
            room_tuple = room_tuple_queue.pop()
            for direction in Direction.main_directions():
                new_room_tuple = utils.add_direction_to_coordinates(direction, room_tuple)
                if self._add_new_room(new_room_tuple, room_tuple_queue):
                    number_of_current_rooms += 1
                    print(room_tuple_queue)
                    print(room_tuple_list)
            room_tuple_list.append(room_tuple)
            if len(room_tuple_queue) == 0 and number_of_current_rooms < number_of_rooms:
                room_tuple_queue.append(room_tuple_list.pop(0))

        # room_tuple_queue.remove(start_room)
        while len(room_tuple_queue) > 0:
            room_tuple_list.append(room_tuple_queue.pop())
        while len(room_tuple_queue) > 0:
            room_tuple = room_tuple_queue.pop()
            room_tuple_list.append(room_tuple)
        room_tuple_list.remove(start_room)
        while len(room_tuple_list) > 0:
            room_tuple = room_tuple_list.pop()
            floor.add_room(room_tuple[0], room_tuple[1])

        dead_ends = self.mark_dead_ends()
        self.add_boss_room(dead_ends, start_room)
        self.add_special_rooms(dead_ends)
        floor.add_doors_to_rooms()

    def mark_dead_ends(self) -> list:
        """
        Searches for dead ends in the floor and marks them ands returns their indices in a list.
        @return: indices of all dead ends
        """
        dead_end_indices = []
        floor = self._floor
        i = 0
        while i < len(floor.get_rooms()):
            room = floor.get_rooms()[i]
            if floor.is_dead_end(room.get_x(), room.get_y()):
                if room.get_type() == RoomType.NORMAL_ROOM:
                    room.set_type(RoomType.DEAD_END)
                    dead_end_indices += (i,)
            i += 1
        return dead_end_indices

    def _add_rooms_next_to_room(self, room, directions) -> None:
        """
        Adds new boss rooms next to a given room.
        @param room: new rooms will be placed next to this room
        @param directions: directions in which the new boss rooms will be placed
        """
        floor = self._floor
        for direction in directions:
            floor.add_room_next_to(room, direction, RoomType.BOSS_ROOM)

    def add_boss_room(self, dead_end_indices: list, start_room: tuple) -> None:
        """
        Marks a room as the boss room depending on the location of the start room.
        @param dead_end_indices: indices for all dead ends
        @param start_room: coordinates of the start room in a tuple
        """
        if len(dead_end_indices) == 0:
            return
        floor = self._floor
        boss_room: Room
        possible_locations: list = []
        boss_room_placed = False
        boss_room = floor.get_rooms()[dead_end_indices[0]]
        boss_room_index = dead_end_indices[0]
        max_distance = 0
        max_distance_index = 0
        for index in dead_end_indices:
            dead_end = floor.get_rooms()[index]
            current_distance = (start_room[0] - dead_end[0]) * (start_room[0] - dead_end[0]) + (start_room[1] - dead_end[1]) * (start_room[1] - dead_end[1])
            if max_distance < current_distance:
                max_distance = current_distance
                max_distance_index = index

            boss_room = floor.get_rooms()[max_distance_index]
            boss_room_index = max_distance_index

        boss_room_x = boss_room.get_x()
        boss_room_y = boss_room.get_y()
        for direction in Direction.main_directions():
            new_boss_tuple = utils.add_direction_to_coordinates(direction, (boss_room_x, boss_room_y))
            if (self._floor.is_within_border(new_boss_tuple) and
                    floor.count_neighbours(new_boss_tuple[0], new_boss_tuple[1]) == 1 and
                    not self._floor.contains_room(new_boss_tuple)):
                possible_locations.append(direction)

        if len(possible_locations) == 0:
            # Place a teleport-room to the boss-room
            self._place_boss_with_teleport_room(boss_room)
            boss_room_placed = True

        elif len(possible_locations) >= 2:
            # Create a 4 * 4 boss-room
            boss_room_placed = self._place_big_boss_room(possible_locations, boss_room)

        if not boss_room_placed:
            # Create a 2 * 2 boss-room
            floor.add_room_next_to(boss_room, possible_locations[0], RoomType.BOSS_ROOM)

        boss_room.set_type(RoomType.BOSS_ROOM)
        dead_end_indices.remove(boss_room_index)

    def _place_big_boss_room(self, possible_locations: List, boss_room: Room) -> bool:
        """
        Searches a free location to add more boss rooms next to the existing boss room.
        @param possible_locations: possible positions for the other boss rooms
        @param boss_room: current boss room
        @return: True if more boss rooms are added otherwise False
        """
        directions = [
            (Direction.RIGHT, Direction.UP, Direction.UP_RIGHT),
            (Direction.RIGHT, Direction.DOWN, Direction.DOWN_RIGHT),
            (Direction.LEFT, Direction.UP, Direction.UP_LEFT),
            (Direction.LEFT, Direction.DOWN, Direction.DOWN_LEFT)
        ]
        for direction in directions:
            corner = utils.add_direction_to_coordinates(direction[2], (boss_room[0], boss_room[1]))
            if direction[0] in possible_locations and direction[1] in possible_locations and self._floor.has_no_neighbours(corner[0], corner[1]):
                self._add_rooms_next_to_room(boss_room, direction)
                return True

        return False

    def _place_boss_with_teleport_room(self, boss_room) -> None:
        """
        Searches for a free places in the corners of the floor to replace the boss room.
        @param boss_room: boss room to replace
        """
        floor = self._floor
        floor.add_teleport_room(boss_room)
        if not (floor.contains_room((0, 0))) and floor.has_no_neighbours(0, 0):
            boss_room.set_cord(0, 0)

        elif (not (floor.contains_room((0, globals.FLOOR_HEIGHT - 1))) and
              floor.has_no_neighbours(0, globals.FLOOR_HEIGHT - 1)):
            boss_room.set_cord(0, globals.FLOOR_HEIGHT - 1)

        elif (not (floor.contains_room((globals.FLOOR_WIDTH - 1, globals.FLOOR_HEIGHT - 1))) and
              floor.has_no_neighbours(globals.FLOOR_WIDTH - 1, globals.FLOOR_HEIGHT - 1)):
            boss_room.set_cord(globals.FLOOR_WIDTH - 1, globals.FLOOR_HEIGHT - 1)

        elif (not (floor.contains_room((globals.FLOOR_WIDTH - 1, 0))) and
              floor.has_no_neighbours(globals.FLOOR_WIDTH - 1, 0)):
            boss_room.set_cord(globals.FLOOR_WIDTH - 1, 0)

    def add_special_rooms(self, dead_ends: list) -> None:
        """
        Places the special rooms on the dead ends of the floor.
        @param dead_ends: indices of all dead ends
        """
        floor = self._floor
        i = 0
        while i < len(globals.SPECIAL_ROOMS) and i < len(dead_ends):
            floor.get_rooms()[dead_ends[i]].set_type(globals.SPECIAL_ROOMS[i])
            i += 1

    def save(self) -> None:
        """
        Writes the generated floor in the output file.
        """
        output = self._output_file
        time = str(datetime.now().microsecond)
        output += time + globals.JSON_SUFFIX
        f = open(output, "w")
        f.write(self.to_json(1))
        f.close()

import random
from collections import deque
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
        :param seed: seed for generating the floor
        :param output_file: file name for saving the result
        :param stage_id: id for the floor
        """
        self._stage_id = stage_id
        self._seed = seed
        self._output_file = output_file
        self._floor = Floor(globals.FLOOR_WIDTH, globals.FLOOR_HEIGHT)

    def to_json(self, indent: int) -> str:
        """
        Creates a string representation of the generator object.
        :return: json string of the generator
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

    def _append_and_add_to_floor_grid(self, room_queue: deque, room: tuple, direction: Direction) -> None:
        """
        Appends a room in the given direction next to the given room and adds it to the floor grid.
        :param room_queue: queue to add the new room
        :param room: room which the new room should be placed next to
        :param direction: direction for placing the room
        """
        floor = self._floor
        room_to_add: tuple
        if direction == Direction.UP:
            room_to_add = (room[0], room[1] - 1)
        elif direction == Direction.DOWN:
            room_to_add = (room[0], room[1] + 1)
        elif direction == Direction.LEFT:
            room_to_add = (room[0] - 1, room[1])
        elif direction == Direction.RIGHT:
            room_to_add = (room[0] + 1, room[1])
        else:
            raise ValueError(str(direction) + "is not a valid direction!")
        room_queue.append(room_to_add)
        floor.add_to_floor_grid(room_to_add[0], room_to_add[1])


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
                        utils.place_room():
                    self._append_and_add_to_floor_grid(room_queue, room, Direction.UP)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

                # Down
                if room[1] + 1 < globals.FLOOR_HEIGHT and \
                        not floor.contains_room(room[0], room[1] + 1) and floor.count_neighbours(
                    room[0], room[1] + 1) <= 1 and \
                        utils.place_room():
                    self._append_and_add_to_floor_grid(room_queue, room, Direction.DOWN)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

                # Right
                if room[0] + 1 < globals.FLOOR_WIDTH and \
                        not floor.contains_room(room[0] + 1, room[1]) and floor.count_neighbours(
                        room[0] + 1, room[1]) <= 1 and utils.place_room():
                    self._append_and_add_to_floor_grid(room_queue, room, Direction.RIGHT)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break

                # Left
                if room[0] - 1 >= 0 and \
                        not floor.contains_room(room[0] - 1, room[1]) and floor.count_neighbours(
                    room[0] - 1, room[1]) <= 1 and \
                        utils.place_room():
                    self._append_and_add_to_floor_grid(room_queue, room, Direction.LEFT)
                    number_of_current_rooms += 1
                    if number_of_rooms == number_of_current_rooms:
                        break
        room_queue.remove(start_room)
        while len(room_queue) > 0:
            room = room_queue.pop()
            floor.add_room(room[0], room[1])

        dead_ends = self.mark_dead_ends()
        self.add_boss_room(dead_ends, start_room)
        self.add_special_rooms(dead_ends)
        floor.add_doors_to_rooms()

    def mark_dead_ends(self) -> list:
        """
        Searches for dead ends in the floor and marks them ands returns their indices in a list.
        :return: indices of all dead ends
        """
        dead_end_indices = []
        floor = self._floor
        i = 0
        while i < len(floor.get_rooms()):
            room = floor.get_rooms()[i]
            if floor.is_dead_end(room.get_x(), room.get_y()):
                if room.get_type() != RoomType.START_ROOM:
                    room.set_type(RoomType.DEAD_END)
                    dead_end_indices += (i,)
            i += 1
        return dead_end_indices

    def _add_rooms_next_to_room(self, room, directions) -> None:
        """
        Adds new boss rooms next to a given room.
        :param room: new rooms will be placed next to this room
        :param directions: directions in which the new boss rooms will be placed
        """
        floor = self._floor
        for direction in directions:
            floor.add_room_next_to(room, direction, RoomType.BOSS_ROOM)

    def add_boss_room(self, dead_end_indices: list, start_room: tuple) -> None:
        """
        Marks a room as the boss room depending on the location of the start room.
        :param dead_end_indices: indices for all dead ends
        :param start_room: coordinates of the start room in a tuple
        """
        floor = self._floor
        boss_room: Room
        boss_room_index: int = -1
        boss_room_x: int
        boss_room_y: int
        possible_locations: list = []
        boss_room_placed = False

        boss_room = floor.get_rooms()[dead_end_indices[0]]
        boss_room_index = dead_end_indices[0]

        for index in dead_end_indices:
            dead_end = floor.get_rooms()[index]
            if (abs(start_room[0] - dead_end.get_x()) >= globals.MIN_DISTANCE) and (
                    abs(start_room[1] - dead_end.get_y()) >= globals.MIN_DISTANCE):
                boss_room = dead_end
                boss_room_index = index

        boss_room_x = boss_room.get_x()
        boss_room_y = boss_room.get_y()
        if (boss_room_x + 1 < globals.FLOOR_WIDTH) and (
                floor.count_neighbours(boss_room_x + 1, boss_room_y) == 1) and not (
                floor.contains_room(boss_room_x + 1, boss_room_y)):
            possible_locations.append(Direction.RIGHT)

        if (boss_room_x - 1 >= 0) and (floor.count_neighbours(boss_room_x - 1, boss_room_y) == 1) and \
                not (floor.contains_room(boss_room_x - 1, boss_room_y)):
            possible_locations.append(Direction.LEFT)

        if (boss_room_y + 1 < globals.FLOOR_HEIGHT) and (floor.count_neighbours(boss_room_x, boss_room_y + 1) == 1) and \
                not (floor.contains_room(boss_room_x, boss_room_y + 1)):
            possible_locations.append(Direction.DOWN)

        if (boss_room_y - 1 >= 0) and (floor.count_neighbours(boss_room_x, boss_room_y - 1) == 1) and \
                not (floor.contains_room(boss_room_x, boss_room_y - 1)):
            possible_locations.append(Direction.UP)

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

    def _place_big_boss_room(self, possible_locations, boss_room):
        if Direction.UP in possible_locations and Direction.RIGHT in possible_locations:
            if self._floor.has_no_neighbours(boss_room[0] + 1, boss_room[1] - 1):
                self._add_rooms_next_to_room(boss_room, [Direction.UP, Direction.RIGHT, Direction.UP_RIGHT])
                return True

        if Direction.UP in possible_locations and Direction.LEFT in possible_locations:
            if self._floor.has_no_neighbours(boss_room[0] - 1, boss_room[1] - 1):
                self._add_rooms_next_to_room(boss_room, [Direction.LEFT, Direction.UP, Direction.UP_LEFT])
                return True

        if Direction.DOWN in possible_locations and Direction.RIGHT in possible_locations:
            if self._floor.has_no_neighbours(boss_room[0] + 1, boss_room[1] + 1):
                self._add_rooms_next_to_room(boss_room, [Direction.DOWN, Direction.RIGHT, Direction.DOWN_RIGHT])
                return True

        if Direction.DOWN in possible_locations and Direction.LEFT in possible_locations:
            if self._floor.has_no_neighbours(boss_room[0] - 1, boss_room[1] + 1):
                self._add_rooms_next_to_room(boss_room, [Direction.LEFT, Direction.DOWN, Direction.DOWN_LEFT])
                return True
        return False

    def _place_boss_with_teleport_room(self, boss_room) -> None:
        """
        Searches for a free places in the corners of the floor to replace the boss room.
        :param boss_room: boss room to replace
        """
        floor = self._floor
        floor.add_teleport_room(boss_room)
        if not (floor.contains_room(0, 0)) and floor.has_no_neighbours(0, 0):
            boss_room.set_cord(0, 0)
        elif not (floor.contains_room(0, globals.FLOOR_HEIGHT - 1)) and floor.has_no_neighbours(0, globals.FLOOR_HEIGHT - 1):
            boss_room.set_cord(0, globals.FLOOR_HEIGHT - 1)
        elif not (floor.contains_room(globals.FLOOR_WIDTH - 1, globals.FLOOR_HEIGHT - 1)) and floor.has_no_neighbours(
                globals.FLOOR_WIDTH - 1, globals.FLOOR_HEIGHT - 1):
            boss_room.set_cord(globals.FLOOR_WIDTH - 1, globals.FLOOR_HEIGHT - 1)
        elif not (floor.contains_room(globals.FLOOR_WIDTH - 1, 0)) and floor.has_no_neighbours(globals.FLOOR_WIDTH - 1, 0):
            boss_room.set_cord(globals.FLOOR_WIDTH - 1, 0)

    def add_special_rooms(self, dead_ends: list) -> None:
        """
        Places the special rooms on the floor
        :param dead_ends: indices of all dead ends
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
        f = open(self._output_file, "w")
        f.write(self.to_json(1))
        f.close()
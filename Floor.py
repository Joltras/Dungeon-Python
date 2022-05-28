import json

import pygame
import Globals
from Globals import Color, RoomType, DoorFace, Directions
from Room import Room, TeleportRoom
import numpy as np


class Floor:

    def __init__(self, height: int, width: int):
        self.__height = height
        self.__width = width
        self.__rooms: list = []
        self.floor_grid = np.zeros((height, width))
        self.rect = pygame.Rect(Globals.floor_plan_coordinates[1], Globals.floor_plan_coordinates[0],
                                width * Globals.room_width, height * Globals.room_height)
        self.room_id = 0

    def __getstate__(self):
        state = dict(self.__dict__)
        del state['rect']
        del state['floor_grid']
        del state['room_id']
        return state

    def toJSON(self):
        currentIndex: int = 0
        maxIndex: int = len(self.__rooms)
        j = "["
        for room in self.__rooms:
            if currentIndex < maxIndex - 1:
                j += room.toJSON() + ","
            else:
                j += room.toJSON()

            currentIndex += 1
        return j + "]"

    def draw(self, screen):
        for room in self.__rooms:
            room.draw(screen)
        for room in self.__rooms:
            room.draw_doors(screen)
        pygame.draw.rect(screen, Color.DARK_GRAY.value, self.rect, 2)

    def add_to_floor_grid(self, x, y):
        self.floor_grid[y][x] = 1

    def add_room(self, x: int, y: int, color: Color = Color.VIOLET, room_type=RoomType.NORMAL_ROOM):
        self.__rooms.append(Room(x=x, y=y, color=color, room_type=room_type, room_id=self.room_id))
        self.room_id += 1

    def add_room_next_to(self, room: Room, direction: Directions, color: Color, room_type: RoomType):
        if direction == Directions.UP:
            self.add_room(room.get_x(), room.get_y() - 1, color, room_type)
        elif direction == Directions.DOWN:
            self.add_room(room.get_x(), room.get_y() + 1, color, room_type)
        elif direction == Directions.LEFT:
            self.add_room(room.get_x() - 1, room.get_y(), color, room_type)
        elif direction == Directions.RIGHT:
            self.add_room(room.get_x() + 1, room.get_y(), color, room_type)
        elif direction == Directions.UP_RIGHT:
            self.add_room(room.get_x() + 1, room.get_y() - 1, color, room_type)
        elif direction == Directions.UP_LEFT:
            self.add_room(room.get_x() - 1, room.get_y() - 1, color, room_type)
        elif direction == Directions.DOWN_RIGHT:
            self.add_room(room.get_x() + 1, room.get_y() + 1, color, room_type)
        elif direction == Directions.DOWN_LEFT:
            self.add_room(room.get_x() - 1, room.get_y() + 1, color, room_type)

    def add_teleport_room(self, room: Room, color=Color.DARK_GRAY):
        t_room = TeleportRoom(x=room.get_x(), y=room.get_y(), color=color, room_id=self.room_id,
                              room_type=RoomType.BOSS_TELEPORT_ROOM, teleport_room_id=room.get_id())
        self.__rooms.append(t_room)
        self.room_id += 1

    def get_rooms(self):
        return self.__rooms

    def get_floor(self):
        return self.floor_grid

    def contains_room(self, x, y):
        return self.floor_grid[y][x] == 1

    def add_doors_to_rooms(self):
        for room in self.__rooms:
            x = room.get_x()
            y = room.get_y()
            if x + 1 < len(self.floor_grid[y]) and self.floor_grid[y][x + 1] == 1:
                room.add_door(DoorFace.EAST)
            if x - 1 >= 0 and self.floor_grid[y][x - 1] == 1:
                room.add_door(DoorFace.WEST)
            if y - 1 >= 0 and self.floor_grid[y - 1][x] == 1:
                room.add_door(DoorFace.TOP)
            if y + 1 < len(self.floor_grid) and self.floor_grid[y + 1][x] == 1:
                room.add_door(DoorFace.BOTTOM)

    def count_neighbours(self, x, y):
        neighbours = 0
        if y + 1 < len(self.floor_grid):
            neighbours += self.floor_grid[y + 1][x]
        if y - 1 >= 0:
            neighbours += self.floor_grid[y - 1][x]
        if x + 1 < len(self.floor_grid[y]):
            neighbours += self.floor_grid[y][x + 1]
        if x - 1 >= 0:
            neighbours += self.floor_grid[y][x - 1]
        return neighbours

    def is_dead_end(self, x: int, y: int) -> bool:
        return self.count_neighbours(x, y) == 1

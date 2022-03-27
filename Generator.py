import math
import random
import Globals
from Globals import Color
from Floor import Floor
import pygame
from collections import deque

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
    start_room: tuple = (random.randint(0, 8), random.randint(0, 7))
    floor.add_room(start_room[0], start_room[1], Color.ORANGE)
    number_of_current_rooms = 1
    room_queue: deque = deque([])
    room_queue.append(start_room)

    while number_of_current_rooms < number_of_rooms:

        while len(room_queue) > 0 and number_of_current_rooms < number_of_rooms:
            room = room_queue.pop()
            if room[1] - 1 > 0:
                if not floor.contains_room(room[0], room[1] - 1) and (
                        floor.count_neighbours(room[0], room[1] - 1) <= 1):
                    if random.randint(1, 2) == 2:
                        floor.add_room(room[0], room[1] - 1)
                        room_queue.append((room[0], room[1] - 1))
                        number_of_current_rooms += 1
                        if number_of_rooms == number_of_current_rooms:
                            break
                    else:
                        room_queue.appendleft(room)

            if room[1] + 1 < Globals.height:
                if not floor.contains_room(room[0], room[1] + 1) and floor.count_neighbours(room[0], room[1] + 1) <= 1:
                    if random.randint(1, 2) == 2:
                        floor.add_room(room[0], room[1] + 1)
                        room_queue.append((room[0], room[1] + 1))
                        number_of_current_rooms += 1
                        if number_of_rooms == number_of_current_rooms:
                            break
                    else:
                        room_queue.appendleft(room)

            if room[0] + 1 < Globals.width:
                if not floor.contains_room(room[0] + 1, room[1]) and floor.count_neighbours(room[0] + 1,  room[1]) <= 1:
                    if random.randint(1, 2) == 2:
                        floor.add_room(room[0] + 1, room[1])
                        room_queue.append((room[0] + 1, room[1]))
                        number_of_current_rooms += 1
                        if number_of_rooms == number_of_current_rooms:
                            break
                    else:
                        room_queue.appendleft(room)

            if room[0] - 1 > 0:
                if not floor.contains_room(room[0] - 1, room[1]) and floor.count_neighbours(room[0] - 1, room[1]) <= 1:
                    if random.randint(1, 2) == 2:
                        floor.add_room(room[0] - 1, room[1])
                        room_queue.append((room[0] - 1, room[1]))
                        number_of_current_rooms += 1
                        if number_of_rooms == number_of_current_rooms:
                            break
                    else:
                        room_queue.appendleft(room)


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


run()

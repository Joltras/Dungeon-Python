import random
import math
import globals
from globals import Direction


def calculate_room_amount(stage_id: int):
    """
    Calculates the room amount.
    :return: room amount
    """
    return min(globals.MAX_ROOMS, int(random.randint(0, 1) + 5 + math.floor(stage_id * 10) / 3.0))


def place_room() -> bool:
    """
    Checks if a new room should be placed.
    :return: True when room should be placed otherwise False
    """
    return random.randint(1, 50) >= 25


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def add_direction_to_coordinates(direction: Direction, coordinates: tuple) -> tuple:
    """
    Calculates the room according to the given room and direction
    @param direction: direction for the room to calculate
    @param coordinates: start point for the calculation
    @return: calculated point
    """
    if direction is Direction.UP:
        return coordinates[0], coordinates[1] - 1
    if direction is Direction.DOWN:
        return coordinates[0], coordinates[1] + 1
    if direction is Direction.LEFT:
        return coordinates[0] - 1, coordinates[1]
    if direction is Direction.RIGHT:
        return coordinates[0] + 1, coordinates[1]
    if direction is Direction.UP_LEFT:
        return coordinates[0] - 1, coordinates[1] - 1
    if direction is Direction.UP_RIGHT:
        return coordinates[0] + 1, coordinates[1] - 1
    if direction is Direction.DOWN_LEFT:
        return coordinates[0] - 1, coordinates[1] + 1
    if direction is Direction.DOWN_RIGHT:
        return coordinates[0] + 1, coordinates[1] + 1


json_file_options: dict = {
            'defaultextension': globals.JSON_SUFFIX,
            'filetypes': [('Json', globals.JSON_SUFFIX)],
        }

open_file_text: str = "Open File"
save_file_text: str = "Save File"
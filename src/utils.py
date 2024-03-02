"""
This module contains utility functions for the floor generator.
"""
import random
import math
from typing import Tuple

import globals as my_globals
from globals import Direction


def calculate_room_amount(stage_id: int):
    """
    Calculates the room amount.
    :return: room amount
    """
    return min(
        my_globals.MAX_ROOMS,
        int(random.randint(0, 1) + 5 + math.floor(stage_id * 10) / 3.0),
    )


def place_room() -> bool:
    """
    Checks if a new room should be placed.
    :return: True when room should be placed otherwise False
    """
    return random.randint(1, 50) >= 25


def rgb2hex(r, g, b):
    """
    Converts rgb to hex.
    """
    return f'#{r:02x}{g:02x}{b:02x}'


def add_direction_to_coordinates(
        direction: Direction, coordinates: Tuple[int, int]
) -> Tuple[int, int]:
    """
    Calculates the room according to the given room and direction
    @param direction: direction for the room to calculate
    @param coordinates: start point for the calculation
    @return: calculated point
    """
    result = None
    if direction is Direction.UP:
        result = coordinates[0], coordinates[1] - 1
    if direction is Direction.DOWN:
        result = coordinates[0], coordinates[1] + 1
    if direction is Direction.LEFT:
        result = coordinates[0] - 1, coordinates[1]
    if direction is Direction.RIGHT:
        result = coordinates[0] + 1, coordinates[1]
    if direction is Direction.UP_LEFT:
        result = coordinates[0] - 1, coordinates[1] - 1
    if direction is Direction.UP_RIGHT:
        result = coordinates[0] + 1, coordinates[1] - 1
    if direction is Direction.DOWN_LEFT:
        result = coordinates[0] - 1, coordinates[1] + 1
    if direction is Direction.DOWN_RIGHT:
        result = coordinates[0] + 1, coordinates[1] + 1
    return result


json_file_options: dict = {
    "defaultextension": my_globals.JSON_SUFFIX,
    "filetypes": [("Json", my_globals.JSON_SUFFIX)],
}

open_file_text: str = "Open File"
save_file_text: str = "Save File"

window_title: str = "Floor Generator"
window_size: str = "1200x550"


def calculate_distance(cord1, cord2) -> int:
    """
    Calculates the distance between two points.
    """
    return (cord1[0] - cord2[0]) * (cord1[0] - cord2[0]) + (cord1[1] - cord2[1]) * (
            cord1[1] - cord2[1]
    )

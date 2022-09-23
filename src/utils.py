import random
import math
import Globals


def calculate_room_amount(stage_id: int):
    """
    Calculates the room amount.
    :return: room amount
    """
    return min(Globals.MAX_ROOMS, int(random.randint(0, 1) + 5 + math.floor(stage_id * 10) / 3.0))


def place_room() -> bool:
    """
    Checks if a new room should be placed.
    :return: True when room should be placed otherwise False
    """
    return random.randint(1, 50) >= 25

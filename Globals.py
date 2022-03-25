from enum import Enum

room_width: int = 120
room_height: int = 60

window_multiplier: float = 2

width: int = 9
height: int = 8

window_height = height * room_height * window_multiplier
window_width = width * room_width * window_multiplier

floor_plan_coordinates = ((height * room_height) / 2, (width * room_width) / 2)


class Color(Enum):
    ORANGE = (255, 140, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (150, 150, 150)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)
    YELLOW = (250, 250, 55)
    VIOLET = (148, 0, 211)

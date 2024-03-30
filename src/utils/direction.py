"""
This module contains the direction enum.
"""

from enum import Enum


class Direction(Enum):
    """
    Enum for the directions.
    """

    @classmethod
    def list(cls):
        """
        Returns a list of all the directions.
        """
        return list(map(lambda c: c.value, cls))

    @classmethod
    def main_directions(cls):
        """
        Returns a list of all the main directions.
        """
        return cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT

    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP_RIGHT = (1, -1)
    UP_LEFT = (-1, -1)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (-1, 1)

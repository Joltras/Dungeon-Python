from enum import Enum


class RoomType(Enum):
    """
    Enum for the room types.
    """

    @classmethod
    def list(cls):
        """
        Returns a list of all the room types.
        """
        return list(map(lambda c: c.value, cls))

    NORMAL_ROOM = 0
    DEAD_END = 1
    ITEM_ROOM = 2
    SHOP_ROOM = 3
    START_ROOM = 4
    TELEPORT_ROOM = 5
    BOSS_ROOM = 6

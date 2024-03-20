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

    def is_special(self) -> bool:
        """
        Checks if the room type is special.
        Special rooms are rooms that have a special function.
        Special rooms are:
        - Item room
        - Shop room
        - Boss room
        - Secret room
        @return: True if special otherwise False
        """
        switcher = {
            self.NORMAL_ROOM: False,
            self.DEAD_END: False,
            self.ITEM_ROOM: True,
            self.SHOP_ROOM: True,
            self.START_ROOM: False,
            self.TELEPORT_ROOM: False,
            self.BOSS_ROOM: True,
            self.SECRET_ROOM: True,
        }
        return switcher[self]

    NORMAL_ROOM = 0
    DEAD_END = 1
    ITEM_ROOM = 2
    SHOP_ROOM = 3
    START_ROOM = 4
    TELEPORT_ROOM = 5
    BOSS_ROOM = 6
    SECRET_ROOM = 7

import unittest
from rooms.teleport_room import TeleportRoom


class TeleportRoomTest(unittest.TestCase):

    def setUp(self) -> None:
        self._t_room = TeleportRoom(1, 2, 3, 4)

    def test_get_connected_room(self):
        self.assertEqual(4, self._t_room.get_connected_room_id())


if __name__ == '__main__':
    unittest.main()

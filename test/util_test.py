import unittest
from utils import utils, globals


class UtilsTest(unittest.TestCase):
    def test_calculate_room_amount(self):
        rooms = utils.calculate_room_amount(2)
        self.assertTrue(0 < rooms <= globals.MAX_ROOMS)

    def test_place_room(self):
        utils.place_room()


if __name__ == "__main__":
    unittest.main()

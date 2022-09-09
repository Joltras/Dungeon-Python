import unittest

from floors.PygameFloor import PygameFloor


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._floor = PygameFloor(20, 30)

    def test_to_json(self):
        expected = "{\n\"rooms\": []\n}"
        self.assertEqual(expected, self._floor.toJSON())


if __name__ == '__main__':
    unittest.main()

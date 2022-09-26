import unittest
from collections import deque
from generators.PygameGenerator import PygameGenerator


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._generator = PygameGenerator("", "test.json")

    def test_get_floors(self):
        self.assertEqual(deque(), self._generator.get_floors())


if __name__ == '__main__':
    unittest.main()

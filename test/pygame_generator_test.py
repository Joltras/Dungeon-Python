import unittest
from collections import deque
from generators.pygame_generator import PygameGenerator


class PygameGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        self._generator = PygameGenerator("", "test.json", "", 0)

    def test_get_floors(self):
        self.assertEqual(deque(), self._generator.get_floors())


if __name__ == "__main__":
    unittest.main()
